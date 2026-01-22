#!/usr/bin/env python3
"""
Update Content Ideas Queue database with additional properties for Content Idea Miner
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
IDEAS_QUEUE_ID = "dae2c9d9-83ce-46b4-be71-f057c0dc5230"

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Add new properties needed by Content Idea Miner
new_properties = {
    "Angle": {
        "select": {
            "options": [
                {"name": "Use Case Spotlight", "color": "blue"},
                {"name": "Hidden Cost", "color": "orange"},
                {"name": "Moment of Clarity", "color": "purple"},
                {"name": "Problem People Don't Know", "color": "yellow"},
                {"name": "Social Proof", "color": "green"},
                {"name": "Emotional Trigger", "color": "red"}
            ]
        }
    },
    "Target Audience": {
        "select": {
            "options": [
                {"name": "Busy Professionals", "color": "blue"},
                {"name": "Telephobia Community", "color": "orange"},
                {"name": "Neurodivergent Individuals", "color": "purple"},
                {"name": "Friendship Maintainers", "color": "pink"},
                {"name": "Parent Demographic", "color": "green"},
                {"name": "General", "color": "gray"}
            ]
        }
    },
    "Content Hook": {"rich_text": {}},
    "Format": {
        "select": {
            "options": [
                {"name": "Text Post", "color": "blue"},
                {"name": "Carousel", "color": "purple"},
                {"name": "Video", "color": "red"},
                {"name": "Reel", "color": "pink"},
                {"name": "Thread", "color": "orange"},
                {"name": "Story", "color": "yellow"}
            ]
        }
    },
    "Why It Works": {"rich_text": {}},
    "Source Content": {
        "relation": {
            "database_id": "edbf92f3-d884-478a-a27e-11d1c6c929ca",  # Content & Creator Capture
            "type": "dual_property",
            "dual_property": {}
        }
    }
}

# Update the database
url = f"https://api.notion.com/v1/databases/{IDEAS_QUEUE_ID}"
data = {"properties": new_properties}

print("Adding properties to Content Ideas Queue database...")
response = requests.patch(url, headers=headers, json=data)

if response.status_code == 200:
    print("✅ Success! New properties have been added.")
    print("\nProperties added:")
    for prop_name in new_properties.keys():
        print(f"  • {prop_name}")
    print("\nThe database is now ready for the Content Idea Miner agent!")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
