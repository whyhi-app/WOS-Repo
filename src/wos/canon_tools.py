"""
WOS Canon Tools v0.1 (with Semantic Search)
Retrieval-first interface for Canon Index (SQLite-backed)
Implements Phase 4 Memory Layer tools + Phase 4.1 Semantic Search
"""

import logging
from typing import Dict, List, Any, Optional
from wos.canon_index import CanonIndex
from wos.canon_embeddings import CanonEmbeddings

logger = logging.getLogger("wos.canon_tools")

class CanonTools:
    """
    Canon Tools v0.1
    
    Provides retrieval interface for Canon Index.
    Enables handlers to search and retrieve knowledge.
    Implements retrieval-first decision making with semantic search.
    """
    
    def __init__(self, canon_index: CanonIndex = None, canon_db_path: str = "canon.db",
                 use_semantic_search: bool = True, openai_api_key: str = None):
        """
        Initialize Canon Tools
        
        Args:
            canon_index: Existing CanonIndex instance (or None to create new)
            canon_db_path: Path to Canon SQLite database
            use_semantic_search: Enable semantic search (requires OpenAI API key)
            openai_api_key: OpenAI API key for embeddings
        """
        if canon_index:
            self.canon = canon_index
        else:
            self.canon = CanonIndex(db_path=canon_db_path)
        
        # Initialize embeddings layer if enabled
        self.use_semantic_search = use_semantic_search
        self.embeddings = None
        
        if use_semantic_search:
            try:
                self.embeddings = CanonEmbeddings(
                    db_path=canon_db_path,
                    api_key=openai_api_key
                )
                logger.info("Semantic search enabled")
            except Exception as e:
                logger.warning(f"Failed to initialize semantic search: {e}")
                logger.warning("Falling back to text search")
                self.use_semantic_search = False
    
    def search(self, query: str, limit: int = 5, artifact_type: str = None,
              category: str = None, request_id: str = None,
              execution_id: str = None, use_semantic: bool = None) -> List[Dict[str, Any]]:
        """
        Search Canon Index for relevant artifacts
        
        Uses semantic search (embeddings) if enabled, falls back to text search.
        
        Args:
            query: Search query (text)
            limit: Max results to return
            artifact_type: Filter by type (optional)
            category: Filter by category (optional)
            request_id: Request ID for audit trail
            execution_id: Execution ID for audit trail
            use_semantic: Override semantic search setting (True/False/None)
        
        Returns: List of artifact references:
        [
            {
                "artifact_id": str,
                "title": str,
                "type": str,
                "category": str,
                "summary": str,
                "relevance_score": float (0-10),
                "source": str,
                "similarity": float (0-1, if semantic search used)
            }
        ]
        """
        logger.info(f"Canon search: query='{query}', limit={limit}")
        
        # Determine which search method to use
        should_use_semantic = (
            use_semantic if use_semantic is not None 
            else self.use_semantic_search
        )
        
        results = []
        
        # Try semantic search first
        if should_use_semantic and self.embeddings:
            try:
                logger.info("Using semantic search")
                results = self.embeddings.semantic_search(
                    query=query,
                    limit=limit,
                    artifact_type=artifact_type,
                    category=category,
                    min_similarity=0.5
                )
                
                # Log retrievals
                for result in results:
                    if request_id or execution_id:
                        self.canon._log_retrieval(
                            result["artifact_id"], "semantic_search",
                            request_id, execution_id, result.get("relevance_score")
                        )
                
                logger.info(f"Semantic search returned {len(results)} results")
            except Exception as e:
                logger.error(f"Semantic search failed: {e}")
                logger.warning("Falling back to text search")
                results = []
        
        # Fall back to text search if semantic failed or disabled
        if not results:
            logger.info("Using text search")
            results = self.canon.search_artifacts(
                query=query,
                limit=limit,
                artifact_type=artifact_type,
                category=category,
                request_id=request_id,
                execution_id=execution_id
            )
        
        logger.info(f"Canon search returned {len(results)} results")
        return results
    
    def get(self, artifact_id: str, request_id: str = None,
           execution_id: str = None) -> Optional[Dict[str, Any]]:
        """
        Retrieve full artifact by ID
        
        Args:
            artifact_id: Artifact ID
            request_id: Request ID for audit trail
            execution_id: Execution ID for audit trail
        
        Returns:
        {
            "artifact_id": str,
            "title": str,
            "type": str,
            "category": str,
            "content": str (full),
            "summary": str,
            "source": str,
            "source_url": str,
            "created_at": str,
            "updated_at": str,
            "tags": [str],
            "approval_status": str
        }
        """
        logger.info(f"Canon get: {artifact_id}")
        
        artifact = self.canon.get_artifact(
            artifact_id=artifact_id,
            log_retrieval=True,
            request_id=request_id,
            execution_id=execution_id
        )
        
        if not artifact:
            logger.warning(f"Artifact not found: {artifact_id}")
            return None
        
        return artifact
    
    def store(self, artifact_id: str, title: str, content: str,
             artifact_type: str = "document", category: str = None,
             summary: str = None, source: str = None,
             source_url: str = None, tags: List[str] = None,
             metadata: Dict = None, auto_embed: bool = True) -> bool:
        """
        Store a new artifact in Canon
        
        Args:
            artifact_id: Unique ID
            title: Human-readable title
            content: Full content
            artifact_type: "decision", "context", "brief", "log", etc.
            category: "product", "growth", "operations", "finance"
            summary: Brief summary (for search results)
            source: Where this came from
            source_url: Link to original
            tags: List of tags
            metadata: Additional JSON metadata
            auto_embed: Automatically generate embedding (default True)
        
        Returns: True if successful
        """
        logger.info(f"Canon store: {artifact_id} ({artifact_type})")
        
        # Store artifact
        success = self.canon.store_artifact(
            artifact_id=artifact_id,
            title=title,
            content=content,
            artifact_type=artifact_type,
            category=category,
            summary=summary,
            source=source,
            source_url=source_url,
            tags=tags,
            metadata=metadata
        )
        
        # Generate embedding if semantic search enabled
        if success and auto_embed and self.embeddings:
            try:
                artifact_text = f"{title}\n{summary or ''}\n{content}"
                embed_success = self.embeddings.embed_artifact(artifact_id, artifact_text)
                if embed_success:
                    logger.info(f"Generated embedding for {artifact_id}")
                else:
                    logger.warning(f"Failed to generate embedding for {artifact_id}")
            except Exception as e:
                logger.error(f"Embedding generation failed: {e}")
        
        return success
    
    def list(self, artifact_type: str = None, category: str = None,
            limit: int = 50) -> List[Dict]:
        """
        List artifacts, optionally filtered
        
        Args:
            artifact_type: Filter by type
            category: Filter by category
            limit: Max results
        
        Returns: List of artifact summaries
        """
        logger.info(f"Canon list: type={artifact_type}, category={category}")
        
        return self.canon.list_artifacts(
            artifact_type=artifact_type,
            category=category,
            limit=limit
        )
    
    def get_related(self, artifact_id: str) -> List[Dict]:
        """
        Get artifacts related to a given artifact
        
        Args:
            artifact_id: Artifact ID
        
        Returns: List of related artifacts
        """
        logger.info(f"Canon get_related: {artifact_id}")
        
        return self.canon.get_related_artifacts(artifact_id)
    
    def link(self, source_id: str, target_id: str,
            relationship_type: str = "related") -> bool:
        """
        Link two artifacts (build knowledge graph)
        
        Args:
            source_id: Source artifact ID
            target_id: Target artifact ID
            relationship_type: Type of relationship
        
        Returns: True if successful
        """
        logger.info(f"Canon link: {source_id} → {target_id} ({relationship_type})")
        
        return self.canon.link_artifacts(
            source_id=source_id,
            target_id=target_id,
            relationship_type=relationship_type
        )
    
    def approve(self, artifact_id: str, approver: str = "founder") -> bool:
        """
        Approve an artifact (change status from draft to approved)
        
        Args:
            artifact_id: Artifact ID
            approver: Who approved (for audit)
        
        Returns: True if successful
        """
        logger.info(f"Canon approve: {artifact_id} (by {approver})")
        
        return self.canon.approve_artifact(artifact_id, approver)
    
    def stats(self) -> Dict[str, Any]:
        """
        Get Canon Index statistics
        
        Returns:
        {
            "total_artifacts": int,
            "by_type": {type: count},
            "by_category": {category: count},
            "total_retrievals": int,
            "embeddings": {
                "total_embeddings": int,
                "missing_embeddings": int,
                "embedding_model": str
            }
        }
        """
        logger.info("Canon stats requested")
        
        stats = self.canon.get_stats()
        
        # Add embeddings stats if available
        if self.embeddings:
            stats["embeddings"] = self.embeddings.get_stats()
        
        return stats
    
    def reindex_embeddings(self) -> Dict[str, int]:
        """
        Regenerate embeddings for all artifacts
        
        Use this when:
        - Switching to semantic search for first time
        - After bulk importing artifacts
        - After changing embedding model
        
        Returns: {total, success, failed}
        """
        if not self.embeddings:
            logger.error("Semantic search not enabled")
            return {"total": 0, "success": 0, "failed": 0}
        
        logger.info("Reindexing all embeddings")
        return self.embeddings.reindex_all(self.canon)


# Helper function to create CanonTools
def create_canon_tools(canon_db_path: str = "canon.db", 
                      use_semantic_search: bool = True,
                      openai_api_key: str = None) -> CanonTools:
    """
    Factory function to create CanonTools
    
    Args:
        canon_db_path: Path to Canon SQLite database
        use_semantic_search: Enable semantic search (requires OpenAI API key)
        openai_api_key: OpenAI API key for embeddings
    """
    canon_index = CanonIndex(db_path=canon_db_path)
    return CanonTools(
        canon_index=canon_index,
        canon_db_path=canon_db_path,
        use_semantic_search=use_semantic_search,
        openai_api_key=openai_api_key
    )
