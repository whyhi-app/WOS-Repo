#!/usr/bin/env python3
"""
Test script to execute daily_email_digest intent directly
"""
import os
import sys
import json
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from wos.intent_registry import IntentRegistry
from wos.brain import Brain
from wos.approval_gate import ApprovalGate
from wos.n8n_executor import N8nExecutor
from wos.canon_tools import create_canon_tools
from wos.intent_handlers import get_handler_factory

def test_daily_digest():
    """Test daily digest execution"""

    print("=== Testing Daily Email Digest Intent ===\n")

    # Initialize components
    print("Initializing components...")
    intent_registry = IntentRegistry(db_path="intent_registry.db")
    n8n_executor = N8nExecutor(
        n8n_base_url=os.getenv("N8N_URL", "https://n8n.whyhi.app"),
        api_key=os.getenv("N8N_API_KEY")
    )
    approval_gate = ApprovalGate(
        notion_db_id=os.getenv("NOTION_APPROVAL_DB_ID"),
        notion_api_key=os.getenv("NOTION_API_KEY")
    )
    canon_tools = create_canon_tools(
        canon_db_path="canon.db",
        use_semantic_search=True,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    handler_factory = get_handler_factory(
        canon_tools=canon_tools,
        n8n_executor=n8n_executor
    )

    brain = Brain(
        intent_registry=intent_registry,
        approval_gate=approval_gate,
        canon_tools=canon_tools,
        n8n_executor=n8n_executor,
        handler_factory=handler_factory
    )

    print("✓ Components initialized\n")

    # Build request
    request = {
        "request_id": f"test_{datetime.utcnow().timestamp()}",
        "intent": "daily_email_digest",  # Use name, not intent_id
        "input": {}
    }

    print(f"Executing intent: {request['intent']}")
    print(f"Request ID: {request['request_id']}\n")

    # Execute
    response = brain.process_request(request)

    # Display result
    print("=== Response ===")
    print(json.dumps(response, indent=2))

    if response.get("status") == "Completed":
        print("\n✅ Intent executed successfully!")
    else:
        print(f"\n❌ Intent failed with status: {response.get('status')}")

if __name__ == "__main__":
    test_daily_digest()
