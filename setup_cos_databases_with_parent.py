#!/usr/bin/env python3
"""
COS Notion Database Setup Script (With Parent Page)
Creates a parent page first, then creates databases under it
"""

import os
import sys
from notion_client import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Notion client
notion = Client(auth=os.getenv("NOTION_API_KEY"))

# Existing database ID
CONTENT_CREATOR_CAPTURE_ID = "23d632f5307e8001a1d6fb31be92d59e"

def format_database_id(db_id: str) -> str:
    """Format database ID for Notion API (add dashes if needed)"""
    if "-" not in db_id:
        return f"{db_id[:8]}-{db_id[8:12]}-{db_id[12:16]}-{db_id[16:20]}-{db_id[20:]}"
    return db_id

def create_parent_page():
    """Create a parent page for COS databases"""
    print("\n" + "=" * 60)
    print("STEP 0: Creating COS Parent Page")
    print("=" * 60)

    # We'll try to find an existing page to use as parent, or create a new one
    # Let's use the existing Content & Creator Capture database as a reference
    # We need to find its parent workspace

    # For now, let's create a page in the workspace by using a known database as reference
    try:
        # Try to get the database to find its parent
        db = notion.databases.retrieve(database_id=format_database_id(CONTENT_CREATOR_CAPTURE_ID))

        # Create a new page in the same parent as the database
        parent = db.get("parent", {})

        page = notion.pages.create(
            parent=parent,
            properties={
                "title": [{"text": {"content": "COS - Content Operating System"}}]
            },
            children=[
                {
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [{"type": "text", "text": {"content": "Content Operating System (COS)"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": "This page contains all COS databases for automated content creation and scheduling."}}]
                    }
                }
            ]
        )

        page_id = page["id"]
        print(f"\n✅ Created COS parent page")
        print(f"   Page ID: {page_id}")
        return page_id
    except Exception as e:
        print(f"\n❌ Error creating parent page: {e}")
        return None

def create_content_ideas_queue(parent_page_id):
    """Create Content Ideas Queue database"""
    print("\n" + "=" * 60)
    print("STEP 1: Creating Content Ideas Queue Database")
    print("=" * 60)

    database_config = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "title": [{"type": "text", "text": {"content": "Content Ideas Queue"}}],
        "properties": {
            "Title": {"title": {}},
            "Idea Description": {"rich_text": {}},
            "Status": {
                "select": {
                    "options": [
                        {"name": "Proposed", "color": "yellow"},
                        {"name": "Approved", "color": "green"},
                        {"name": "Rejected", "color": "red"},
                        {"name": "Done", "color": "gray"}
                    ]
                }
            },
            "Platform": {
                "select": {
                    "options": [
                        {"name": "LinkedIn", "color": "blue"},
                        {"name": "Facebook", "color": "blue"},
                        {"name": "Instagram", "color": "pink"},
                        {"name": "All", "color": "purple"}
                    ]
                }
            },
            "Content Type": {
                "select": {
                    "options": [
                        {"name": "Social Post", "color": "green"},
                        {"name": "Video", "color": "red"},
                        {"name": "Blog Post", "color": "orange"}
                    ]
                }
            },
            "Use Case Reference": {"rich_text": {}},
            "Formula Used": {
                "select": {
                    "options": [
                        {"name": "Use Case Spotlight", "color": "blue"},
                        {"name": "Hidden Cost", "color": "orange"},
                        {"name": "Moment of Clarity", "color": "purple"},
                        {"name": "Problem People Don't Know", "color": "yellow"}
                    ]
                }
            },
            "Notes": {"rich_text": {}}
        }
    }

    try:
        response = notion.databases.create(**database_config)
        db_id = response["id"]
        print(f"\n✅ Content Ideas Queue created successfully!")
        print(f"   Database ID: {db_id}")
        return db_id
    except Exception as e:
        print(f"\n❌ Error creating Content Ideas Queue: {e}")
        return None

def create_drafts_for_review(parent_page_id):
    """Create Drafts for Review database"""
    print("\n" + "=" * 60)
    print("STEP 2: Creating Drafts for Review Database")
    print("=" * 60)

    database_config = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "title": [{"type": "text", "text": {"content": "Drafts for Review"}}],
        "properties": {
            "Title": {"title": {}},
            "Status": {
                "select": {
                    "options": [
                        {"name": "Draft", "color": "yellow"},
                        {"name": "Needs Revision", "color": "orange"},
                        {"name": "Approved", "color": "green"},
                        {"name": "Scheduled", "color": "blue"}
                    ]
                }
            },
            "Content Type": {
                "select": {
                    "options": [
                        {"name": "Social Post", "color": "green"},
                        {"name": "Social Video", "color": "red"},
                        {"name": "Instructional Video", "color": "purple"}
                    ]
                }
            },
            "Platform": {
                "select": {
                    "options": [
                        {"name": "LinkedIn", "color": "blue"},
                        {"name": "Facebook", "color": "blue"},
                        {"name": "Instagram", "color": "pink"},
                        {"name": "All Platforms", "color": "purple"}
                    ]
                }
            },
            "LinkedIn Content": {"rich_text": {}},
            "Facebook Content": {"rich_text": {}},
            "Instagram Content": {"rich_text": {}},
            "Video Script": {"rich_text": {}},
            "Storyboard Notes": {"rich_text": {}},
            "Image Suggestions": {"rich_text": {}},
            "Created Date": {"date": {}},
            "Last Edited": {"last_edited_time": {}},
            "Notes": {"rich_text": {}}
        }
    }

    try:
        response = notion.databases.create(**database_config)
        db_id = response["id"]
        print(f"\n✅ Drafts for Review created successfully!")
        print(f"   Database ID: {db_id}")
        return db_id
    except Exception as e:
        print(f"\n❌ Error creating Drafts for Review: {e}")
        return None

