"""
Add "Completed" status option to Approval Queue database
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

print("Adding 'Completed' status to Approval Queue...")

# Get current database schema
response = requests.get(
    f"https://api.notion.com/v1/databases/{notion_approval_db_id}",
    headers=headers
)

if response.status_code != 200:
    print(f"❌ Failed to get database: {response.status_code}")
    exit(1)

db = response.json()
status_property = db["properties"]["Status"]

# Check if Completed already exists
current_options = status_property["select"]["options"]
if any(opt["name"] == "Completed" for opt in current_options):
    print("✅ 'Completed' status already exists")
    exit(0)

# Add Completed option
new_options = current_options + [{"name": "Completed", "color": "blue"}]

response = requests.patch(
    f"https://api.notion.com/v1/databases/{notion_approval_db_id}",
    headers=headers,
    json={
        "properties": {
            "Status": {
                "select": {
                    "options": new_options
                }
            }
        }
    }
)

if response.status_code == 200:
    print("✅ 'Completed' status added successfully")
    print()
    print("Status options now:")
    print("  - Pending (yellow)")
    print("  - Approved (green)")
    print("  - Rejected (red)")
    print("  - Completed (blue)")
else:
    print(f"❌ Failed to update database: {response.status_code}")
    print(f"   Error: {response.text}")
