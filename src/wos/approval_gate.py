"""
WOS Approval Gate v0.2
Human-in-the-loop approval enforcement via Notion
Implements Phase 3.2 HITL policy + Sprint 1 Notion integration
"""

import logging
import uuid
import os
import time
import requests
from datetime import datetime
from typing import Dict, Any, Optional

logger = logging.getLogger("wos.approval_gate")

class ApprovalGate:
    """
    Approval Gate v0.2 with Notion Integration

    Routes requests requiring approval to human review via Notion database.

    Workflow:
    1. Agent calls request_approval() → Creates Notion page (status: Pending)
    2. Human reviews in Notion → Changes status to Approved/Rejected
    3. Agent calls wait_for_approval() → Polls Notion until status changes
    4. Agent proceeds (approved) or stops (rejected)
    """

    def __init__(self, notion_api_key=None, notion_db_id=None):
        """
        Initialize approval gate

        Args:
            notion_api_key: Notion API key (or set NOTION_API_KEY env var)
            notion_db_id: Notion approval queue database ID (or set NOTION_APPROVAL_DB_ID env var)
        """
        self.notion_api_key = notion_api_key or os.getenv("NOTION_API_KEY")
        self.notion_db_id = notion_db_id or os.getenv("NOTION_APPROVAL_DB_ID")

        if not self.notion_api_key:
            logger.warning("Notion API key not provided - approval gate will not work")

        self.notion_version = "2022-06-28"  # Notion API version
        self.base_url = "https://api.notion.com/v1"

    def _notion_request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """Make a request to Notion API"""
        headers = {
            "Authorization": f"Bearer {self.notion_api_key}",
            "Content-Type": "application/json",
            "Notion-Version": self.notion_version
        }

        url = f"{self.base_url}/{endpoint}"

        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method == "PATCH":
            response = requests.patch(url, headers=headers, json=data)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        response.raise_for_status()
        return response.json()

    def request_approval(
        self,
        request_id: str,
        intent_id: str,
        content: str,
        title: str = None,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Create an approval request in Notion

        Args:
            request_id: WOS request ID
            intent_id: Intent being executed
            content: Draft content requiring approval (markdown)
            title: Human-readable title for the approval
            metadata: Additional context (JSON)

        Returns:
        {
            "approval_id": str (Notion page ID),
            "status": "pending",
            "notion_url": str,
            "created_at": str
        }
        """

        if not self.notion_api_key or not self.notion_db_id:
            raise ValueError("Notion API key and database ID required for approval requests")

        # Auto-generate title if not provided
        if not title:
            title = f"{intent_id} - {request_id[:8]}"

        # Create Notion page
        page_data = {
            "parent": {"database_id": self.notion_db_id},
            "properties": {
                "Name": {
                    "title": [{"text": {"content": title}}]
                },
                "Status": {
                    "select": {"name": "Pending"}
                },
                "Request ID": {
                    "rich_text": [{"text": {"content": request_id}}]
                },
                "Intent": {
                    "rich_text": [{"text": {"content": intent_id}}]
                }
            },
            "children": [
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"text": {"content": "Content Requiring Approval"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "code",
                    "code": {
                        "rich_text": [{"text": {"content": content[:2000]}}],  # Notion limit
                        "language": "markdown"
                    }
                }
            ]
        }

        # Add metadata block if provided
        if metadata:
            import json
            page_data["children"].append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"text": {"content": "Metadata"}}]
                }
            })
            page_data["children"].append({
                "object": "block",
                "type": "code",
                "code": {
                    "rich_text": [{"text": {"content": json.dumps(metadata, indent=2)[:2000]}}],
                    "language": "json"
                }
            })

        try:
            result = self._notion_request("POST", "pages", page_data)
            approval_id = result["id"]
            notion_url = result["url"]

            logger.info(f"Approval request created: {approval_id} ({notion_url})")

            return {
                "approval_id": approval_id,
                "status": "pending",
                "notion_url": notion_url,
                "created_at": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Failed to create approval request: {e}")
            raise

    def get_approval_status(self, approval_id: str) -> Optional[Dict]:
        """
        Check status of an approval request

        Args:
            approval_id: Notion page ID

        Returns:
        {
            "approval_id": str,
            "status": "pending" | "approved" | "rejected",
            "reviewed_at": str (if completed),
            "notion_url": str
        }
        """

        if not self.notion_api_key:
            raise ValueError("Notion API key required")

        try:
            page = self._notion_request("GET", f"pages/{approval_id}")

            # Extract status from properties
            status_property = page["properties"].get("Status", {})
            status_value = status_property.get("select", {}).get("name", "pending").lower()

            # Map Notion status to standard values
            if status_value in ["approved", "✅ approved", "approve"]:
                status = "approved"
            elif status_value in ["rejected", "❌ rejected", "reject"]:
                status = "rejected"
            else:
                status = "pending"

            return {
                "approval_id": approval_id,
                "status": status,
                "reviewed_at": page.get("last_edited_time"),
                "notion_url": page["url"]
            }

        except Exception as e:
            logger.error(f"Failed to get approval status: {e}")
            return None

    def wait_for_approval(
        self,
        approval_id: str,
        timeout_seconds: int = 3600,
        poll_interval: int = 10
    ) -> Dict[str, Any]:
        """
        Wait for approval (blocking poll)

        Args:
            approval_id: Notion page ID
            timeout_seconds: Max time to wait (default 1 hour)
            poll_interval: Seconds between polls (default 10s)

        Returns:
        {
            "approved": bool,
            "status": "approved" | "rejected" | "timeout",
            "reviewed_at": str
        }
        """

        logger.info(f"Waiting for approval: {approval_id} (timeout={timeout_seconds}s)")

        start_time = time.time()

        while True:
            # Check if timeout exceeded
            elapsed = time.time() - start_time
            if elapsed > timeout_seconds:
                logger.warning(f"Approval timeout: {approval_id}")
                return {
                    "approved": False,
                    "status": "timeout",
                    "reviewed_at": None
                }

            # Check current status
            status_result = self.get_approval_status(approval_id)

            if not status_result:
                logger.error(f"Failed to get status for {approval_id}")
                time.sleep(poll_interval)
                continue

            status = status_result["status"]

            if status == "approved":
                logger.info(f"Approval granted: {approval_id}")
                return {
                    "approved": True,
                    "status": "approved",
                    "reviewed_at": status_result["reviewed_at"]
                }

            elif status == "rejected":
                logger.info(f"Approval rejected: {approval_id}")
                return {
                    "approved": False,
                    "status": "rejected",
                    "reviewed_at": status_result["reviewed_at"]
                }

            # Still pending - wait and poll again
            logger.debug(f"Approval pending: {approval_id} ({int(elapsed)}s elapsed)")
            time.sleep(poll_interval)

    def check_approval(self, request_id: str, intent_id: str,
                      intent_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Legacy method for backward compatibility

        Returns:
        {
            "approved": bool,
            "approval_required": bool,
            "approval_id": str,
            "reason": str
        }
        """

        # For now, always require approval (agents should call request_approval() explicitly)
        approval_id = str(uuid.uuid4())

        return {
            "approved": False,
            "approval_required": True,
            "approval_id": approval_id,
            "reason": "Awaiting human approval (HITL gate)",
            "intent_input": intent_input,
            "created_at": datetime.utcnow().isoformat()
        }
