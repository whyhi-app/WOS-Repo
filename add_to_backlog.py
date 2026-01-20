#!/usr/bin/env python3
"""
Add to Backlog - Dual capture to BACKLOG.md + Notion tasks-masterlist
Usage: python3 add_to_backlog.py "Task description"
"""

import os
import sys
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

notion_api_key = os.getenv("NOTION_API_KEY")
notion_tasks_db_id = "235632f5307e804fac20fcad655dba8a"  # tasks-masterlist

headers = {
    "Authorization": f"Bearer {notion_api_key}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

if len(sys.argv) < 2:
    print("Usage: python3 add_to_backlog.py \"Task description\"")
    print()
    print("Example:")
    print('  python3 add_to_backlog.py "Set up Facebook API for auto-DM sending"')
    print()
    print("This will:")
    print("  1. Add task to BACKLOG.md")
    print("  2. Create task in Notion tasks-masterlist with Context: 'Backlog'")
    sys.exit(1)

task_description = " ".join(sys.argv[1:])
today = datetime.now().strftime("%b %d, %Y")

print(f"📝 Adding to backlog: {task_description}")
print()

# Step 1: Add to BACKLOG.md
print("1. Adding to BACKLOG.md...")

backlog_entry = f"""
## {task_description}

**Added:** {today}

- [ ] {task_description}

---
"""

try:
    with open("BACKLOG.md", "a") as f:
        f.write(backlog_entry)
    print("   ✅ Added to BACKLOG.md")
except Exception as e:
    print(f"   ❌ Failed to update BACKLOG.md: {e}")
    sys.exit(1)

# Step 2: Create Notion task
print("2. Creating task in Notion...")

try:
    response = requests.post(
        "https://api.notion.com/v1/pages",
        headers=headers,
        json={
            "parent": {"database_id": notion_tasks_db_id},
            "properties": {
                "Name": {
                    "title": [{"text": {"content": task_description}}]
                },
                "Context": {
                    "multi_select": [{"name": "Backlog"}]
                }
            }
        }
    )

    if response.status_code == 200:
        notion_url = response.json()["url"]
        print(f"   ✅ Created in Notion: {notion_url}")
    else:
        print(f"   ❌ Failed to create Notion task: {response.status_code}")
        print(f"   Error: {response.text}")

except Exception as e:
    print(f"   ❌ Failed to create Notion task: {e}")

print()
print("=" * 60)
print("✅ Backlog item captured!")
print("=" * 60)
print()
print("Task added to:")
print("  - BACKLOG.md (version controlled)")
print("  - Notion tasks-masterlist (Context: 'Backlog')")
print()
print("When ready to work on it:")
print("  - Update details in Notion")
print("  - When complete, delete from BACKLOG.md and commit")
print()