def create_content_calendar(parent_page_id):
    """Create Content Calendar database"""
    print("\n" + "=" * 60)
    print("STEP 3: Creating Content Calendar Database")
    print("=" * 60)

    database_config = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "title": [{"type": "text", "text": {"content": "Content Calendar"}}],
        "properties": {
            "Title": {"title": {}},
            "Scheduled Date": {"date": {}},
            "Status": {
                "select": {
                    "options": [
                        {"name": "Scheduled", "color": "blue"},
                        {"name": "Posted", "color": "green"},
                        {"name": "Failed", "color": "red"}
                    ]
                }
            },
            "Platform": {
                "select": {
                    "options": [
                        {"name": "LinkedIn", "color": "blue"},
                        {"name": "Facebook", "color": "blue"},
                        {"name": "Instagram", "color": "pink"}
                    ]
                }
            },
            "Content Type": {
                "select": {
                    "options": [
                        {"name": "Social Post", "color": "green"},
                        {"name": "Video", "color": "red"}
                    ]
                }
            },
            "Buffer Post ID": {"rich_text": {}},
            "Post URL": {"url": {}},
            "Likes": {"number": {"format": "number"}},
            "Comments": {"number": {"format": "number"}},
            "Shares": {"number": {"format": "number"}},
            "Reach": {"number": {"format": "number"}},
            "Notes": {"rich_text": {}}
        }
    }

    try:
        response = notion.databases.create(**database_config)
        db_id = response["id"]
        print(f"\n✅ Content Calendar created successfully!")
        print(f"   Database ID: {db_id}")
        return db_id
    except Exception as e:
        print(f"\n❌ Error creating Content Calendar: {e}")
        return None

