"""
Add test creators to CRM for Creator Outreach testing
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

notion_api_key = os.getenv("NOTION_API_KEY")
notion_crm_db_id = "23d632f5307e8001a1d6fb31be92d59e"

print(f"API Key loaded: {notion_api_key[:20] if notion_api_key else 'NOT FOUND'}...")
print(f"Database ID: {notion_crm_db_id}\n")

headers = {
    "Authorization": f"Bearer {notion_api_key}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Test creators
test_creators = [
    {
        "name": "@techcrunch",
        "url": "https://twitter.com/techcrunch/status/12345",
        "platform": "Twitter",
        "contact_method": "Twitter DM",
        "notes": "Posted about voice-first social apps last week"
    },
    {
        "name": "Sarah Chen",
        "url": "https://www.theverge.com/tech/voice-social-apps",
        "email": "sarah.chen@theverge.com",
        "company": "The Verge",
        "platform": "Article",
        "contact_method": "Email",
        "notes": "Covers social media innovation"
    }
]

print("Adding test creators to CRM...\n")

for creator in test_creators:
    try:
        properties = {
            "Name": {
                "title": [{"text": {"content": creator["name"]}}]
            },
            "URL": {
                "url": creator["url"]  # URL field type
            },
            "Contact Method": {
                "rich_text": [{"text": {"content": creator["contact_method"]}}]
            },
            "Notes": {
                "rich_text": [{"text": {"content": creator["notes"]}}]
            },
            "Outreach Status": {
                "select": {"name": "Draft Ready"}
            }
        }

        # Add email if present
        if "email" in creator:
            properties["Email"] = {
                "email": creator["email"]  # Email field type
            }

        # Add company if present
        if "company" in creator:
            properties["Company"] = {
                "rich_text": [{"text": {"content": creator["company"]}}]
            }

        response = requests.post(
            "https://api.notion.com/v1/pages",
            headers=headers,
            json={
                "parent": {"database_id": notion_crm_db_id},
                "properties": properties
            }
        )

        if response.status_code != 200:
            print(f"❌ Failed to add {creator['name']}: {response.status_code}")
            print(f"   Error: {response.text}")
            continue

        print(f"✅ Added: {creator['name']} ({creator['platform']})")

    except Exception as e:
        print(f"❌ Failed to add {creator['name']}: {e}")
        import traceback
        traceback.print_exc()

print("\n✅ Test creators added! Ready to test Creator Outreach.")
