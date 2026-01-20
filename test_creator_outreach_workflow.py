"""
Test Creator Outreach Workflow End-to-End
Tests: CRM query → generate message → approval → update CRM
"""

import os
import requests
import time
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

notion_api_key = os.getenv("NOTION_API_KEY")
notion_crm_db_id = "23d632f5307e8001a1d6fb31be92d59e"
notion_approval_db_id = os.getenv("NOTION_APPROVAL_DB_ID")

headers = {
    "Authorization": f"Bearer {notion_api_key}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

print("🧪 Testing Creator Outreach Workflow")
print("=" * 60)
print()

# Step 1: Query CRM for "Draft Ready" creators
print("Step 1: Querying CRM for 'Draft Ready' creators...")

response = requests.post(
    f"https://api.notion.com/v1/databases/{notion_crm_db_id}/query",
    headers=headers,
    json={
        "filter": {
            "property": "Outreach Status",
            "select": {
                "equals": "Draft Ready"
            }
        },
        "page_size": 5
    }
)

if response.status_code != 200:
    print(f"❌ Failed to query CRM: {response.status_code}")
    print(f"   Error: {response.text}")
    exit(1)

results = response.json()["results"]

if not results:
    print("   ⚠️  No creators with 'Draft Ready' status found")
    print()
    print("   Add a creator to CRM with 'Draft Ready' status first:")
    print("   - Run: python3 test_add_creators.py")
    print("   - Or manually add one in Notion")
    exit(0)

print(f"   ✅ Found {len(results)} creator(s) ready for outreach")
print()

# Extract creator info from first result
page = results[0]
page_id = page["id"]
props = page["properties"]

def get_text(prop):
    if not prop:
        return ""
    if prop["type"] == "title":
        return prop["title"][0]["text"]["content"] if prop["title"] else ""
    elif prop["type"] == "rich_text":
        return prop["rich_text"][0]["text"]["content"] if prop["rich_text"] else ""
    elif prop["type"] == "url":
        return prop["url"] or ""
    elif prop["type"] == "email":
        return prop["email"] or ""
    elif prop["type"] == "select":
        return prop["select"]["name"] if prop["select"] else ""
    return ""

creator = {
    "page_id": page_id,
    "name": get_text(props.get("Name")),
    "url": get_text(props.get("URL")),
    "email": get_text(props.get("Email")),
    "contact_method": get_text(props.get("Contact Method")),
    "notes": get_text(props.get("Notes")),
    "status": get_text(props.get("Outreach Status"))
}

print(f"   Testing with: {creator['name']}")
print(f"   Platform: {creator['contact_method']}")
print(f"   URL: {creator['url']}")
print()

# Step 2: Generate personalized message
print("Step 2: Generating personalized outreach message...")

# Determine if email or DM
is_email = "email" in creator["contact_method"].lower() or creator["email"]
platform = creator["contact_method"].split()[0] if creator["contact_method"] else "Unknown"

if is_email:
    # Journalist/blogger template (formal)
    first_name = creator["name"].split()[0] if " " in creator["name"] else creator["name"]
    message = f"""Subject: WhyHi - Voice-first social app launching March 2026

Hi {first_name},

I came across your article: {creator['url']}

I'm Tom, founder of WhyHi - we're launching a voice-first social app in March that eliminates feeds, likes, and text-first engagement in favor of authentic voice conversations.

Given your coverage of social/tech products, I thought you might be interested in an early look before we go live.

Would you be open to a brief chat or early access?

Best,
Tom Wynn
Founder, WhyHi
tom@whyhi.app"""
else:
    # Creator template (casual DM)
    name = creator["name"].replace("@", "")
    first_name = name.split()[0] if " " in name else name
    message = f"""Hey {first_name}!

I saw your post: {creator['url']}

I'm building WhyHi - a voice-first social app launching in March (no feeds, no likes, just real conversations).

Thought you might vibe with what we're doing. Would love to get your thoughts or have you try it early.

Interested?

- Tom
Founder @ WhyHi"""

print("   ✅ Message generated")
print()
print("   Preview:")
print("   " + "-" * 56)
for line in message.split("\n"):
    print("   " + line)
print("   " + "-" * 56)
print()

# Step 3: Create approval request
print("Step 3: Creating approval request in Notion...")

approval_title = f"Outreach to {creator['name']} ({platform})"

page_data = {
    "parent": {"database_id": notion_approval_db_id},
    "properties": {
        "Name": {
            "title": [{"text": {"content": approval_title}}]
        },
        "Status": {
            "select": {"name": "Pending"}
        },
        "Request ID": {
            "rich_text": [{"text": {"content": f"test-{int(time.time())}"}}]
        },
        "Intent": {
            "rich_text": [{"text": {"content": "creator_outreach_v0"}}]
        },
        "Sending Email": {
            "select": {"name": "tom@whyhi.app"}
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
                "rich_text": [{"text": {"content": message}}],
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
                "rich_text": [{"text": {"content": f'{{\n  "creator_name": "{creator["name"]}",\n  "platform": "{platform}",\n  "contact_method": "{creator["contact_method"]}",\n  "original_url": "{creator["url"]}"\n}}'}}],
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

if response.status_code != 200:
    print(f"   ❌ Failed to create approval: {response.status_code}")
    print(f"   Error: {response.text}")
    exit(1)

result = response.json()
approval_id = result["id"]
approval_url = result["url"]

print(f"   ✅ Approval created")
print(f"   Notion URL: {approval_url}")
print()

# Step 4: Wait for approval decision
print("Step 4: Waiting for approval decision...")
print("   (Polling every 5 seconds, 60 second timeout)")
print()
print("   👉 Open the Notion URL above and change status to 'Approved' or 'Rejected'")
print()

timeout = 60
poll_interval = 5
start_time = time.time()

while True:
    elapsed = time.time() - start_time

    if elapsed > timeout:
        print("   ⏱️  Timeout - no decision made in 60 seconds")
        print()
        print("   You can still approve/reject in Notion manually")
        print("   (In real workflow, timeout would be 10 minutes)")
        exit(0)

    # Check approval status
    response = requests.get(
        f"https://api.notion.com/v1/pages/{approval_id}",
        headers=headers
    )

    if response.status_code != 200:
        print(f"   ⚠️  Failed to check status, retrying...")
        time.sleep(poll_interval)
        continue

    page = response.json()
    status_prop = page["properties"].get("Status", {})
    status = status_prop.get("select", {}).get("name", "").lower()

    if status in ["approved", "✅ approved", "approve"]:
        print(f"   ✅ Approved! (after {int(elapsed)}s)")
        print()

        # Step 5: Update CRM status
        print("Step 5: Updating CRM status to 'Outreach Sent'...")

        response = requests.patch(
            f"https://api.notion.com/v1/pages/{page_id}",
            headers=headers,
            json={
                "properties": {
                    "Outreach Status": {
                        "select": {"name": "Outreach Sent"}
                    }
                }
            }
        )

        if response.status_code != 200:
            print(f"   ❌ Failed to update CRM: {response.status_code}")
            print(f"   Error: {response.text}")
        else:
            print(f"   ✅ CRM updated - {creator['name']} is now 'Outreach Sent'")

        print()
        print("=" * 60)
        print("✅ WORKFLOW TEST COMPLETE!")
        print("=" * 60)
        print()
        print("What happened:")
        print("1. ✅ Queried CRM for 'Draft Ready' creators")
        print("2. ✅ Generated personalized outreach message")
        print("3. ✅ Created approval request in Notion")
        print("4. ✅ Waited for your approval decision")
        print("5. ✅ Updated CRM status on approval")
        print()
        print("In the real workflow:")
        print("- This would repeat for each 'Draft Ready' creator")
        print("- Artifact would be published with outreach log")
        print("- You'd manually send the approved messages")
        print()
        break

    elif status in ["rejected", "❌ rejected", "reject"]:
        print(f"   ❌ Rejected (after {int(elapsed)}s)")
        print()
        print("   CRM status NOT updated (stays 'Draft Ready')")
        print()
        print("=" * 60)
        print("✅ WORKFLOW TEST COMPLETE (REJECTION PATH)")
        print("=" * 60)
        print()
        print("What happened:")
        print("1. ✅ Queried CRM for 'Draft Ready' creators")
        print("2. ✅ Generated personalized outreach message")
        print("3. ✅ Created approval request in Notion")
        print("4. ✅ Detected rejection")
        print("5. ✅ Left CRM status unchanged")
        print()
        break

    else:
        # Still pending
        print(f"   ⏳ Pending... ({int(elapsed)}s elapsed)")
        time.sleep(poll_interval)