def add_relations(content_creator_id, ideas_queue_id, drafts_review_id, calendar_id):
    """Add relation properties between databases"""
    print("\n" + "=" * 60)
    print("STEP 4: Setting Up Database Relations")
    print("=" * 60)

    success_count = 0

    # 1. Add "Generated Ideas" relation to Content & Creator Capture
    if content_creator_id and ideas_queue_id:
        try:
            notion.databases.update(
                database_id=format_database_id(content_creator_id),
                properties={
                    "Generated Ideas": {
                        "relation": {
                            "database_id": ideas_queue_id,
                            "type": "dual_property",
                            "dual_property": {}
                        }
                    }
                }
            )
            print("✅ Added relation: Content & Creator Capture → Content Ideas Queue")
            success_count += 1
        except Exception as e:
            print(f"❌ Error adding Generated Ideas relation: {e}")

    # 2. Add "Generated Draft" relation to Content Ideas Queue → Drafts for Review
    if ideas_queue_id and drafts_review_id:
        try:
            notion.databases.update(
                database_id=ideas_queue_id,
                properties={
                    "Generated Draft": {
                        "relation": {
                            "database_id": drafts_review_id,
                            "type": "dual_property",
                            "dual_property": {}
                        }
                    }
                }
            )
            print("✅ Added relation: Content Ideas Queue → Drafts for Review")
            success_count += 1
        except Exception as e:
            print(f"❌ Error adding Generated Draft relation: {e}")

    # 3. Add "Related Drafts" relation to Content & Creator Capture → Drafts for Review
    if content_creator_id and drafts_review_id:
        try:
            notion.databases.update(
                database_id=format_database_id(content_creator_id),
                properties={
                    "Related Drafts": {
                        "relation": {
                            "database_id": drafts_review_id,
                            "type": "dual_property",
                            "dual_property": {}
                        }
                    }
                }
            )
            print("✅ Added relation: Content & Creator Capture → Drafts for Review")
            success_count += 1
        except Exception as e:
            print(f"❌ Error adding Related Drafts relation: {e}")

    # 4. Add "Scheduled Post" relation to Drafts for Review → Content Calendar
    if drafts_review_id and calendar_id:
        try:
            notion.databases.update(
                database_id=drafts_review_id,
                properties={
                    "Scheduled Post": {
                        "relation": {
                            "database_id": calendar_id,
                            "type": "dual_property",
                            "dual_property": {}
                        }
                    }
                }
            )
            print("✅ Added relation: Drafts for Review → Content Calendar")
            success_count += 1
        except Exception as e:
            print(f"❌ Error adding Scheduled Post relation: {e}")

    print(f"\n✅ Successfully created {success_count}/4 relations")
    return success_count == 4

def main():
    print("\n" + "=" * 60)
    print("COS NOTION DATABASE SETUP (WITH PARENT PAGE)")
    print("Phase 1, Day 2: Foundation")
    print("=" * 60)

    # Check Notion API key
    if not os.getenv("NOTION_API_KEY"):
        print("\n❌ NOTION_API_KEY not found in .env file")
        sys.exit(1)

    print("\n🚀 Starting automated database setup...")

    # STEP 0: Create parent page
    parent_page_id = create_parent_page()
    if not parent_page_id:
        print("\n❌ Failed to create parent page. Exiting.")
        sys.exit(1)

    # STEP 1-3: Create new databases
    ideas_queue_id = create_content_ideas_queue(parent_page_id)
    drafts_review_id = create_drafts_for_review(parent_page_id)
    calendar_id = create_content_calendar(parent_page_id)

    if not all([ideas_queue_id, drafts_review_id, calendar_id]):
        print("\n⚠️  Some databases failed to create. Relations may be incomplete.")
        sys.exit(1)

    # STEP 4: Set up relations
    content_creator_id = CONTENT_CREATOR_CAPTURE_ID
    add_relations(content_creator_id, ideas_queue_id, drafts_review_id, calendar_id)

    # Summary
    print("\n" + "=" * 60)
    print("SETUP COMPLETE!")
    print("=" * 60)
    print("\n✅ COS Database IDs:")
    print(f"  COS Parent Page: {parent_page_id}")
    print(f"  Content & Creator Capture: {format_database_id(content_creator_id)}")
    print(f"  Content Ideas Queue: {ideas_queue_id}")
    print(f"  Drafts for Review: {drafts_review_id}")
    print(f"  Content Calendar: {calendar_id}")

    # Write database IDs to a file for easy reference
    with open("cos_database_ids.txt", "w") as f:
        f.write("COS Database IDs\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"COS Parent Page: {parent_page_id}\n")
        f.write(f"Content & Creator Capture: {format_database_id(content_creator_id)}\n")
        f.write(f"Content Ideas Queue: {ideas_queue_id}\n")
        f.write(f"Drafts for Review: {drafts_review_id}\n")
        f.write(f"Content Calendar: {calendar_id}\n")

    print("\n💾 Database IDs saved to: cos_database_ids.txt")

    print("\n✅ Next Steps:")
    print("  1. Check your Notion workspace - look for 'COS - Content Operating System' page")
    print("  2. You'll find 3 new databases under that page")
    print("  3. Test create a sample entry in each database")
    print("  4. Verify relations are working between databases")
    print("  5. Update content_capture n8n workflow with new fields")

if __name__ == "__main__":
    main()
