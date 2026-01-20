"""
Update Sarah Chen's email for testing
"""

import os
import sys
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

# Get test email from command line
if len(sys.argv) < 2:
    print("Usage: python3 update_test_creator_email.py YOUR_EMAIL@example.com")
    print()
    print("This will update Sarah Chen's email in the CRM to your email")
    print("so you can test receiving the outreach email.")
    exit(1)

test_email = sys.argv[1]

print(f"Updating Sarah Chen's email to: {test_email}")
print()

# Find Sarah Chen in CRM
response = requests.post(
    f"https://api.notion.com/v1/databases/{notion_crm_db_id}/query",
    headers=headers,
    json={
        "filter": {
            "property": "Name",
            "title": {
                "contains": "Sarah Chen"
            }
        }
    }
)

if response.status_code != 200 or not response.json()["results"]:
    print("❌ Couldn't find Sarah Chen in CRM")
    exit(1)

page_id = response.json()["results"][0]["id"]

# Update email
response = requests.patch(
    f"https://api.notion.com/v1/pages/{page_id}",
    headers=headers,
    json={
        "properties": {
            "Email": {
                "email": test_email
            }
        }
    }
)

if response.status_code == 200:
    print("✅ Email updated successfully!")
    print()
    print("Ready to test:")
    print("1. Generate app password for tom@whyhi.app (see setup_gmail_sending.md)")
    print("2. Add to .env: GMAIL_PASSWORD_TOM=your-app-password")
    print("3. Run: python3 test_creator_outreach_workflow.py")
    print("4. Approve in Notion")
    print("5. Run: python3 process_approved_outreach.py")
    print(f"6. Check {test_email} for the outreach email!")
else:
    print(f"❌ Failed to update email: {response.status_code}")
    print(f"   Error: {response.text}")
