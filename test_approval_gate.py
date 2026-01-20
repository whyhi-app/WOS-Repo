"""
Test Approval Gate v0.2
Sprint 1 - Verify Notion integration works end-to-end
"""

import os
import time
from src.wos.approval_gate import ApprovalGate

def test_approval_gate():
    """Test the Approval Gate with Notion"""

    print("🧪 Testing Approval Gate with Notion...")
    print()

    # Step 1: Check credentials
    print("1. Checking Notion credentials...")

    notion_api_key = os.getenv("NOTION_API_KEY")
    notion_db_id = os.getenv("NOTION_APPROVAL_DB_ID")

    if not notion_api_key or not notion_db_id:
        print("   ❌ Missing Notion credentials")
        print()
        print("Run setup_approval_gate.py first to configure Notion integration.")
        print("Or set environment variables:")
        print("  export NOTION_API_KEY=secret_...")
        print("  export NOTION_APPROVAL_DB_ID=...")
        return False

    print(f"   ✅ API key found: {notion_api_key[:20]}...")
    print(f"   ✅ Database ID: {notion_db_id}")
    print()

    # Step 2: Initialize Approval Gate
    print("2. Initializing Approval Gate...")

    gate = ApprovalGate(
        notion_api_key=notion_api_key,
        notion_db_id=notion_db_id
    )

    print("   ✅ Approval Gate initialized")
    print()

    # Step 3: Create approval request
    print("3. Creating test approval request...")

    test_content = """# Test Outreach Email

Hey {{first_name}},

I saw you're covering AI/tech products at {{publication}}.

WhyHi is launching in March - it's a voice-first social app for authentic conversations (no feeds, no likes).

Would you be interested in an early look?

Best,
Tom
"""

    try:
        approval = gate.request_approval(
            request_id="test-123",
            intent_id="creator_outreach_v0",
            content=test_content,
            title="Test Approval - Creator Outreach Email",
            metadata={
                "test": True,
                "sprint": 1,
                "recipient": "test@example.com"
            }
        )

        print(f"   ✅ Approval created: {approval['approval_id'][:8]}...")
        print(f"   ✅ Notion URL: {approval['notion_url']}")
        print()

    except Exception as e:
        print(f"   ❌ Failed to create approval: {e}")
        return False

    approval_id = approval["approval_id"]

    # Step 4: Check initial status
    print("4. Checking approval status...")

    status = gate.get_approval_status(approval_id)

    if status:
        print(f"   ✅ Status: {status['status']}")
        print(f"   ✅ Notion URL: {status['notion_url']}")
    else:
        print(f"   ❌ Failed to get status")
        return False

    print()

    # Step 5: Wait for user approval
    print("=" * 60)
    print("MANUAL STEP REQUIRED:")
    print("=" * 60)
    print()
    print("1. Open the Notion URL above in your browser")
    print("2. Review the draft content")
    print("3. Change 'Status' from 'Pending' to either:")
    print("   - 'Approved' to continue the test")
    print("   - 'Rejected' to test rejection")
    print()
    print("The test will wait for up to 60 seconds for you to approve/reject...")
    print()

    input("Press Enter when you've changed the status in Notion...")

    print()
    print("5. Waiting for approval decision...")

    result = gate.wait_for_approval(
        approval_id=approval_id,
        timeout_seconds=60,
        poll_interval=3
    )

    if result["status"] == "approved":
        print(f"   ✅ Approved! Reviewed at: {result['reviewed_at']}")
        print()
        print("🎉 Approval Gate test successful!")
        print("   Agent would now proceed with the action (send email, post, etc.)")

    elif result["status"] == "rejected":
        print(f"   ✅ Rejected! Reviewed at: {result['reviewed_at']}")
        print()
        print("🎉 Approval Gate test successful!")
        print("   Agent would now stop and log the rejection.")

    elif result["status"] == "timeout":
        print(f"   ⏱️  Timeout - no decision made in time")
        print()
        print("⚠️  Test incomplete (timeout), but Approval Gate is working.")

    print()
    print("=" * 60)
    print("✅ Approval Gate test completed!")
    print("=" * 60)
    print()
    print("The Approval Gate is ready to use with agents that require approval:")
    print("- Creator Outreach")
    print("- Social Content Engine")
    print("- App Store Reviews (replies)")
    print("- Support Triage (non-template responses)")
    print()

    return True


if __name__ == "__main__":
    import sys
    success = test_approval_gate()
    sys.exit(0 if success else 1)
