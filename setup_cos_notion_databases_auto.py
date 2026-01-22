#!/usr/bin/env python3
"""
COS Notion Database Setup Script (Auto-Run Version)
Phase 1, Day 2: Create and configure all Notion databases for COS
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

def update_content_creator_capture():
    """Add new properties to Content & Creator Capture database"""
    print("\n" + "=" * 60)
    print("STEP 1: Updating Content & Creator Capture Database")
    print("=" * 60)

    formatted_id = format_database_id(CONTENT_CREATOR_CAPTURE_ID)

    # Define new properties to add
    new_properties = {
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
        "Relevance Score": {
            "number": {
                "format": "number"
            }
        },
        "Content Notes": {
            "rich_text": {}
        },
        "Ideation Status": {
            "select": {
                "options": [
                    {"name": "New", "color": "gray"},
                    {"name": "Sent to COS", "color": "blue"},
                    {"name": "Ideas Generated", "color": "green"}
                ]
            }
        }
    }

    print("\n📝 Adding new properties:")
    for prop_name in new_properties.keys():
        print(f"  - {prop_name}")

    try:
        response = notion.databases.update(
            database_id=formatted_id,
            properties=new_properties
        )
        print("\n✅ Content & Creator Capture database updated successfully!")
        return formatted_id
    except Exception as e:
        print(f"\n❌ Error updating database: {e}")
        return None

def create_content_ideas_queue():
    """Create Content Ideas Queue database"""
    print("\n" + "=" * 60)
    print("STEP 2: Creating Content Ideas Queue Database")
    print("=" * 60)

    database_config = {
        "parent": {"type": "workspace", "workspace": True},
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

def create_drafts_for_review():
    """Create Drafts for Review database"""
    print("\n" + "=" * 60)
    print("STEP 3: Creating Drafts for Review Database")
    print("=" * 60)

    database_config = {
        "parent": {"type": "workspace", "workspace": True},
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

def create_content_calendar():
    """Create Content Calendar database"""
    print("\n" + "=" * 60)
    print("STEP 4: Creating Content Calendar Database")
    print("=" * 60)

    database_config = {
        "parent": {"type": "workspace", "workspace": True},
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
    print("STEP 5: Setting Up Database Relations")
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
    print("COS NOTION DATABASE SETUP (AUTO-RUN)")
    print("Phase 1, Day 2: Foundation")
    print("=" * 60)

    # Check Notion API key
    if not os.getenv("NOTION_API_KEY"):
        print("\n❌ NOTION_API_KEY not found in .env file")
        sys.exit(1)

    print("\n🚀 Starting automated database setup...")

    # STEP 1: Update Content & Creator Capture
    content_creator_id = update_content_creator_capture()
    if not content_creator_id:
        print("\n❌ Failed to update Content & Creator Capture. Exiting.")
        sys.exit(1)

    # STEP 2-4: Create new databases (using workspace root)
    ideas_queue_id = create_content_ideas_queue()
    drafts_review_id = create_drafts_for_review()
    calendar_id = create_content_calendar()

    if not all([ideas_queue_id, drafts_review_id, calendar_id]):
        print("\n⚠️  Some databases failed to create. Relations may be incomplete.")

    # STEP 5: Set up relations
    if ideas_queue_id and drafts_review_id and calendar_id:
        add_relations(content_creator_id, ideas_queue_id, drafts_review_id, calendar_id)

    # Summary
    print("\n" + "=" * 60)
    print("SETUP COMPLETE!")
    print("=" * 60)
    print("\n✅ Database IDs:")
    print(f"  Content & Creator Capture: {content_creator_id}")
    if ideas_queue_id:
        print(f"  Content Ideas Queue: {ideas_queue_id}")
    if drafts_review_id:
        print(f"  Drafts for Review: {drafts_review_id}")
    if calendar_id:
        print(f"  Content Calendar: {calendar_id}")

    # Write database IDs to a file for easy reference
    with open("cos_database_ids.txt", "w") as f:
        f.write("COS Database IDs\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Content & Creator Capture: {content_creator_id}\n")
        if ideas_queue_id:
            f.write(f"Content Ideas Queue: {ideas_queue_id}\n")
        if drafts_review_id:
            f.write(f"Drafts for Review: {drafts_review_id}\n")
        if calendar_id:
            f.write(f"Content Calendar: {calendar_id}\n")

    print("\n💾 Database IDs saved to: cos_database_ids.txt")

    print("\n✅ Next Steps:")
    print("  1. Check your Notion workspace for the 3 new databases")
    print("  2. Test create a sample entry in each database")
    print("  3. Verify relations are working")
    print("  4. Update content_capture n8n workflow with new fields")

if __name__ == "__main__":
    main()
