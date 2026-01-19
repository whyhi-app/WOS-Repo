"""
WOS Approval Gate v0
Human-in-the-loop approval enforcement
Implements Phase 3.2 HITL policy
"""

import logging
import uuid
from datetime import datetime
from typing import Dict, Any, Optional

logger = logging.getLogger("wos.approval_gate")

class ApprovalGate:
    """
    Approval Gate v0
    
    Routes requests requiring approval to human review.
    For v0, this is a stub that can be extended for HITL via Notion wait gates.
    """
    
    def __init__(self, notion_db_id=None, notion_api_key=None):
        """
        Initialize approval gate

        Args:
            notion_db_id: Notion database ID for approval tracking
            notion_api_key: Notion API key for authentication
        """
        self.notion_db_id = notion_db_id
        self.notion_api_key = notion_api_key
        # TODO: Initialize Notion client if credentials provided
        self.approval_storage = None  # Placeholder for future Notion integration
    
    def check_approval(self, request_id: str, intent_id: str, 
                      intent_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if approval is available or required
        
        Returns:
        {
            "approved": bool,
            "approval_id": str (if pending),
            "reason": str
        }
        """
        
        # V0: Check if approval already exists for this request
        approval_id = str(uuid.uuid4())
        
        # For v0, always return "not approved" which triggers HITL
        return {
            "approved": False,
            "approval_required": True,
            "approval_id": approval_id,
            "reason": "Awaiting human approval (HITL gate)",
            "intent_input": intent_input,
            "created_at": datetime.utcnow().isoformat()
        }
    
    def get_approval_status(self, approval_id: str) -> Optional[Dict]:
        """Check status of an approval request"""
        # TODO: Query approval_storage
        return None
    
    def approve_request(self, approval_id: str, approver: str) -> bool:
        """Mark a request as approved"""
        # TODO: Update approval_storage
        logger.info(f"Request {approval_id} approved by {approver}")
        return True
    
    def reject_request(self, approval_id: str, approver: str, reason: str) -> bool:
        """Mark a request as rejected"""
        # TODO: Update approval_storage
        logger.info(f"Request {approval_id} rejected by {approver}: {reason}")
        return True
