"""
Content Idea Miner Intent Handler v1.0
Analyzes captured content and generates 2-5 content ideas using Canon references
Part of COS (Content Operating System) Phase 2
"""

import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional, List
from notion_client import Client as NotionClient
from anthropic import Anthropic

from ..artifact_publisher import ArtifactPublisher

logger = logging.getLogger("wos.intent_handlers.content_idea_miner")

class ContentIdeaMinerHandler:
    """
    Content Idea Miner Handler v1.0

    Workflow:
    1. Query Content & Creator Capture DB for entries with "Sent to COS" status
    2. Load Canon documents (Brand Foundation + Content Playbook)
    3. For each entry, generate 2-5 content ideas using Claude
    4. Create entries in Content Ideas Queue database
    5. Update original entry to "Ideas Generated" status
    6. Publish artifact with ideation log
    """

    def __init__(self):
        """Initialize handler with Notion, Claude, and Artifact Publisher"""
        self.notion_api_key = os.getenv("NOTION_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

        # Database IDs
        self.content_capture_db_id = "edbf92f3-d884-478a-a27e-11d1c6c929ca"
        self.ideas_queue_db_id = "dae2c9d9-83ce-46b4-be71-f057c0dc5230"

        if not self.notion_api_key:
            raise ValueError("NOTION_API_KEY environment variable required")
        if not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable required")

        self.notion = NotionClient(auth=self.notion_api_key)
        self.anthropic = Anthropic(api_key=self.anthropic_api_key)
        self.artifact_publisher = ArtifactPublisher()

        # Load Canon documents
        self._load_canon()

    def _load_canon(self):
        """Load Canon documents for AI context"""
        canon_dir = os.path.join(os.path.dirname(__file__), "../../../canon")

        try:
            # Load Brand Foundation
            with open(os.path.join(canon_dir, "brand_foundation.md"), "r") as f:
                self.brand_foundation = f.read()

            # Load Content Playbook
            with open(os.path.join(canon_dir, "cos_content_playbook.md"), "r") as f:
                self.content_playbook = f.read()

            logger.info("Canon documents loaded successfully")

        except Exception as e:
            logger.error(f"Failed to load Canon documents: {e}")
            raise

    def execute(self, request_id: str, intent_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute content ideation

        Args:
            request_id: WOS request ID
            intent_input: {
                "limit": int (default 5),
                "min_relevance_score": int (default 3),
                "dry_run": bool (default False)
            }

        Returns:
            {
                "success": bool,
                "entries_processed": int,
                "ideas_generated": int,
                "artifact_uri": str
            }
        """

        logger.info(f"Starting content idea mining (request_id={request_id})")

        # Extract parameters
        limit = intent_input.get("limit", 5)
        min_relevance_score = intent_input.get("min_relevance_score", 3)
        dry_run = intent_input.get("dry_run", False)

        # Step 1: Query for entries ready for ideation
        entries = self._query_content_capture(limit, min_relevance_score)

        if not entries:
            logger.info("No entries found with status 'Sent to COS'")
            return {
                "success": True,
                "entries_processed": 0,
                "ideas_generated": 0,
                "message": "No entries ready for ideation"
            }

        logger.info(f"Found {len(entries)} entries ready for ideation")

        # Step 2: Generate ideas for each entry
        ideation_log = []
        total_ideas_created = 0

        for entry in entries:
            try:
                # Generate ideas using Claude
                ideas = self._generate_ideas(entry)

                if not dry_run:
                    # Create entries in Ideas Queue
                    for idea in ideas:
                        self._create_idea_entry(idea, entry)

                    # Update original entry status
                    self._update_capture_status(entry["page_id"], "Ideas Generated")

                    total_ideas_created += len(ideas)

                ideation_log.append({
                    "content_name": entry["name"],
                    "content_url": entry["url"],
                    "platform": entry["platform"],
                    "topic_tags": entry["topic_tags"],
                    "relevance_score": entry["relevance_score"],
                    "ideas_count": len(ideas),
                    "ideas": ideas,
                    "status": "success"
                })

                logger.info(f"Generated {len(ideas)} ideas for '{entry['name']}'")

            except Exception as e:
                logger.error(f"Failed to process entry '{entry.get('name', 'unknown')}': {e}")
                ideation_log.append({
                    "content_name": entry.get("name", "unknown"),
                    "status": "error",
                    "error": str(e)
                })

        # Step 3: Publish ideation log as artifact
        artifact_markdown = self._format_ideation_log(ideation_log)

        artifact = self.artifact_publisher.publish_daily_artifact(
            markdown=artifact_markdown,
            category="ideation",
            filename_prefix="content_ideas",
            title=f"Content Ideation Log - {datetime.now().strftime('%Y-%m-%d')}",
            artifact_type="ideation_log",
            summary=f"Generated {total_ideas_created} ideas from {len(entries)} captured content pieces",
            tags=["content_ideation", "cos", "ideas"],
            metadata={
                "limit": limit,
                "min_relevance_score": min_relevance_score,
                "dry_run": dry_run,
                "entries_processed": len(entries),
                "ideas_generated": total_ideas_created
            }
        )

        logger.info(f"Content ideation complete: {total_ideas_created} ideas from {len(entries)} entries")

        return {
            "success": True,
            "entries_processed": len(entries),
            "ideas_generated": total_ideas_created,
            "artifact_uri": artifact["artifact_uri"]
        }

    def _query_content_capture(self, limit: int, min_relevance_score: int) -> List[Dict[str, Any]]:
        """
        Query Content & Creator Capture for entries ready for ideation

        Args:
            limit: Maximum number of entries to return
            min_relevance_score: Minimum relevance score filter

        Returns:
            List of entry dictionaries with extracted properties
        """
        try:
            # Build filter - "Sent to COS" status AND has Content Ideation action type
            filter_conditions = {
                "and": [
                    {
                        "property": "Ideation Status",
                        "select": {
                            "equals": "Sent to COS"
                        }
                    },
                    {
                        "property": "Action Type",
                        "multi_select": {
                            "contains": "💡 Content Ideation"
                        }
                    }
                ]
            }

            # Add relevance score filter if specified
            if min_relevance_score > 0:
                filter_conditions["and"].append({
                    "property": "Relevance Score",
                    "number": {
                        "greater_than_or_equal_to": min_relevance_score
                    }
                })

            response = self.notion.databases.query(
                database_id=self.content_capture_db_id,
                filter=filter_conditions,
                page_size=limit,
                sorts=[
                    {
                        "property": "Relevance Score",
                        "direction": "descending"
                    }
                ]
            )

            entries = []
            for page in response["results"]:
                entry = self._extract_entry_from_page(page)
                if entry:
                    entries.append(entry)

            return entries

        except Exception as e:
            logger.error(f"Failed to query Content Capture: {e}")
            return []

    def _extract_entry_from_page(self, page: Dict) -> Optional[Dict[str, Any]]:
        """Extract content data from Notion page"""
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

            # Extract multi-select values
            def get_multi_select(prop):
                if not prop or prop["type"] != "multi_select":
                    return []
                return [item["name"] for item in prop["multi_select"]]

            # Extract number
            def get_number(prop):
                if not prop or prop["type"] != "number":
                    return 0
                return prop["number"] or 0

            return {
                "page_id": page["id"],
                "name": get_text(props.get("Name")),
                "url": get_text(props.get("URL")),
                "platform": get_text(props.get("Platform")),
                "content_notes": get_text(props.get("Content Notes")),
                "notes": get_text(props.get("Notes")),
                "topic_tags": get_multi_select(props.get("Topic Tags")),
                "relevance_score": get_number(props.get("Relevance Score"))
            }

        except Exception as e:
            logger.error(f"Failed to extract entry from page: {e}")
            return None

    def _generate_ideas(self, entry: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate 2-5 content ideas using Claude API

        Args:
            entry: Content entry with URL, platform, notes, topic tags, etc.

        Returns:
            List of idea dictionaries with title, angle, platform, format
        """

        # Build the ideation prompt
        prompt = f"""You are the Content Idea Miner for WhyHi's Content Operating System (COS).

Your job: Analyze captured content and generate 2-5 content ideas that align with WhyHi's brand and resonate with our target audiences.

## CAPTURED CONTENT

**Source:** {entry['name']}
**URL:** {entry['url']}
**Platform:** {entry['platform']}
**User Notes:** {entry['content_notes']}
**Topic Tags:** {', '.join(entry['topic_tags']) if entry['topic_tags'] else 'None'}
**Relevance Score:** {entry['relevance_score']}/5

---

## YOUR CANON REFERENCES

### BRAND FOUNDATION
{self.brand_foundation}

---

### CONTENT PLAYBOOK
{self.content_playbook}

---

## INSTRUCTIONS

1. **Analyze the captured content** based on the URL, platform, and user notes
2. **Generate 2-5 content ideas** that:
   - Apply one of the writing formulas from the Content Playbook
   - Target one of WhyHi's core audiences (Busy Professionals, Telephobia community, etc.)
   - Use a relatable scenario from the Use Case Library
   - Follow WhyHi's voice guardrails (conversational, supportive, never salesy)
   - Are platform-specific (LinkedIn = professional, Instagram = visual, etc.)

3. **For each idea, provide:**
   - **Title:** Clear, concise title (5-10 words)
   - **Angle:** The writing formula or angle being used (e.g., "Use Case Spotlight", "Hidden Cost")
   - **Target Audience:** Which audience segment this resonates with
   - **Content Hook:** The first 1-2 sentences that grab attention
   - **Platform:** Best platform for this idea (LinkedIn, Instagram, Facebook, Twitter/X, TikTok)
   - **Format:** Content format (Text post, Carousel, Video, Reel, Thread, etc.)
   - **Why It Works:** 1-2 sentences explaining why this idea aligns with WhyHi's brand

## OUTPUT FORMAT

Return your ideas as a JSON array:

```json
[
  {{
    "title": "When Your Best Friend Only Texts",
    "angle": "Hidden Cost",
    "target_audience": "Friendship Maintainers",
    "content_hook": "You text your best friend every day, but haven't heard their voice in months. When did staying close become so distant?",
    "platform": "Instagram",
    "format": "Carousel",
    "why_it_works": "Uses emotional contrast to highlight the hidden cost of text-only friendships. Relatable scenario that positions WhyHi as the solution without being salesy."
  }}
]
```

Generate 2-5 high-quality ideas now:"""

        try:
            # Call Claude API
            response = self.anthropic.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                temperature=0.7,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # Extract JSON from response
            import json
            import re

            content = response.content[0].text

            # Try to extract JSON array from response
            json_match = re.search(r'\[[\s\S]*\]', content)
            if json_match:
                ideas_json = json.loads(json_match.group())
                logger.info(f"Generated {len(ideas_json)} ideas")
                return ideas_json
            else:
                logger.error("No JSON array found in Claude response")
                return []

        except Exception as e:
            logger.error(f"Failed to generate ideas: {e}")
            return []

    def _create_idea_entry(self, idea: Dict[str, Any], source_entry: Dict[str, Any]):
        """
        Create entry in Content Ideas Queue database

        Args:
            idea: Generated idea dictionary
            source_entry: Original captured content entry
        """
        try:
            self.notion.pages.create(
                parent={"database_id": self.ideas_queue_db_id},
                properties={
                    "Title": {
                        "title": [{"text": {"content": idea["title"]}}]
                    },
                    "Angle": {
                        "select": {"name": idea["angle"]}
                    },
                    "Target Audience": {
                        "select": {"name": idea["target_audience"]}
                    },
                    "Content Hook": {
                        "rich_text": [{"text": {"content": idea["content_hook"]}}]
                    },
                    "Platform": {
                        "select": {"name": idea["platform"]}
                    },
                    "Format": {
                        "select": {"name": idea["format"]}
                    },
                    "Why It Works": {
                        "rich_text": [{"text": {"content": idea["why_it_works"]}}]
                    },
                    "Status": {
                        "select": {"name": "Proposed"}
                    },
                    "Source Content": {
                        "relation": [{"id": source_entry["page_id"]}]
                    }
                }
            )

            logger.info(f"Created idea entry: {idea['title']}")

        except Exception as e:
            logger.error(f"Failed to create idea entry: {e}")
            raise

    def _update_capture_status(self, page_id: str, new_status: str):
        """Update Ideation Status in Content & Creator Capture"""
        try:
            self.notion.pages.update(
                page_id=page_id,
                properties={
                    "Ideation Status": {
                        "select": {"name": new_status}
                    }
                }
            )
            logger.info(f"Updated ideation status to '{new_status}'")

        except Exception as e:
            logger.error(f"Failed to update ideation status: {e}")

    def _format_ideation_log(self, ideation_log: List[Dict]) -> str:
        """Format ideation log as markdown"""

        markdown = f"""# Content Ideation Log

**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Entries Processed:** {len(ideation_log)}
**Total Ideas Generated:** {sum(entry.get('ideas_count', 0) for entry in ideation_log)}

---

"""

        for entry in ideation_log:
            markdown += f"## {entry['content_name']}\n\n"
            markdown += f"**URL:** {entry.get('content_url', 'N/A')}\n"
            markdown += f"**Platform:** {entry.get('platform', 'N/A')}\n"
            markdown += f"**Topic Tags:** {', '.join(entry.get('topic_tags', [])) if entry.get('topic_tags') else 'None'}\n"
            markdown += f"**Relevance Score:** {entry.get('relevance_score', 0)}/5\n"
            markdown += f"**Status:** {entry['status']}\n"

            if entry['status'] == 'success':
                markdown += f"**Ideas Generated:** {entry['ideas_count']}\n\n"

                for i, idea in enumerate(entry.get('ideas', []), 1):
                    markdown += f"### Idea {i}: {idea['title']}\n\n"
                    markdown += f"- **Angle:** {idea['angle']}\n"
                    markdown += f"- **Target Audience:** {idea['target_audience']}\n"
                    markdown += f"- **Platform:** {idea['platform']}\n"
                    markdown += f"- **Format:** {idea['format']}\n"
                    markdown += f"- **Content Hook:** {idea['content_hook']}\n"
                    markdown += f"- **Why It Works:** {idea['why_it_works']}\n\n"

            elif 'error' in entry:
                markdown += f"\n**Error:** {entry['error']}\n"

            markdown += "\n---\n\n"

        return markdown


def create_handler(n8n_executor=None, **kwargs):
    """Factory function for handler registration"""
    # n8n_executor not needed for this handler
    return ContentIdeaMinerHandler()
