"""
Process Approved Outreach - Send emails for approved requests
Run this daily (or whenever) to process your approved outreach queue
"""

import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

notion_api_key = os.getenv("NOTION_API_KEY")
notion_crm_db_id = "23d632f5307e8001a1d6fb31be92d59e"
notion_approval_db_id = os.getenv("NOTION_APPROVAL_DB_ID")

# Gmail credentials - support multiple accounts
GMAIL_CREDENTIALS = {
    "tom@whyhi.app": os.getenv("GMAIL_PASSWORD_TOM"),
    "admin@whyhi.app": os.getenv("GMAIL_PASSWORD_ADMIN"),
    "hello@whyhi.app": os.getenv("GMAIL_PASSWORD_HELLO")
}

headers = {
    "Authorization": f"Bearer {notion_api_key}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

print("📧 Processing Approved Outreach Queue")
print("=" * 60)
print()

# Step 1: Query Approval Queue for "Approved" items
print("Step 1: Finding approved outreach requests...")

response = requests.post(
    f"https://api.notion.com/v1/databases/{notion_approval_db_id}/query",
    headers=headers,
    json={
        "filter": {
            "and": [
                {
                    "property": "Status",
                    "select": {
                        "equals": "Approved"
                    }
                },
                {
                    "property": "Intent",
                    "rich_text": {
                        "contains": "creator_outreach"
                    }
                }
            ]
        }
    }
)

if response.status_code != 200:
    print(f"❌ Failed to query approvals: {response.status_code}")
    print(f"   Error: {response.text}")
    exit(1)

approvals = response.json()["results"]

if not approvals:
    print("   ℹ️  No approved outreach requests found")
    print()
    print("   To test:")
    print("   1. Run: python3 test_creator_outreach_workflow.py")
    print("   2. Open the Notion approval URL")
    print("   3. Change Status to 'Approved'")
    print("   4. Run this script again")
    exit(0)

print(f"   ✅ Found {len(approvals)} approved request(s)")
print()

# Process each approved request
sent_count = 0
error_count = 0

for approval in approvals:
    approval_id = approval["id"]
    props = approval["properties"]

    # Extract approval info
    def get_text(prop):
        if not prop:
            return ""
        if prop["type"] == "title":
            return prop["title"][0]["text"]["content"] if prop["title"] else ""
        elif prop["type"] == "rich_text":
            return prop["rich_text"][0]["text"]["content"] if prop["rich_text"] else ""
        elif prop["type"] == "select":
            return prop["select"]["name"] if prop["select"] else ""
        return ""

    title = get_text(props.get("Name"))
    request_id = get_text(props.get("Request ID"))
    sending_email = get_text(props.get("Sending Email")) or "tom@whyhi.app"  # Default to tom@whyhi.app

    print(f"Processing: {title}")

    # Get the page content (has the message and metadata)
    response = requests.get(
        f"https://api.notion.com/v1/blocks/{approval_id}/children",
        headers=headers
    )

    if response.status_code != 200:
        print(f"   ❌ Failed to get approval content")
        error_count += 1
        continue

    blocks = response.json()["results"]

    # Extract message from code block
    message = None
    metadata = None

    for block in blocks:
        if block["type"] == "code":
            code_content = block["code"]["rich_text"]
            if code_content:
                text = code_content[0]["text"]["content"]

                # Check if it's the message or metadata
                if block["code"]["language"] == "markdown":
                    message = text
                elif block["code"]["language"] == "json":
                    import json
                    try:
                        metadata = json.loads(text)
                    except:
                        pass

    if not message or not metadata:
        print(f"   ⚠️  Couldn't extract message/metadata, skipping")
        error_count += 1
        continue

    creator_name = metadata.get("creator_name", "Unknown")
    contact_method = metadata.get("contact_method", "")

    # Only send if contact method is email
    if "email" not in contact_method.lower():
        print(f"   ⏭️  Skipping - contact method is {contact_method} (not email)")
        continue

    # Get creator from CRM to get email address
    print(f"   Looking up {creator_name} in CRM...")

    response = requests.post(
        f"https://api.notion.com/v1/databases/{notion_crm_db_id}/query",
        headers=headers,
        json={
            "filter": {
                "property": "Name",
                "title": {
                    "equals": creator_name
                }
            }
        }
    )

    if response.status_code != 200 or not response.json()["results"]:
        print(f"   ❌ Couldn't find creator in CRM")
        error_count += 1
        continue

    creator_page = response.json()["results"][0]
    creator_page_id = creator_page["id"]
    creator_props = creator_page["properties"]

    # Extract email
    email_prop = creator_props.get("Email", {})
    to_email = email_prop.get("email") if email_prop.get("type") == "email" else None

    if not to_email:
        print(f"   ⚠️  No email address found for {creator_name}")
        error_count += 1
        continue

    print(f"   📧 Sending to: {to_email}")
    print(f"   📤 From: {sending_email}")

    # Extract subject from message (first line after "Subject:")
    subject = "WhyHi - Voice-first social app"
    if "Subject:" in message:
        lines = message.split("\n")
        for line in lines:
            if line.startswith("Subject:"):
                subject = line.replace("Subject:", "").strip()
                # Remove subject line from message body
                message = "\n".join([l for l in lines if not l.startswith("Subject:")])
                break

    # Get credentials for sending email
    gmail_password = GMAIL_CREDENTIALS.get(sending_email)

    # Send email
    if not gmail_password:
        print(f"   ⚠️  Gmail password not set for {sending_email} - skipping actual send")
        print(f"   ℹ️  Would send email to {to_email}")
        print(f"   ℹ️  Subject: {subject}")
        print()
        print("   To enable sending:")
        print("   1. Go to https://myaccount.google.com/apppasswords")
        print("   2. Generate an app password for 'Mail'")
        print(f"   3. Add to .env: GMAIL_PASSWORD_TOM=your-app-password")
        print("      (or GMAIL_PASSWORD_ADMIN, GMAIL_PASSWORD_HELLO)")
        print()
        continue

    try:
        # Create email
        msg = MIMEMultipart()
        msg['From'] = sending_email
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        # Send via Gmail SMTP
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sending_email, gmail_password)
            smtp.send_message(msg)

        print(f"   ✅ Email sent to {to_email}")
        sent_count += 1

        # Update CRM status to "Outreach Sent"
        response = requests.patch(
            f"https://api.notion.com/v1/pages/{creator_page_id}",
            headers=headers,
            json={
                "properties": {
                    "Outreach Status": {
                        "select": {"name": "Outreach Sent"}
                    }
                }
            }
        )

        if response.status_code == 200:
            print(f"   ✅ CRM updated to 'Outreach Sent'")

        # Mark approval as "Completed"
        response = requests.patch(
            f"https://api.notion.com/v1/pages/{approval_id}",
            headers=headers,
            json={
                "properties": {
                    "Status": {
                        "select": {"name": "Completed"}
                    }
                }
            }
        )

        if response.status_code == 200:
            print(f"   ✅ Approval marked 'Completed'")

    except Exception as e:
        print(f"   ❌ Failed to send email: {e}")
        error_count += 1

    print()

# Summary
print("=" * 60)
print("✅ PROCESSING COMPLETE")
print("=" * 60)
print()
print(f"Emails sent: {sent_count}")
print(f"Errors/skipped: {error_count}")
print()

if sent_count > 0:
    print("What happened:")
    print("1. ✅ Found approved outreach requests in Notion")
    print("2. ✅ Extracted message content and creator info")
    print("3. ✅ Looked up email addresses from CRM")
    print("4. ✅ Sent emails via Gmail")
    print("5. ✅ Updated CRM to 'Outreach Sent'")
    print("6. ✅ Marked approvals as 'Completed'")
    print()
