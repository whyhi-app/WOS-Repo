"""
WOS MCP Server v0.2
WhyHi Operating System - MCP Server Integration
Integrates: Brain (Phase 3.2) + Handlers (Phase 3.3) + Canon (Phase 4+4.1)

This MCP server works with Claude Code and Claude Desktop.
Implements AOS Constitution v1.0 principles.
"""
import logging
from mcp.server import Server
from mcp.types import Tool, TextContent
import os
from datetime import datetime
import json

# WOS Components (Phase 3-4)
from wos.intent_registry import IntentRegistry
from wos.brain import Brain
from wos.approval_gate import ApprovalGate
from wos.n8n_executor import N8nExecutor
from wos.canon_tools import create_canon_tools
from wos.intent_handlers import get_handler_factory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("wos")

# AOS Constitution
CONSTITUTION_VERSION = "1.0"
OPERATING_PHASE = "phase_3_4"  # Brain + Handlers + Canon operational

# ============================================================================
# WOS Components Initialization
# ============================================================================

class WOSComponents:
    """Container for all WOS components"""
    
    def __init__(self):
        logger.info("=== Initializing WOS Components ===")
        
        # Phase 4: Canon Index (Memory Layer)
        logger.info("Initializing Canon Index...")
        self.canon_tools = create_canon_tools(
            canon_db_path=os.getenv("WOS_CANON_DB_PATH", "canon.db"),
            use_semantic_search=True,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        logger.info("✅ Canon Index ready")
        
        # Phase 3.2: Intent Registry
        logger.info("Initializing Intent Registry...")
        self.intent_registry = IntentRegistry(
            db_path=os.getenv("WOS_REGISTRY_DB_PATH", "intent_registry.db")
        )
        logger.info("✅ Intent Registry ready")
        
        # Phase 3.2: n8n Executor
        logger.info("Initializing n8n Executor...")
        self.n8n_executor = N8nExecutor(
            n8n_base_url=os.getenv("N8N_URL", "https://n8n.whyhi.app"),
            api_key=os.getenv("N8N_API_KEY")
        )
        logger.info("✅ n8n Executor ready")
        
        # Phase 3.2: Approval Gate (HITL)
        logger.info("Initializing Approval Gate...")
        self.approval_gate = ApprovalGate(
            notion_db_id=os.getenv("NOTION_APPROVAL_DB_ID"),
            notion_api_key=os.getenv("NOTION_API_KEY")
        )
        logger.info("✅ Approval Gate ready")
        
        # Phase 3.3: Handler Factory
        logger.info("Initializing Handler Factory...")
        handler_factory = get_handler_factory(
            canon_tools=self.canon_tools,
            n8n_executor=self.n8n_executor
        )
        logger.info("✅ Handler Factory ready")
        
        # Phase 3.2: Brain Control Plane
        logger.info("Initializing Brain Control Plane...")
        self.brain = Brain(
            intent_registry=self.intent_registry,
            approval_gate=self.approval_gate,
            canon_tools=self.canon_tools,
            n8n_executor=self.n8n_executor,
            handler_factory=handler_factory
        )
        logger.info("✅ Brain Control Plane ready")
        
        logger.info("=== WOS Components Initialized Successfully ===\n")
    
    def get_status(self) -> dict:
        """Get detailed WOS status"""
        canon_stats = self.canon_tools.stats()
        intents = self.intent_registry.list_intents()
        
        return {
            "constitution_version": CONSTITUTION_VERSION,
            "operating_phase": OPERATING_PHASE,
            "timestamp": datetime.utcnow().isoformat(),
            "founder_authority": "active",
            "components": {
                "brain": "operational",
                "canon_index": "operational",
                "intent_registry": "operational",
                "n8n_executor": "operational",
                "approval_gate": "operational"
            },
            "canon_stats": {
                "total_artifacts": canon_stats.get("total_artifacts", 0),
                "embeddings_enabled": "embeddings" in canon_stats
            },
            "registered_intents": len(intents)
        }

# Initialize components globally
wos_components = None

def get_wos() -> WOSComponents:
    """Get or initialize WOS components"""
    global wos_components
    if wos_components is None:
        wos_components = WOSComponents()
    return wos_components

# ============================================================================
# MCP Server Definition
# ============================================================================

app = Server("wos")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    Expose WOS tools following AOS Constitution principles:
    - Reliability First
    - Determinism Over Creativity
    - Operator Supremacy
    """
    return [
        Tool(
            name="wos_status",
            description="Get current WOS operational status, component health, and Canon statistics",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="execute_intent",
            description="Execute a registered intent through WOS Brain (Phase 3.2+). Routes to appropriate handler, enforces policy gates, returns standardized response.",
            inputSchema={
                "type": "object",
                "properties": {
                    "intent": {
                        "type": "string",
                        "description": "Intent name (e.g., 'daily_digest', 'generate_brief')"
                    },
                    "inputs": {
                        "type": "object",
                        "description": "Intent-specific input parameters"
                    },
                    "request_id": {
                        "type": "string",
                        "description": "Optional request ID for tracking"
                    }
                },
                "required": ["intent"]
            }
        ),
        Tool(
            name="list_intents",
            description="List all registered intents with their descriptions and requirements",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="canon_search",
            description="Search Canon Index (Phase 4) for relevant artifacts using semantic search or text matching",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max results to return (default 5)"
                    },
                    "artifact_type": {
                        "type": "string",
                        "description": "Filter by type (optional): decision, context, brief, log, etc."
                    },
                    "category": {
                        "type": "string",
                        "description": "Filter by category (optional): product, growth, operations, finance"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="canon_store",
            description="Store an artifact in Canon Index for future retrieval",
            inputSchema={
                "type": "object",
                "properties": {
                    "artifact_id": {
                        "type": "string",
                        "description": "Unique artifact ID"
                    },
                    "title": {
                        "type": "string",
                        "description": "Human-readable title"
                    },
                    "content": {
                        "type": "string",
                        "description": "Full artifact content"
                    },
                    "artifact_type": {
                        "type": "string",
                        "description": "Type: decision, context, brief, log, etc."
                    },
                    "category": {
                        "type": "string",
                        "description": "Category: product, growth, operations, finance"
                    },
                    "summary": {
                        "type": "string",
                        "description": "Brief summary for search results"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Tags for categorization"
                    }
                },
                "required": ["artifact_id", "title", "content"]
            }
        ),
        Tool(
            name="register_intent",
            description="Register a new intent in the intent registry (Founder authority required)",
            inputSchema={
                "type": "object",
                "properties": {
                    "intent_id": {
                        "type": "string",
                        "description": "Unique intent identifier"
                    },
                    "name": {
                        "type": "string",
                        "description": "Human-readable name"
                    },
                    "description": {
                        "type": "string",
                        "description": "What this intent does"
                    },
                    "handler": {
                        "type": "string",
                        "description": "Handler class name"
                    },
                    "approval_required": {
                        "type": "boolean",
                        "description": "Whether this intent requires HITL approval"
                    },
                    "n8n_workflow_id": {
                        "type": "string",
                        "description": "Optional n8n workflow ID to execute"
                    }
                },
                "required": ["intent_id", "name", "description", "handler"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Execute WOS tools following AOS Security & Trust Model
    """
    logger.info(f"Tool called: {name}")
    
    try:
        if name == "wos_status":
            return await handle_wos_status()
        elif name == "execute_intent":
            return await handle_execute_intent(arguments)
        elif name == "list_intents":
            return await handle_list_intents()
        elif name == "canon_search":
            return await handle_canon_search(arguments)
        elif name == "canon_store":
            return await handle_canon_store(arguments)
        elif name == "register_intent":
            return await handle_register_intent(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
    except Exception as e:
        logger.error(f"Tool execution failed: {e}", exc_info=True)
        return [TextContent(
            type="text",
            text=f"ERROR: {str(e)}"
        )]

# ============================================================================
# Tool Handlers
# ============================================================================

async def handle_wos_status() -> list[TextContent]:
    """Return current WOS operational status"""
    wos = get_wos()
    status = wos.get_status()
    
    return [TextContent(
        type="text",
        text=f"WOS Status Report:\n\n{json.dumps(status, indent=2)}"
    )]

async def handle_execute_intent(args: dict) -> list[TextContent]:
    """
    Execute intent through Brain
    Following Phase 3.2 Brain_Run_Response_v0 envelope
    """
    wos = get_wos()
    
    intent = args.get("intent")
    inputs = args.get("inputs", {})
    request_id = args.get("request_id", f"req_{datetime.utcnow().timestamp()}")
    
    logger.info(f"Executing intent: {intent}")
    
    # Build Brain request
    brain_request = {
        "request_id": request_id,
        "intent": intent,
        "input": inputs
    }
    
    # Process through Brain
    response = wos.brain.process_request(brain_request)
    
    # Format response
    status = response.get("status")
    
    if status == "Completed":
        result = response.get("output", {})
        return [TextContent(
            type="text",
            text=f"✅ Intent '{intent}' completed successfully\n\n{json.dumps(result, indent=2)}"
        )]
    elif status == "PendingApproval":
        return [TextContent(
            type="text",
            text=f"⏸️ Intent '{intent}' requires approval\n\nReason: {response.get('human_readable_reason', 'Approval required')}\n\nRequest ID: {request_id}"
        )]
    elif status == "Failed":
        return [TextContent(
            type="text",
            text=f"❌ Intent '{intent}' failed\n\nError: {response.get('error_code', 'Unknown')}\nMessage: {response.get('human_readable_reason', 'Unknown error')}"
        )]
    else:
        return [TextContent(
            type="text",
            text=f"Status: {status}\n\n{json.dumps(response, indent=2)}"
        )]

async def handle_list_intents() -> list[TextContent]:
    """List all registered intents"""
    wos = get_wos()
    intents = wos.intent_registry.list_intents()
    
    if not intents:
        return [TextContent(
            type="text",
            text="No intents registered yet."
        )]
    
    intent_list = "\n\n".join([
        f"**{intent['name']}** (`{intent['intent_id']}`)\n"
        f"Description: {intent['description']}\n"
        f"Handler: {intent['handler']}\n"
        f"Approval Required: {intent.get('approval_required', False)}"
        for intent in intents
    ])
    
    return [TextContent(
        type="text",
        text=f"Registered Intents ({len(intents)}):\n\n{intent_list}"
    )]

async def handle_canon_search(args: dict) -> list[TextContent]:
    """Search Canon Index"""
    wos = get_wos()
    
    query = args.get("query")
    limit = args.get("limit", 5)
    artifact_type = args.get("artifact_type")
    category = args.get("category")
    
    logger.info(f"Canon search: {query}")
    
    results = wos.canon_tools.search(
        query=query,
        limit=limit,
        artifact_type=artifact_type,
        category=category
    )
    
    if not results:
        return [TextContent(
            type="text",
            text=f"No artifacts found for query: '{query}'"
        )]
    
    results_text = "\n\n".join([
        f"**{r['title']}** (ID: {r['artifact_id']})\n"
        f"Type: {r['type']} | Category: {r.get('category', 'N/A')}\n"
        f"Relevance: {r.get('relevance_score', 0):.1f}/10\n"
        f"Summary: {r.get('summary', 'N/A')}"
        for r in results
    ])
    
    return [TextContent(
        type="text",
        text=f"Canon Search Results ({len(results)}):\n\n{results_text}"
    )]

async def handle_canon_store(args: dict) -> list[TextContent]:
    """Store artifact in Canon"""
    wos = get_wos()
    
    artifact_id = args.get("artifact_id")
    title = args.get("title")
    content = args.get("content")
    artifact_type = args.get("artifact_type", "document")
    category = args.get("category")
    summary = args.get("summary")
    tags = args.get("tags", [])
    
    logger.info(f"Storing artifact: {artifact_id}")
    
    success = wos.canon_tools.store(
        artifact_id=artifact_id,
        title=title,
        content=content,
        artifact_type=artifact_type,
        category=category,
        summary=summary,
        tags=tags
    )
    
    if success:
        return [TextContent(
            type="text",
            text=f"✅ Artifact '{artifact_id}' stored successfully in Canon Index"
        )]
    else:
        return [TextContent(
            type="text",
            text=f"❌ Failed to store artifact '{artifact_id}'"
        )]

async def handle_register_intent(args: dict) -> list[TextContent]:
    """Register new intent (Founder authority)"""
    wos = get_wos()
    
    intent_id = args.get("intent_id")
    name = args.get("name")
    description = args.get("description")
    handler = args.get("handler")
    approval_required = args.get("approval_required", False)
    n8n_workflow_id = args.get("n8n_workflow_id")
    
    logger.info(f"Registering intent: {intent_id}")
    
    success = wos.intent_registry.register_intent(
        intent_id=intent_id,
        name=name,
        description=description,
        required_inputs=[],  # TODO: Parse from args
        handler=handler,
        approval_required=approval_required,
        n8n_workflow_id=n8n_workflow_id
    )
    
    if success:
        return [TextContent(
            type="text",
            text=f"✅ Intent '{intent_id}' registered successfully"
        )]
    else:
        return [TextContent(
            type="text",
            text=f"❌ Failed to register intent '{intent_id}'"
        )]

# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    import asyncio
    from mcp.server.stdio import stdio_server
    
    async def main():
        """Run MCP server with WOS integration"""
        logger.info("\n" + "="*60)
        logger.info("WOS MCP SERVER STARTING")
        logger.info("="*60 + "\n")
        
        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
    
    asyncio.run(main())
