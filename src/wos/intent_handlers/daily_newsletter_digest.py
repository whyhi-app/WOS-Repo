"""
Phase 3.3 Intent Handler: daily_email_digest_v0
Executes daily newsletter digest workflow
Pulls emails, categorizes by WhyHi business relevance, returns digest
"""

import logging
import uuid
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger("wos.intent_handlers.daily_newsletter_digest")

class DailyNewsletterDigestHandler:
    """
    Daily Email Digest Handler v0
    
    Orchestrates the daily newsletter digest workflow:
    1. Fetches emails from Gmail (wynntom@gmail + tom@whyhi.app)
    2. Filters by labels + deduplicates
    3. Extracts content + URLs
    4. Sends to GPT-4.1-mini for categorization
    5. Returns HTML digest categorized by: Product | Growth | Operations | Finance
    6. Emails digest to tom@whyhi.app
    
    Implements Phase 3.1 Acceptance Demo (Daily Newsletter Digest)
    """
    
    def __init__(self, n8n_executor):
        """
        Initialize handler with n8n executor
        
        Args:
            n8n_executor: N8nExecutor instance for calling workflows
        """
        self.n8n_executor = n8n_executor
        self.workflow_name = "Daily_Newsletter_Digest"
    
    def execute(self, request_id: str, execution_id: str, 
                intent_input: Dict[str, Any], 
                intent_record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute daily digest workflow
        
        Args:
            request_id: Request ID from Brain
            execution_id: Unique execution ID
            intent_input: Input parameters (typically empty for daily digest)
            intent_record: Intent definition from registry
        
        Returns:
        {
            "status": "success" | "failed",
            "result": {
                "digest_html": str,
                "email_sent_to": str,
                "categories": {product, growth, operations, finance},
                "execution_time_ms": int
            },
            "error": str (if failed),
            "error_code": str (if failed)
        }
        """
        
        start_time = datetime.utcnow()
        
        try:
            logger.info(f"Executing daily_digest: request_id={request_id}, execution_id={execution_id}")
            
            # Step 1: Call n8n workflow
            # The workflow is already configured in n8n and triggered via webhook
            # We pass through the request/execution IDs for tracking
            
            payload = {
                "request_id": request_id,
                "execution_id": execution_id,
                "triggered_by": "wos_brain",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            n8n_result = self.n8n_executor.execute_workflow(
                workflow_name=self.workflow_name,
                payload=payload,
                timeout_seconds=120  # Digest can take time for GPT processing
            )
            
            execution_time_ms = int(
                (datetime.utcnow() - start_time).total_seconds() * 1000
            )
            
            # Step 2: Parse n8n result
            if n8n_result.get("status") == "failed":
                logger.error(f"n8n workflow failed: {n8n_result.get('error')}")
                return {
                    "status": "failed",
                    "result": None,
                    "error": n8n_result.get("error"),
                    "error_code": "N8N_EXECUTION_FAILED",
                    "execution_time_ms": execution_time_ms
                }
            
            # Step 3: Extract digest from n8n response
            # n8n returns the digest HTML in the response
            n8n_output = n8n_result.get("result", {})
            
            # The workflow sends an email, so the "result" is confirmation
            digest_result = self._parse_digest_result(n8n_output)
            
            logger.info(f"Daily digest completed: {execution_id}")
            
            return {
                "status": "success",
                "result": {
                    "digest_generated": True,
                    "email_sent_to": "tom@whyhi.app",
                    "digest_html": digest_result.get("digest_html", ""),
                    "categories": {
                        "product": digest_result.get("product_count", 0),
                        "growth": digest_result.get("growth_count", 0),
                        "operations": digest_result.get("operations_count", 0),
                        "finance": digest_result.get("finance_count", 0)
                    },
                    "total_emails_processed": digest_result.get("email_count", 0),
                    "execution_id": execution_id,
                    "request_id": request_id
                },
                "error": None,
                "execution_time_ms": execution_time_ms
            }
        
        except Exception as e:
            execution_time_ms = int(
                (datetime.utcnow() - start_time).total_seconds() * 1000
            )
            logger.error(f"daily_digest handler error: {e}", exc_info=True)
            
            return {
                "status": "failed",
                "result": None,
                "error": str(e),
                "error_code": "HANDLER_ERROR",
                "execution_time_ms": execution_time_ms
            }
    
    def _parse_digest_result(self, n8n_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse n8n workflow output to extract digest information
        
        The n8n workflow emails the digest and returns confirmation.
        This method extracts key metrics from the response.
        """
        
        # The workflow's final output contains:
        # - digest_html (from GPT)
        # - email confirmation
        # - packet count
        
        # Best effort parsing of n8n response
        digest_html = ""
        email_count = 0
        
        # Try to extract from n8n response
        if isinstance(n8n_output, dict):
            digest_html = n8n_output.get("digest_html", "") or n8n_output.get("output", "")
            email_count = n8n_output.get("packet_count", 0) or n8n_output.get("count", 0)
        
        # Estimate category counts (rough heuristic)
        # In production, n8n would return actual counts
        categories = {
            "product_count": 0,
            "growth_count": 0,
            "operations_count": 0,
            "finance_count": 0
        }
        
        return {
            "digest_html": digest_html,
            "email_count": email_count,
            **categories
        }
    
    def validate_input(self, intent_input: Dict[str, Any]) -> bool:
        """
        Validate handler input
        
        Daily digest doesn't require specific input - it uses predefined Gmail labels
        and runs on a schedule or on-demand via webhook.
        """
        # No required input for daily digest
        return True


# Handler factory function
def create_daily_newsletter_digest_handler(n8n_executor) -> DailyNewsletterDigestHandler:
    """Factory function to create handler"""
    return DailyNewsletterDigestHandler(n8n_executor)
