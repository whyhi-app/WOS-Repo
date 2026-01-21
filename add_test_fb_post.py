"""
Add Tom's test Facebook post to CRM
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

notion_api_key = os.getenv("NOTION_API_KEY")
notion_crm_db_id = "23d632f5307e8001a1d6fb31be92d59e"

headers = {
    "Authorization": f"Bearer {notion_api_key}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

print("Adding Tom's Facebook test post to CRM...")

# Create CRM entry
properties = {
    "Name": {
        "title": [{"text": {"content": "Tom Wynn (Test)"}}]
    },
    "URL": {
        "url": "https://www.facebook.com/share/r/1C9VdYceA9/?mibextid=wwXIfr"
    },
    "Email": {
        "email": "wynntom@gmail.com"
    },
    "Contact Method": {
        "rich_text": [{"text": {"content": "Facebook DM"}}]
    },
    "Notes": {
        "rich_text": [{"text": {"content": "Test FB post for DM outreach workflow"}}]
    },
    "Outreach Status": {
        "select": {"name": "Draft Ready"}
    }
}

response = requests.post(
    "https://api.notion.com/v1/pages",
    headers=headers,
    json={
        "parent": {"database_id": notion_crm_db_id},
        "properties": properties
    }
)

if response.status_code == 200:
    print("✅ Added to CRM!")
    print()
    print("Details:")
    print("  Name: Tom Wynn (Test)")
    print("  Platform: Facebook")
    print("  Contact Method: Facebook DM")
    print("  Status: Draft Ready")
    print()
    print("Ready to generate DM-style outreach!")
else:
    print(f"❌ Failed: {response.status_code}")
    print(f"   Error: {response.text}")
