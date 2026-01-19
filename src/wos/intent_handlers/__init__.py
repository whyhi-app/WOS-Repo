"""
WOS Intent Handlers Package (Phase 3.3)
Registry and factory for all intent handlers
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("wos.intent_handlers")

# Import handlers as they're added
from wos.intent_handlers.daily_digest import create_daily_digest_handler

# Handler registry - maps intent_id to handler factory
HANDLER_REGISTRY = {
    "daily_email_digest_v0": {
        "factory": create_daily_digest_handler,
        "name": "Daily Email Digest",
        "version": "0.1",
    },
    # Future handlers will be added here:
    # "brief_generator_v0": {...},
    # etc.
}


def get_handler(intent_id: str, n8n_executor, approval_gate=None, canon_tools=None):
    """
    Factory function to get a handler by intent_id

    Args:
        intent_id: Intent ID (e.g., "daily_email_digest_v0")
        n8n_executor: N8nExecutor instance
        approval_gate: ApprovalGate instance (optional)
        canon_tools: CanonTools instance (optional)

    Returns:
        Handler instance, or None if not found
    """

    if intent_id not in HANDLER_REGISTRY:
        logger.error(f"Handler not found for intent: {intent_id}")
        return None

    handler_config = HANDLER_REGISTRY[intent_id]
    factory = handler_config["factory"]

    try:
        # Call factory with appropriate dependencies
        # Each handler's factory decides which deps it needs
        handler = factory(n8n_executor=n8n_executor)
        logger.info(f"Created handler for {intent_id}")
        return handler
    except Exception as e:
        logger.error(f"Failed to create handler for {intent_id}: {e}", exc_info=True)
        return None


def list_handlers() -> Dict[str, Dict[str, Any]]:
    """List all available handlers"""
    return {
        intent_id: {"name": config["name"], "version": config["version"]}
        for intent_id, config in HANDLER_REGISTRY.items()
    }


def get_handler_factory(canon_tools, n8n_executor):
    """
    Returns a factory function that the Brain can use to get handlers

    Args:
        canon_tools: CanonTools instance
        n8n_executor: N8nExecutor instance

    Returns:
        Function that takes intent_id and returns handler
    """

    def factory(intent_id: str):
        return get_handler(
            intent_id=intent_id, n8n_executor=n8n_executor, canon_tools=canon_tools
        )

    return factory
