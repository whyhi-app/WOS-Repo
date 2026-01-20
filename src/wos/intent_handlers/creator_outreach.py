"""
Creator Outreach Intent Handler v0.1
Generates personalized outreach to creators/journalists with HITL approval
Part of Creator Pipeline (Sprint 1 Foundation Build)
"""

import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional, List
from notion_client import Client as NotionClient

from ..artifact_publisher import ArtifactPublisher
from ..approval_gate import ApprovalGate

logger = logging.getLogger("wos.intent_handlers.creator_outreach")

class CreatorOutreachHandler:
    """
    Creator Outreach Handler v0.1

    Workflow:
    1. Query Notion CRM for creators with specific status
    2. Generate personalized outreach message referencing original content
    3. Request approval via Approval Gate
    4. If approved, mark as "Outreach Sent" in CRM
    5. Publish artifact with outreach log
    """

    def __init__(self):
        """Initialize handler with Notion, Artifact Publisher, and Approval Gate"""
        self.notion_api_key = os.getenv("NOTION_API_KEY")
        self.notion_crm_db_id = "23d632f5307e8001a1d6fb31be92d59e"  # User's CRM database

        if not self.notion_api_key:
            raise ValueError("NOTION_API_KEY environment variable required")

        self.notion = NotionClient(auth=self.notion_api_key)
        self.artifact_publisher = ArtifactPublisher()
        self.approval_gate = ApprovalGate()

    def execute(self, request_id: str, intent_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute creator outreach

        Args:
            request_id: WOS request ID
            intent_input: {
                "status_filter": str (default "Draft Ready"),
                "limit": int (default 5),
                "dry_run": bool (default False),
                "template": str (optional custom template)
            }

        Returns:
            {
                "success": bool,
                "creators_contacted": int,
                "approvals_requested": int,
                "artifact_uri": str
            }
        """

        logger.info(f"Starting creator outreach (request_id={request_id})")

        # Extract parameters
        status_filter = intent_input.get("status_filter", "Draft Ready")
        limit = intent_input.get("limit", 5)
        dry_run = intent_input.get("dry_run", False)
        custom_template = intent_input.get("template")

        # Step 1: Query CRM for creators ready for outreach
        creators = self._query_crm(status_filter, limit)

        if not creators:
            logger.info(f"No creators found with status '{status_filter}'")
            return {
                "success": True,
                "creators_contacted": 0,
                "approvals_requested": 0,
                "message": f"No creators with status '{status_filter}'"
            }

        logger.info(f"Found {len(creators)} creators ready for outreach")

        # Step 2: Generate and approve outreach for each creator
        approvals_requested = 0
        approved_count = 0
        outreach_log = []

        for creator in creators:
            try:
                # Generate personalized message
                message = self._generate_outreach_message(creator, custom_template)

                # Request approval
                approval_title = f"Outreach to {creator['name']} ({creator['platform']})"

                approval = self.approval_gate.request_approval(
                    request_id=request_id,
                    intent_id="creator_outreach_v0",
                    content=message,
                    title=approval_title,
                    metadata={
                        "creator_name": creator["name"],
                        "creator_url": creator["url"],
                        "platform": creator["platform"],
                        "contact_method": creator["contact_method"],
                        "status_filter": status_filter
                    }
                )

                approvals_requested += 1

                logger.info(f"Approval requested for {creator['name']}: {approval['notion_url']}")

                # Wait for approval (10 minute timeout)
                if not dry_run:
                    result = self.approval_gate.wait_for_approval(
                        approval_id=approval["approval_id"],
                        timeout_seconds=600,  # 10 minutes
                        poll_interval=10
                    )

                    if result["status"] == "approved":
                        # Update CRM status to "Outreach Sent"
                        self._update_crm_status(creator["page_id"], "Outreach Sent")
                        approved_count += 1

                        outreach_log.append({
                            "creator": creator["name"],
                            "platform": creator["platform"],
                            "status": "approved",
                            "message": message,
                            "notion_url": approval["notion_url"]
                        })

                        logger.info(f"Outreach approved for {creator['name']}")

                    elif result["status"] == "rejected":
                        outreach_log.append({
                            "creator": creator["name"],
                            "platform": creator["platform"],
                            "status": "rejected",
                            "notion_url": approval["notion_url"]
                        })

                        logger.info(f"Outreach rejected for {creator['name']}")

                    else:
                        # Timeout - don't update status
                        outreach_log.append({
                            "creator": creator["name"],
                            "platform": creator["platform"],
                            "status": "timeout",
                            "notion_url": approval["notion_url"]
                        })

                        logger.warning(f"Approval timeout for {creator['name']}")

                else:
                    # Dry run - just log the approval URL
                    outreach_log.append({
                        "creator": creator["name"],
                        "platform": creator["platform"],
                        "status": "dry_run",
                        "message": message,
                        "notion_url": approval["notion_url"]
                    })

            except Exception as e:
                logger.error(f"Failed to process outreach for {creator.get('name', 'unknown')}: {e}")
                outreach_log.append({
                    "creator": creator.get("name", "unknown"),
                    "status": "error",
                    "error": str(e)
                })

        # Step 3: Publish outreach log as artifact
        artifact_markdown = self._format_outreach_log(outreach_log, status_filter)

        artifact = self.artifact_publisher.publish_daily_artifact(
            markdown=artifact_markdown,
            category="outreach",
            filename_prefix="creator_outreach",
            title=f"Creator Outreach Log - {datetime.now().strftime('%Y-%m-%d')}",
            artifact_type="outreach_log",
            summary=f"Outreach to {len(creators)} creators (status: {status_filter})",
            tags=["creator_outreach", "crm", status_filter.lower().replace(" ", "_")],
            metadata={
                "status_filter": status_filter,
                "limit": limit,
                "dry_run": dry_run,
                "creators_found": len(creators),
                "approvals_requested": approvals_requested,
                "approved_count": approved_count
            }
        )

        logger.info(f"Creator outreach complete: {approved_count}/{approvals_requested} approved")

        return {
            "success": True,
            "creators_contacted": len(creators),
            "approvals_requested": approvals_requested,
            "approved_count": approved_count,
            "artifact_uri": artifact["artifact_uri"]
        }

    def _query_crm(self, status_filter: str, limit: int) -> List[Dict[str, Any]]:
        """
        Query Notion CRM for creators with specific status

        Args:
            status_filter: Outreach Status value to filter by
            limit: Maximum number of creators to return

        Returns:
            List of creator dictionaries with extracted properties
        """
        try:
            # Query Notion database with status filter
            response = self.notion.databases.query(
                database_id=self.notion_crm_db_id,
                filter={
                    "property": "Outreach Status",
                    "select": {
                        "equals": status_filter
                    }
                },
                page_size=limit
            )

            creators = []
            for page in response["results"]:
                creator = self._extract_creator_from_page(page)
                if creator:
                    creators.append(creator)

            return creators

        except Exception as e:
            logger.error(f"Failed to query CRM: {e}")
            return []

    def _extract_creator_from_page(self, page: Dict) -> Optional[Dict[str, Any]]:
        """Extract creator data from Notion page"""
        try:
            props = page["properties"]

            # Helper to extract text
            def get_text(prop):
                if not prop:
                    return ""
                if prop["type"] == "title":
                    return prop["title"][0]["text"]["content"] if prop["title"] else ""
                elif prop["type"] == "rich_text":
                    return prop["rich_text"][0]["text"]["content"] if prop["rich_text"] else ""
                elif prop["type"] == "url":
                    return prop["url"] or ""
                elif prop["type"] == "select":
                    return prop["select"]["name"] if prop["select"] else ""
                return ""

            return {
                "page_id": page["id"],
                "name": get_text(props.get("Name")),
                "url": get_text(props.get("URL")),
                "email": get_text(props.get("Email")),
                "company": get_text(props.get("Company")),
                "contact_method": get_text(props.get("Contact Method")),
                "platform": get_text(props.get("Contact Method")).split()[0] if get_text(props.get("Contact Method")) else "",
                "notes": get_text(props.get("Notes")),
                "status": get_text(props.get("Outreach Status"))
            }

        except Exception as e:
            logger.error(f"Failed to extract creator from page: {e}")
            return None

    def _generate_outreach_message(self, creator: Dict[str, Any], custom_template: str = None) -> str:
        """
        Generate personalized outreach message

        Args:
            creator: Creator data from CRM
            custom_template: Optional custom template string

        Returns:
            Formatted outreach message
        """

        # Use custom template if provided
        if custom_template:
            return custom_template.format(**creator)

        # Default template based on platform
        platform = creator.get("platform", "").lower()
        name = creator.get("name", "").replace("@", "")
        url = creator.get("url", "")
        contact_method = creator.get("contact_method", "DM")

        # Extract first name if possible
        first_name = name.split()[0] if " " in name else name

        # Different templates for journalists vs creators
        if "email" in contact_method.lower() or "article" in platform.lower():
            # Journalist/blogger template (more formal)
            message = f"""Subject: WhyHi - Voice-first social app launching March 2026

Hi {first_name},

I came across your article: {url}

I'm Tom, founder of WhyHi - we're launching a voice-first social app in March that eliminates feeds, likes, and text-first engagement in favor of authentic voice conversations.

Given your coverage of social/tech products, I thought you might be interested in an early look before we go live.

Would you be open to a brief chat or early access?

Best,
Tom Wynn
Founder, WhyHi
tom@whyhi.app"""

        else:
            # Creator/influencer template (more casual DM style)
            message = f"""Hey {first_name}!

I saw your post: {url}

I'm building WhyHi - a voice-first social app launching in March (no feeds, no likes, just real conversations).

Thought you might vibe with what we're doing. Would love to get your thoughts or have you try it early.

Interested?

- Tom
Founder @ WhyHi"""

        return message

    def _update_crm_status(self, page_id: str, new_status: str):
        """Update creator's Outreach Status in Notion CRM"""
        try:
            self.notion.pages.update(
                page_id=page_id,
                properties={
                    "Outreach Status": {
                        "select": {"name": new_status}
                    }
                }
            )
            logger.info(f"Updated creator status to '{new_status}'")

        except Exception as e:
            logger.error(f"Failed to update CRM status: {e}")

    def _format_outreach_log(self, outreach_log: List[Dict], status_filter: str) -> str:
        """Format outreach log as markdown"""

        markdown = f"""# Creator Outreach Log

**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Status Filter:** {status_filter}
**Creators Processed:** {len(outreach_log)}

---

"""

        for entry in outreach_log:
            markdown += f"## {entry['creator']} ({entry.get('platform', 'Unknown')})\n\n"
            markdown += f"**Status:** {entry['status']}\n"

            if "notion_url" in entry:
                markdown += f"**Approval URL:** {entry['notion_url']}\n"

            if "message" in entry:
                markdown += f"\n**Message:**\n```\n{entry['message']}\n```\n"

            if "error" in entry:
                markdown += f"\n**Error:** {entry['error']}\n"

            markdown += "\n---\n\n"

        return markdown


def create_handler():
    """Factory function for handler registration"""
    return CreatorOutreachHandler()
