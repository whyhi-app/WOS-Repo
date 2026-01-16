"""
WOS Canon Embeddings v0 (Phase 4.1)
Semantic search using OpenAI embeddings + vector similarity
Upgrades Canon Index from text matching to intelligent retrieval
"""

import sqlite3
import logging
import numpy as np
from typing import List, Dict, Any, Optional
import os
import openai

logger = logging.getLogger("wos.canon_embeddings")

class CanonEmbeddings:
    """
    Canon Embeddings Layer
    
    Adds semantic search to Canon Index using:
    - OpenAI text-embedding-3-small (cheap, fast, good quality)
    - Cosine similarity for relevance scoring
    - SQLite for vector storage (with JSON serialization)
    """
    
    def __init__(self, db_path: str = "canon.db", api_key: str = None):
        self.db_path = db_path
        self.conn = None
        self.openai_api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.openai_api_key:
            logger.warning("OPENAI_API_KEY not set - embeddings will fail")
        
        openai.api_key = self.openai_api_key
        
        self.embedding_model = "text-embedding-3-small"
        self.embedding_dimension = 1536  # Dimension for text-embedding-3-small
        
        self.init_db()
    
    def init_db(self):
        """Initialize embeddings table in Canon database"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()
        
        # Embeddings table - stores vectors as JSON arrays
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS artifact_embeddings (
                embedding_id TEXT PRIMARY KEY,
                artifact_id TEXT NOT NULL,
                embedding_vector TEXT NOT NULL,
                embedding_model TEXT NOT NULL,
                embedding_dimension INTEGER NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (artifact_id) REFERENCES artifacts(artifact_id)
            )
        """)
        
        # Index for fast lookups
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_embedding_artifact 
            ON artifact_embeddings(artifact_id)
        """)
        
        self.conn.commit()
        logger.info("Canon embeddings table initialized")
    
    def generate_embedding(self, text: str) -> Optional[List[float]]:
        """
        Generate embedding vector for text using OpenAI
        
        Args:
            text: Text to embed (will be truncated to 8191 tokens)
        
        Returns: List of floats (1536 dimensions) or None if failed
        """
        try:
            # Truncate text if too long (OpenAI limit is ~8k tokens)
            text_truncated = text[:30000]  # ~8k tokens max
            
            response = openai.embeddings.create(
                model=self.embedding_model,
                input=text_truncated
            )
            
            embedding = response.data[0].embedding
            logger.info(f"Generated embedding: {len(embedding)} dimensions")
            return embedding
        
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            return None
    
    def store_embedding(self, artifact_id: str, embedding: List[float]) -> bool:
        """
        Store embedding vector for an artifact
        
        Args:
            artifact_id: Artifact ID
            embedding: Vector (list of floats)
        
        Returns: True if successful
        """
        try:
            cursor = self.conn.cursor()
            embedding_id = f"emb_{artifact_id}"
            
            # Serialize vector as JSON
            import json
            embedding_json = json.dumps(embedding)
            
            cursor.execute("""
                INSERT OR REPLACE INTO artifact_embeddings
                (embedding_id, artifact_id, embedding_vector, 
                 embedding_model, embedding_dimension)
                VALUES (?, ?, ?, ?, ?)
            """, (embedding_id, artifact_id, embedding_json,
                  self.embedding_model, len(embedding)))
            
            self.conn.commit()
            logger.info(f"Stored embedding for {artifact_id}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to store embedding: {e}")
            return False
    
    def get_embedding(self, artifact_id: str) -> Optional[np.ndarray]:
        """
        Retrieve embedding vector for an artifact
        
        Args:
            artifact_id: Artifact ID
        
        Returns: NumPy array of embedding or None
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT embedding_vector FROM artifact_embeddings
                WHERE artifact_id = ?
            """, (artifact_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            import json
            embedding = json.loads(row[0])
            return np.array(embedding)
        
        except Exception as e:
            logger.error(f"Failed to get embedding: {e}")
            return None
    
    def embed_artifact(self, artifact_id: str, artifact_text: str) -> bool:
        """
        Generate and store embedding for an artifact
        
        Args:
            artifact_id: Artifact ID
            artifact_text: Text to embed (title + summary + content)
        
        Returns: True if successful
        """
        logger.info(f"Embedding artifact: {artifact_id}")
        
        # Generate embedding
        embedding = self.generate_embedding(artifact_text)
        if not embedding:
            logger.error(f"Failed to embed artifact {artifact_id}")
            return False
        
        # Store embedding
        success = self.store_embedding(artifact_id, embedding)
        return success
    
    def semantic_search(self, query: str, limit: int = 10,
                       artifact_type: str = None, category: str = None,
                       min_similarity: float = 0.5) -> List[Dict[str, Any]]:
        """
        Semantic search using cosine similarity
        
        Args:
            query: Search query
            limit: Max results
            artifact_type: Filter by type (optional)
            category: Filter by category (optional)
            min_similarity: Minimum cosine similarity threshold (0-1)
        
        Returns: List of artifacts with similarity scores
        """
        logger.info(f"Semantic search: query='{query}', limit={limit}")
        
        # Step 1: Generate query embedding
        query_embedding = self.generate_embedding(query)
        if not query_embedding:
            logger.error("Failed to generate query embedding")
            return []
        
        query_vector = np.array(query_embedding)
        
        # Step 2: Get all artifact embeddings
        cursor = self.conn.cursor()
        
        # Build query with filters
        sql = """
            SELECT ae.artifact_id, ae.embedding_vector, 
                   a.title, a.type, a.category, a.summary, a.source
            FROM artifact_embeddings ae
            JOIN artifacts a ON ae.artifact_id = a.artifact_id
            WHERE 1=1
        """
        params = []
        
        if artifact_type:
            sql += " AND a.type = ?"
            params.append(artifact_type)
        
        if category:
            sql += " AND a.category = ?"
            params.append(category)
        
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        
        if not rows:
            logger.warning("No embeddings found in database")
            return []
        
        # Step 3: Calculate cosine similarity for each artifact
        import json
        results = []
        
        for row in rows:
            artifact_id = row[0]
            embedding_json = row[1]
            
            # Deserialize embedding
            embedding = np.array(json.loads(embedding_json))
            
            # Calculate cosine similarity
            similarity = self._cosine_similarity(query_vector, embedding)
            
            # Filter by minimum similarity
            if similarity < min_similarity:
                continue
            
            results.append({
                "artifact_id": artifact_id,
                "title": row[2],
                "type": row[3],
                "category": row[4],
                "summary": row[5],
                "source": row[6],
                "similarity": float(similarity),
                "relevance_score": float(similarity * 10)  # Scale to 0-10
            })
        
        # Step 4: Sort by similarity (descending) and limit
        results.sort(key=lambda x: x["similarity"], reverse=True)
        results = results[:limit]
        
        logger.info(f"Semantic search returned {len(results)} results")
        return results
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors
        
        Args:
            vec1: First vector
            vec2: Second vector
        
        Returns: Similarity score (0-1)
        """
        # Normalize vectors
        vec1_norm = vec1 / np.linalg.norm(vec1)
        vec2_norm = vec2 / np.linalg.norm(vec2)
        
        # Dot product
        similarity = np.dot(vec1_norm, vec2_norm)
        
        return similarity
    
    def has_embedding(self, artifact_id: str) -> bool:
        """Check if artifact has an embedding"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM artifact_embeddings
            WHERE artifact_id = ?
        """, (artifact_id,))
        
        count = cursor.fetchone()[0]
        return count > 0
    
    def reindex_all(self, canon_index) -> Dict[str, int]:
        """
        Reindex all artifacts (generate embeddings for all)
        
        Args:
            canon_index: CanonIndex instance to read artifacts from
        
        Returns: Stats {total, success, failed}
        """
        logger.info("Reindexing all artifacts")
        
        # Get all artifacts
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT artifact_id, title, summary, content
            FROM artifacts
        """)
        
        artifacts = cursor.fetchall()
        
        stats = {"total": len(artifacts), "success": 0, "failed": 0}
        
        for row in artifacts:
            artifact_id = row[0]
            title = row[1] or ""
            summary = row[2] or ""
            content = row[3] or ""
            
            # Combine text for embedding
            artifact_text = f"{title}\n{summary}\n{content}"
            
            # Generate and store embedding
            success = self.embed_artifact(artifact_id, artifact_text)
            
            if success:
                stats["success"] += 1
            else:
                stats["failed"] += 1
        
        logger.info(f"Reindex complete: {stats}")
        return stats
    
    def get_stats(self) -> Dict[str, Any]:
        """Get embeddings statistics"""
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM artifact_embeddings")
        total_embeddings = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM artifacts a
            WHERE NOT EXISTS (
                SELECT 1 FROM artifact_embeddings ae
                WHERE ae.artifact_id = a.artifact_id
            )
        """)
        missing_embeddings = cursor.fetchone()[0]
        
        return {
            "total_embeddings": total_embeddings,
            "missing_embeddings": missing_embeddings,
            "embedding_model": self.embedding_model,
            "embedding_dimension": self.embedding_dimension
        }
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def __del__(self):
        self.close()
