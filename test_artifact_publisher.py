"""
Test Artifact Publisher v0.1
Sprint 1 - Verify artifact publishing works end-to-end
"""

import os
from src.wos.artifact_publisher import create_artifact_publisher
from src.wos.canon_tools import create_canon_tools

def test_artifact_publisher():
    """Test the Artifact Publisher utility"""

    print("🧪 Testing Artifact Publisher...")
    print()

    # Step 1: Initialize
    print("1. Initializing Artifact Publisher...")
    repo_root = os.path.dirname(os.path.abspath(__file__))

    # Initialize Canon Tools (for storing in Canon)
    openai_api_key = os.getenv("OPENAI_API_KEY")
    canon_tools = create_canon_tools(
        canon_db_path=os.path.join(repo_root, "canon.db"),
        use_semantic_search=True if openai_api_key else False,
        openai_api_key=openai_api_key
    )

    # Initialize Artifact Publisher
    publisher = create_artifact_publisher(
        repo_root=repo_root,
        canon_tools=canon_tools,
        git_enabled=True
    )

    print(f"   ✅ Initialized at: {publisher.artifacts_dir}")
    print()

    # Step 2: Test basic artifact publishing
    print("2. Publishing test artifact...")

    test_markdown = """# Test Artifact

This is a test artifact created by the Artifact Publisher.

## Details
- **Created:** Sprint 1 testing
- **Purpose:** Verify artifact publishing works
- **Category:** Test

## Content
This artifact demonstrates the following:
1. Markdown file written to /artifacts/test/
2. Artifact URI recorded in Canon
3. Optional git commit

✅ If you're reading this, the Artifact Publisher is working!
"""

    result = publisher.publish_artifact(
        markdown=test_markdown,
        category="test",
        filename="sprint1-test.md",
        artifact_id="test_sprint1_artifact_publisher",
        title="Sprint 1 - Artifact Publisher Test",
        artifact_type="test",
        summary="Test artifact to verify Artifact Publisher works correctly",
        tags=["sprint1", "test", "infrastructure"],
        metadata={"sprint": 1, "test_run": True},
        git_commit=True,
        commit_message="Test artifact publisher\n\nSprint 1 infrastructure testing"
    )

    if result["success"]:
        print(f"   ✅ Published: {result['artifact_path']}")
        print(f"   ✅ URI: {result['artifact_uri']}")
        print(f"   ✅ Canon stored: {result['canon_stored']}")
        print(f"   ✅ Git committed: {result['git_committed']}")
    else:
        print(f"   ❌ Failed: {result['error']}")
        return False

    print()

    # Step 3: Test daily artifact convenience method
    print("3. Publishing daily artifact...")

    daily_markdown = """# Daily Test Artifact

Testing the daily artifact convenience method.

Date: 2026-01-19
"""

    daily_result = publisher.publish_daily_artifact(
        markdown=daily_markdown,
        category="test",
        prefix="daily-test",
        title="Daily Test Artifact",
        artifact_type="test",
        git_commit=False  # Don't commit this one
    )

    if daily_result["success"]:
        print(f"   ✅ Published: {daily_result['artifact_path']}")
        print(f"   ✅ URI: {daily_result['artifact_uri']}")
    else:
        print(f"   ❌ Failed: {daily_result['error']}")
        return False

    print()

    # Step 4: Test weekly artifact convenience method
    print("4. Publishing weekly artifact...")

    weekly_markdown = """# Weekly Test Artifact

Testing the weekly artifact convenience method.

Week: 2026-W03
"""

    weekly_result = publisher.publish_weekly_artifact(
        markdown=weekly_markdown,
        category="test",
        prefix="weekly-test",
        title="Weekly Test Artifact",
        artifact_type="test",
        git_commit=False  # Don't commit this one
    )

    if weekly_result["success"]:
        print(f"   ✅ Published: {weekly_result['artifact_path']}")
        print(f"   ✅ URI: {weekly_result['artifact_uri']}")
    else:
        print(f"   ❌ Failed: {weekly_result['error']}")
        return False

    print()

    # Step 5: Verify Canon integration
    print("5. Verifying Canon integration...")

    if canon_tools:
        # Try to retrieve the artifact we just stored
        artifact = canon_tools.get("test_sprint1_artifact_publisher")
        if artifact:
            print(f"   ✅ Canon retrieval successful")
            print(f"   ✅ Title: {artifact['title']}")
            print(f"   ✅ Type: {artifact['type']}")
            print(f"   ✅ URI in metadata: {artifact.get('metadata', {}).get('artifact_uri')}")
        else:
            print(f"   ⚠️  Canon retrieval failed (artifact not found)")
    else:
        print(f"   ⚠️  Canon integration skipped (no API key)")

    print()

    # Success!
    print("=" * 60)
    print("✅ Artifact Publisher test completed successfully!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Check /artifacts/test/ folder for created files")
    print("2. Check git log for commit")
    print("3. Search Canon for 'sprint1' to verify storage")
    print()

    return True


if __name__ == "__main__":
    import sys
    success = test_artifact_publisher()
    sys.exit(0 if success else 1)
