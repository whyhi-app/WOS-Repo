#!/usr/bin/env python3
"""
Add missing properties to Content & Creator Capture database
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = "edbf92f3-d884-478a-a27e-11d1c6c929ca"

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Define all the properties that need to be added
properties = {
    "URL": {"url": {}},
    "Platform": {
        "select": {
            "options": [
                {"name": "Twitter/X", "color": "blue"},
                {"name": "Instagram", "color": "pink"},
                {"name": "Instagram (Post)", "color": "pink"},
                {"name": "YouTube", "color": "red"},
                {"name": "YouTube (Video)", "color": "red"},
                {"name": "TikTok", "color": "default"},
                {"name": "LinkedIn", "color": "blue"},
                {"name": "LinkedIn (Company)", "color": "blue"},
                {"name": "Facebook", "color": "blue"},
                {"name": "Facebook (Page)", "color": "blue"},
                {"name": "Article/Blog", "color": "gray"}
            ]
        }
    },
    "Action Type": {
        "multi_select": {
            "options": [
                {"name": "💡 Content Ideation", "color": "blue"},
                {"name": "🤝 Outreach", "color": "green"}
            ]
        }
    },
    "Topic Tags": {
        "multi_select": {
            "options": [
                {"name": "Loneliness", "color": "red"},
                {"name": "Telephobia", "color": "orange"},
                {"name": "Connection", "color": "yellow"},
                {"name": "Texting vs Calling", "color": "green"},
                {"name": "Professional Communication", "color": "blue"},
                {"name": "Neurodiversity", "color": "purple"},
                {"name": "Parent Scenarios", "color": "pink"},
                {"name": "Friendship Maintenance", "color": "brown"}
            ]
        }
    },
    "Relevance Score": {"number": {"format": "number"}},
    "Content Notes": {"rich_text": {}},
    "Ideation Status": {
        "select": {
            "options": [
                {"name": "New", "color": "gray"},
                {"name": "Sent to COS", "color": "blue"},
                {"name": "Ideas Generated", "color": "green"}
            ]
        }
    },
    "Contact Method": {"rich_text": {}},
    "Outreach Status": {
        "select": {
            "options": [
                {"name": "New Lead", "color": "gray"},
                {"name": "Draft Ready", "color": "yellow"},
                {"name": "Awaiting Approval", "color": "orange"},
                {"name": "Outreach Sent", "color": "green"}
            ]
        }
    },
    "Notes": {"rich_text": {}},
    "Email": {"email": {}},
    "Company": {"rich_text": {}}
}

# Update the database with all properties
url = f"https://api.notion.com/v1/databases/{DATABASE_ID}"
data = {"properties": properties}

print("Adding properties to Content & Creator Capture database...")
response = requests.patch(url, headers=headers, json=data)

if response.status_code == 200:
    print("✅ Success! All properties have been added.")
    print("\nProperties added:")
    for prop_name in properties.keys():
        print(f"  • {prop_name}")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
