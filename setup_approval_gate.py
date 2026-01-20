"""
Setup Approval Gate with Notion
Sprint 1 - Create approval queue database in Notion
"""

import os
import requests
import json

def setup_notion_approval_database(notion_api_key: str, parent_page_id: str = None):
    """
    Create WOS Approval Queue database in Notion

    Args:
        notion_api_key: Your Notion API key (integration token)
        parent_page_id: Optional - Notion page ID to create database under
                       (If not provided, will create in workspace root)

    Returns:
        Database ID to use in NOTION_APPROVAL_DB_ID
    """

    print("🔧 Setting up WOS Approval Queue in Notion...")
    print()

    # Notion API settings
    headers = {
        "Authorization": f"Bearer {notion_api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    # Database schema
    database_data = {
        "parent": {},
        "title": [
            {
                "type": "text",
                "text": {"content": "WOS Approval Queue"}
            }
        ],
        "properties": {
            "Name": {
                "title": {}
            },
            "Status": {
                "select": {
                    "options": [
                        {"name": "Pending", "color": "yellow"},
                        {"name": "Approved", "color": "green"},
                        {"name": "Rejected", "color": "red"}
                    ]
                }
            },
            "Request ID": {
                "rich_text": {}
            },
            "Intent": {
                "rich_text": {}
            },
            "Created": {
                "created_time": {}
            },
            "Last Edited": {
                "last_edited_time": {}
            }
        }
    }

    # Set parent (page or workspace)
    if parent_page_id:
        database_data["parent"] = {"type": "page_id", "page_id": parent_page_id}
    else:
        # Create in workspace root
        database_data["parent"] = {"type": "workspace", "workspace": True}

    # Create database
    try:
        response = requests.post(
            "https://api.notion.com/v1/databases",
            headers=headers,
            json=database_data
        )

        response.raise_for_status()
        result = response.json()

        database_id = result["id"]
        database_url = result["url"]

        print("✅ Approval Queue database created!")
        print()
        print(f"Database ID: {database_id}")
        print(f"Database URL: {database_url}")
        print()
        print("=" * 60)
        print("Add these to your .env file:")
        print("=" * 60)
        print(f"NOTION_API_KEY={notion_api_key}")
        print(f"NOTION_APPROVAL_DB_ID={database_id}")
        print("=" * 60)
        print()
        print("✅ Setup complete! Approval Gate is ready to use.")
        print()

        return database_id

    except requests.exceptions.HTTPError as e:
        print(f"❌ Failed to create database:")
        print(f"   Status: {e.response.status_code}")
        print(f"   Error: {e.response.text}")
        print()
        print("Common issues:")
        print("- Invalid API key (check your Notion integration token)")
        print("- Invalid parent_page_id (make sure the page exists and integration has access)")
        print("- Integration not shared with workspace/page")
        print()
        raise


def get_notion_api_key():
    """Helper to get Notion API key from user"""

    print("=" * 60)
    print("NOTION API KEY SETUP")
    print("=" * 60)
    print()
    print("To use the Approval Gate, you need a Notion API key.")
    print()
    print("Steps to get your API key:")
    print("1. Go to https://www.notion.so/my-integrations")
    print("2. Click '+ New integration'")
    print("3. Name it 'WOS Approval Gate' (or anything you like)")
    print("4. Select your workspace")
    print("5. Click 'Submit'")
    print("6. Copy the 'Internal Integration Token'")
    print()
    print("IMPORTANT: After creating the integration:")
    print("- Go to the Notion page where you want the approval database")
    print("- Click '...' menu → 'Add connections' → Select your integration")
    print("- This gives the integration permission to create/read pages")
    print()

    api_key = input("Paste your Notion API key (starts with 'secret_'): ").strip()

    if not api_key.startswith("secret_"):
        print()
        print("⚠️  Warning: Notion API keys usually start with 'secret_'")
        confirm = input("Continue anyway? (y/n): ").strip().lower()
        if confirm != 'y':
            return None

    return api_key


def get_parent_page_id():
    """Helper to get optional parent page ID"""

    print()
    print("=" * 60)
    print("PARENT PAGE (Optional)")
    print("=" * 60)
    print()
    print("You can create the approval database:")
    print("A) In your workspace root (accessible from sidebar)")
    print("B) Under a specific page (keeps it organized)")
    print()

    choice = input("Create under a specific page? (y/n): ").strip().lower()

    if choice == 'y':
        print()
        print("To get the page ID:")
        print("1. Open the page in Notion")
        print("2. Copy the URL (looks like: notion.so/Page-Title-abc123...)")
        print("3. The page ID is the part after the last dash (abc123...)")
        print()
        page_id = input("Paste page ID (or press Enter to skip): ").strip()

        if page_id:
            # Clean up the ID (remove dashes if copied full)
            page_id = page_id.replace("-", "")
            return page_id

    return None


if __name__ == "__main__":
    print()
    print("🚀 WOS Approval Gate Setup")
    print()

    # Get API key
    api_key = get_notion_api_key()

    if not api_key:
        print("❌ Setup cancelled")
        exit(1)

    # Get parent page ID (optional)
    parent_id = get_parent_page_id()

    # Create database
    try:
        db_id = setup_notion_approval_database(api_key, parent_id)

        print("🎉 Success! Your Approval Gate is configured.")
        print()
        print("Next steps:")
        print("1. Add the NOTION_API_KEY and NOTION_APPROVAL_DB_ID to your .env file")
        print("2. Test the approval gate with test_approval_gate.py")
        print("3. Start building agents that require approval!")
        print()

    except Exception as e:
        print(f"❌ Setup failed: {e}")
        exit(1)
