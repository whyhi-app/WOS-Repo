"""
WOS MCP Server
Implements the WhyHi Operating System as defined in AOS v1.0
"""
import logging
from mcp.server import Server
from mcp.types import Tool, TextContent
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("wos")

# Initialize MCP Server
app = Server("wos")

# AOS Constitution Principles
CONSTITUTION_VERSION = "1.0"
OPERATING_PHASE = "bootstrap"  # Will evolve through phases

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
            description="Get current WOS operational status and configuration",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="execute_n8n_workflow",
            description="Execute an n8n workflow via REST API (Founder-authorized only)",
            inputSchema={
                "type": "object",
                "properties": {
                    "workflow_id": {
                        "type": "string",
                        "description": "The n8n workflow ID to execute"
                    },
                    "payload": {
                        "type": "object",
                        "description": "Data payload to send to the workflow"
                    }
                },
                "required": ["workflow_id"]
            }
        ),
        Tool(
            name="log_event",
            description="Record an AOS-compliant audit event",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_type": {
                        "type": "string",
                        "description": "Type of event (task_start, task_complete, violation, etc.)"
                    },
                    "details": {
                        "type": "object",
                        "description": "Event details"
                    }
                },
                "required": ["event_type", "details"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Execute WOS tools following AOS Security & Trust Model
    """
    logger.info(f"Tool called: {name} with arguments: {arguments}")
    
    if name == "wos_status":
        return await get_wos_status()
    elif name == "execute_n8n_workflow":
        return await execute_n8n_workflow(arguments)
    elif name == "log_event":
        return await log_event(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")

async def get_wos_status() -> list[TextContent]:
    """Return current WOS operational status"""
    status = {
        "constitution_version": CONSTITUTION_VERSION,
        "operating_phase": OPERATING_PHASE,
        "timestamp": datetime.utcnow().isoformat(),
        "founder_authority": "active",
        "agent_registry_initialized": False,  # TODO: Implement
        "memory_system_initialized": False     # TODO: Implement
    }
    
    return [TextContent(
        type="text",
        text=f"WOS Status:\n{status}"
    )]

async def execute_n8n_workflow(args: dict) -> list[TextContent]:
    """
    Execute n8n workflow via REST API
    Following AOS Security Model: explicit authorization required
    """
    import requests
    
    workflow_id = args["workflow_id"]
    payload = args.get("payload", {})
    
    # TODO: Load from .env
    n8n_url = os.getenv("N8N_URL", "https://n8n.whyhi.app")
    n8n_api_key = os.getenv("N8N_API_KEY")
    
    if not n8n_api_key:
        return [TextContent(
            type="text",
            text="ERROR: N8N_API_KEY not configured. Founder authorization required."
        )]
    
    try:
        # Call n8n webhook endpoint
        response = requests.post(
            f"{n8n_url}/webhook/{workflow_id}",
            json=payload,
            headers={"Authorization": f"Bearer {n8n_api_key}"}
        )
        
        return [TextContent(
            type="text",
            text=f"Workflow {workflow_id} executed. Status: {response.status_code}\nResponse: {response.text}"
        )]
    except Exception as e:
        logger.error(f"Workflow execution failed: {e}")
        return [TextContent(
            type="text",
            text=f"ERROR: Workflow execution failed: {str(e)}"
        )]

async def log_event(args: dict) -> list[TextContent]:
    """
    Log AOS-compliant audit event
    Following AOS Memory & Observability Specification
    """
    event_type = args["event_type"]
    details = args["details"]
    
    # TODO: Implement proper SQLite logging
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "details": details
    }
    
    logger.info(f"Event logged: {log_entry}")
    
    return [TextContent(
        type="text",
        text=f"Event logged: {event_type}"
    )]

if __name__ == "__main__":
    import asyncio
    from mcp.server.stdio import stdio_server
    
    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await app.run(read_stream, write_stream, app.create_initialization_options())
    
    asyncio.run(main())
