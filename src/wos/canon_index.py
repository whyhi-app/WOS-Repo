"""
WOS Canon Index v0
Artifact registry and retrieval system
Implements Phase 4 Memory Layer - retrieval-first knowledge base
"""

import sqlite3
import json
import logging
from datetime import datetime
from typing import Optional, Dict, List, Any
import hashlib

logger = logging.getLogger("wos.canon_index")

class CanonIndex:
    """
    Canon Index v0
    
    SQLite-backed artifact registry following AOS Memory & Observability spec.
    Stores decision history, context, and retrieved knowledge.
    Enables retrieval-first decision making.
    """
    
    def __init__(self, db_path: str = "canon.db"):
        self.db_path = db_path
        self.conn = None
        self.init_db()
    
    def init_db(self):
        """Initialize SQLite database with Canon Index schema"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()
        
        # Artifacts table - central knowledge store
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS artifacts (
                artifact_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                type TEXT NOT NULL,
                category TEXT,
                content TEXT NOT NULL,
                summary TEXT,
                source TEXT,
                source_url TEXT,
                approval_status TEXT DEFAULT 'draft',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                expires_at TEXT,
                owner TEXT DEFAULT 'wos',
                tags TEXT,
                metadata JSON,
                checksum TEXT
            )
        """)
        
        # Artifact retrieval log (audit trail)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS retrieval_log (
                log_id TEXT PRIMARY KEY,
                artifact_id TEXT NOT NULL,
                request_id TEXT,
                execution_id TEXT,
                intent_id TEXT,
                retrieval_type TEXT,
                relevance_score REAL,
                retrieved_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (artifact_id) REFERENCES artifacts(artifact_id)
            )
        """)
        
        # Artifact relationships (for linking related knowledge)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS artifact_relationships (
                rel_id TEXT PRIMARY KEY,
                source_artifact_id TEXT NOT NULL,
                target_artifact_id TEXT NOT NULL,
                relationship_type TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (source_artifact_id) REFERENCES artifacts(artifact_id),
                FOREIGN KEY (target_artifact_id) REFERENCES artifacts(artifact_id)
            )
        """)
        
        # Search index (for fast lookups)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS search_index (
                idx_id TEXT PRIMARY KEY,
                artifact_id TEXT NOT NULL,
                searchable_text TEXT,
                indexed_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (artifact_id) REFERENCES artifacts(artifact_id)
            )
        """)
        
        # Create indexes for performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_artifact_type ON artifacts(type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_artifact_category ON artifacts(category)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_artifact_created ON artifacts(created_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_artifact_approval ON artifacts(approval_status)")
        
        self.conn.commit()
        logger.info(f"Canon Index initialized at {self.db_path}")
    
    def store_artifact(self, artifact_id: str, title: str, content: str,
                      artifact_type: str = "document", category: str = None,
                      summary: str = None, source: str = None,
                      source_url: str = None, tags: List[str] = None,
                      metadata: Dict = None) -> bool:
        """
        Store a new artifact in Canon Index
        
        Args:
            artifact_id: Unique artifact identifier
            title: Human-readable title
            content: Full artifact content
            artifact_type: "decision", "context", "brief", "log", etc.
            category: Business category (product, growth, operations, finance)
            summary: Brief summary for fast retrieval
            source: Where this came from (workflow, email, etc.)
            source_url: Link to original source
            tags: List of tags for categorization
            metadata: Additional JSON metadata
        
        Returns: True if successful
        """
        try:
            cursor = self.conn.cursor()
            
            # Generate checksum for content integrity
            checksum = hashlib.sha256(content.encode()).hexdigest()
            
            cursor.execute("""
                INSERT OR REPLACE INTO artifacts 
                (artifact_id, title, type, category, content, summary, 
                 source, source_url, tags, metadata, checksum, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                artifact_id, title, artifact_type, category, content,
                summary, source, source_url,
                json.dumps(tags) if tags else None,
                json.dumps(metadata) if metadata else None,
                checksum,
                datetime.utcnow().isoformat()
            ))
            
            # Update search index
            self._index_artifact(artifact_id, title, content, tags or [])
            
            self.conn.commit()
            logger.info(f"Stored artifact: {artifact_id}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to store artifact {artifact_id}: {e}")
            return False
    
    def get_artifact(self, artifact_id: str, log_retrieval: bool = True,
                    request_id: str = None, execution_id: str = None) -> Optional[Dict]:
        """
        Retrieve full artifact by ID
        
        Args:
            artifact_id: Artifact ID
            log_retrieval: Whether to log this retrieval (for audit)
            request_id: Request ID for audit trail
            execution_id: Execution ID for audit trail
        
        Returns: Artifact dict or None if not found
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM artifacts WHERE artifact_id = ?", (artifact_id,))
        row = cursor.fetchone()
        
        if not row:
            logger.warning(f"Artifact not found: {artifact_id}")
            return None
        
        artifact = dict(row)
        
        # Parse JSON fields
        if artifact.get("tags"):
            artifact["tags"] = json.loads(artifact["tags"])
        if artifact.get("metadata"):
            artifact["metadata"] = json.loads(artifact["metadata"])
        
        # Log retrieval for audit trail
        if log_retrieval:
            self._log_retrieval(artifact_id, "get", request_id, execution_id)
        
        logger.info(f"Retrieved artifact: {artifact_id}")
        return artifact
    
    def search_artifacts(self, query: str, limit: int = 10,
                        artifact_type: str = None, category: str = None,
                        request_id: str = None, execution_id: str = None) -> List[Dict]:
        """
        Search Canon Index for relevant artifacts
        
        Args:
            query: Search query (simple text matching for v0)
            limit: Max results to return
            artifact_type: Filter by type (optional)
            category: Filter by category (optional)
            request_id: Request ID for audit
            execution_id: Execution ID for audit
        
        Returns: List of artifact summaries with relevance scores
        """
        try:
            query_lower = query.lower()
            
            # Build query
            sql = "SELECT * FROM artifacts WHERE "
            params = []
            
            # Search in title and summary
            sql += "(LOWER(title) LIKE ? OR LOWER(summary) LIKE ?)"
            params.append(f"%{query_lower}%")
            params.append(f"%{query_lower}%")
            
            # Filter by type if specified
            if artifact_type:
                sql += " AND type = ?"
                params.append(artifact_type)
            
            # Filter by category if specified
            if category:
                sql += " AND category = ?"
                params.append(category)
            
            # Order by recency, limit results
            sql += " ORDER BY created_at DESC LIMIT ?"
            params.append(limit)
            
            cursor = self.conn.cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            
            # Convert to dicts with relevance scores
            results = []
            for row in rows:
                artifact = dict(row)
                
                # Calculate relevance score (simple: how many times query appears)
                content_text = (artifact.get("title", "") + " " + 
                               artifact.get("summary", "") + " " + 
                               artifact.get("content", "")).lower()
                relevance_score = min(10.0, content_text.count(query_lower) * 2.0)
                
                artifact["relevance_score"] = relevance_score
                
                # Log retrieval
                if request_id or execution_id:
                    self._log_retrieval(
                        artifact["artifact_id"], "search",
                        request_id, execution_id, relevance_score
                    )
                
                # Return summary, not full content
                results.append({
                    "artifact_id": artifact["artifact_id"],
                    "title": artifact["title"],
                    "type": artifact["type"],
                    "category": artifact["category"],
                    "summary": artifact.get("summary", artifact["content"][:200]),
                    "source": artifact.get("source"),
                    "relevance_score": relevance_score,
                    "created_at": artifact["created_at"]
                })
            
            logger.info(f"Search found {len(results)} artifacts for: {query}")
            return results
        
        except Exception as e:
            logger.error(f"Search failed: {e}", exc_info=True)
            return []
    
    def list_artifacts(self, artifact_type: str = None, category: str = None,
                      limit: int = 50) -> List[Dict]:
        """
        List artifacts, optionally filtered
        
        Args:
            artifact_type: Filter by type
            category: Filter by category
            limit: Max results
        
        Returns: List of artifact summaries
        """
        sql = "SELECT * FROM artifacts WHERE 1=1"
        params = []
        
        if artifact_type:
            sql += " AND type = ?"
            params.append(artifact_type)
        
        if category:
            sql += " AND category = ?"
            params.append(category)
        
        sql += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        
        return [
            {
                "artifact_id": dict(row)["artifact_id"],
                "title": dict(row)["title"],
                "type": dict(row)["type"],
                "category": dict(row)["category"],
                "created_at": dict(row)["created_at"]
            }
            for row in cursor.fetchall()
        ]
    
    def link_artifacts(self, source_id: str, target_id: str,
                      relationship_type: str = "related") -> bool:
        """
        Link two artifacts (for knowledge graph)
        
        Args:
            source_id: Source artifact ID
            target_id: Target artifact ID
            relationship_type: Type of relationship (related, child, decision, etc.)
        
        Returns: True if successful
        """
        try:
            cursor = self.conn.cursor()
            rel_id = f"{source_id}→{target_id}"
            
            cursor.execute("""
                INSERT OR REPLACE INTO artifact_relationships
                (rel_id, source_artifact_id, target_artifact_id, relationship_type)
                VALUES (?, ?, ?, ?)
            """, (rel_id, source_id, target_id, relationship_type))
            
            self.conn.commit()
            logger.info(f"Linked artifacts: {source_id} → {target_id}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to link artifacts: {e}")
            return False
    
    def get_related_artifacts(self, artifact_id: str) -> List[Dict]:
        """Get artifacts related to a given artifact"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT target_artifact_id, relationship_type
            FROM artifact_relationships
            WHERE source_artifact_id = ?
            ORDER BY created_at DESC
        """, (artifact_id,))
        
        related = []
        for row in cursor.fetchall():
            target_id = row[0]
            rel_type = row[1]
            target = self.get_artifact(target_id, log_retrieval=False)
            if target:
                related.append({
                    "artifact_id": target_id,
                    "relationship_type": rel_type,
                    "title": target["title"]
                })
        
        return related
    
    def approve_artifact(self, artifact_id: str, approver: str = "founder") -> bool:
        """Mark artifact as approved"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE artifacts
                SET approval_status = 'approved', updated_at = ?
                WHERE artifact_id = ?
            """, (datetime.utcnow().isoformat(), artifact_id))
            
            self.conn.commit()
            logger.info(f"Approved artifact: {artifact_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to approve artifact: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get Canon Index statistics"""
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as total FROM artifacts")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT type, COUNT(*) as count FROM artifacts GROUP BY type")
        by_type = {row[0]: row[1] for row in cursor.fetchall()}
        
        cursor.execute("SELECT category, COUNT(*) as count FROM artifacts WHERE category IS NOT NULL GROUP BY category")
        by_category = {row[0]: row[1] for row in cursor.fetchall()}
        
        cursor.execute("SELECT COUNT(*) as total FROM retrieval_log")
        total_retrievals = cursor.fetchone()[0]
        
        return {
            "total_artifacts": total,
            "by_type": by_type,
            "by_category": by_category,
            "total_retrievals": total_retrievals,
            "db_path": self.db_path
        }
    
    def _index_artifact(self, artifact_id: str, title: str, content: str,
                       tags: List[str]):
        """Create search index for artifact (internal)"""
        try:
            cursor = self.conn.cursor()
            searchable_text = f"{title} {content} {' '.join(tags)}".lower()
            
            cursor.execute("""
                INSERT OR REPLACE INTO search_index
                (idx_id, artifact_id, searchable_text)
                VALUES (?, ?, ?)
            """, (f"idx_{artifact_id}", artifact_id, searchable_text[:5000]))
            
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to index artifact: {e}")
    
    def _log_retrieval(self, artifact_id: str, retrieval_type: str,
                      request_id: str = None, execution_id: str = None,
                      relevance_score: float = None):
        """Log artifact retrieval for audit trail (internal)"""
        try:
            cursor = self.conn.cursor()
            log_id = f"log_{artifact_id}_{datetime.utcnow().isoformat()}"
            
            cursor.execute("""
                INSERT INTO retrieval_log
                (log_id, artifact_id, request_id, execution_id, retrieval_type, relevance_score)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (log_id, artifact_id, request_id, execution_id, retrieval_type, relevance_score))
            
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log retrieval: {e}")
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def __del__(self):
        self.close()
