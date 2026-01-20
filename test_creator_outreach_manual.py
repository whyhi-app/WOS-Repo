"""
Manual test of Creator Outreach workflow
Simulates what the handler does
"""

import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

notion_api_key = os.getenv("NOTION_API_KEY")
notion_approval_db_id = os.getenv("NOTION_APPROVAL_DB_ID")

headers = {
    "Authorization": f"Bearer {notion_api_key}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Simulate outreach message for @techcrunch
outreach_message = """Hey TechCrunch team!

I saw your post: https://twitter.com/techcrunch/status/12345

I'm building WhyHi - a voice-first social app launching in March (no feeds, no likes, just real conversations).

Thought you might vibe with what we're doing. Would love to get your thoughts or have you try it early.

Interested?

- Tom
Founder @ WhyHi"""

print("Creating approval request for @techcrunch outreach...")
print()

# Create approval page
page_data = {
    "parent": {"database_id": notion_approval_db_id},
    "properties": {
        "Name": {
            "title": [{"text": {"content": "Outreach to @techcrunch (Twitter)"}}]
        },
        "Status": {
            "select": {"name": "Pending"}
        },
        "Request ID": {
            "rich_text": [{"text": {"content": "test-creator-outreach-001"}}]
        },
        "Intent": {
            "rich_text": [{"text": {"content": "creator_outreach_v0"}}]
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
                "rich_text": [{"text": {"content": outreach_message}}],
                "language": "markdown"
            }
        },
        {
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{"text": {"content": "Metadata"}}]
            }
        },
        {
            "object": "block",
            "type": "code",
            "code": {
                "rich_text": [{"text": {"content": '''{\n  "creator_name": "@techcrunch",\n  "platform": "Twitter",\n  "contact_method": "Twitter DM",\n  "original_url": "https://twitter.com/techcrunch/status/12345"\n}'''}}],
                "language": "json"
            }
        }
    ]
}

response = requests.post(
    "https://api.notion.com/v1/pages",
    headers=headers,
    json=page_data
)

if response.status_code == 200:
    result = response.json()
    approval_url = result["url"]
    approval_id = result["id"]

    print(f"✅ Approval created!")
    print(f"   Approval ID: {approval_id[:20]}...")
    print(f"   Notion URL: {approval_url}")
    print()
    print("=" * 60)
    print("NEXT STEPS:")
    print("=" * 60)
    print()
    print("1. Open the approval in Notion (URL above)")
    print("2. Review the outreach message")
    print("3. Change Status from 'Pending' to 'Approved' or 'Rejected'")
    print()
    print("This simulates what happens when you run:")
    print("  ~/.local/bin/claude \"execute the creator_outreach intent\"")
    print()
    print("The real workflow would:")
    print("  - Query CRM for 'Draft Ready' creators")
    print("  - Generate personalized messages for each")
    print("  - Create approval requests like this")
    print("  - Wait for you to approve/reject")
    print("  - Update CRM status to 'Outreach Sent' if approved")
    print()
else:
    print(f"❌ Failed to create approval: {response.status_code}")
    print(f"   Error: {response.text}")
