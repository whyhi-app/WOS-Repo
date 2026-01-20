"""
Add "Sending Email" select field to Approval Queue
Allows specifying which Gmail account should send the approved message
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

notion_api_key = os.getenv("NOTION_API_KEY")
notion_approval_db_id = os.getenv("NOTION_APPROVAL_DB_ID")

headers = {
    "Authorization": f"Bearer {notion_api_key}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

print("Adding 'Sending Email' field to Approval Queue...")

response = requests.patch(
    f"https://api.notion.com/v1/databases/{notion_approval_db_id}",
    headers=headers,
    json={
        "properties": {
            "Sending Email": {
                "select": {
                    "options": [
                        {"name": "tom@whyhi.app", "color": "blue"},
                        {"name": "admin@whyhi.app", "color": "gray"},
                        {"name": "hello@whyhi.app", "color": "green"}
                    ]
                }
            }
        }
    }
)

if response.status_code == 200:
    print("✅ 'Sending Email' field added successfully")
    print()
    print("Options:")
    print("  - tom@whyhi.app (blue) - Personal outreach")
    print("  - admin@whyhi.app (gray) - Operations/automation")
    print("  - hello@whyhi.app (green) - Public marketing")
    print()
    print("Default for creator outreach: tom@whyhi.app")
else:
    print(f"❌ Failed to add field: {response.status_code}")
    print(f"   Error: {response.text}")
