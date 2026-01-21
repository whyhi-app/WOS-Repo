# WOS Context Documentation

**Purpose:** Canonical knowledge base for understanding WOS architecture, patterns, and implementation
**Last Updated:** January 20, 2026
**Version:** Phase 3.4 (MCP + Brain + Handlers + Canon operational)

---

## Table of Contents
1. [System Architecture](#system-architecture)
2. [Tech Stack](#tech-stack)
3. [Design Decisions](#design-decisions)
4. [Agent Patterns](#agent-patterns)
5. [Integration Details](#integration-details)
6. [Common Commands](#common-commands)
7. [Key Constraints](#key-constraints)
8. [Development Workflow](#development-workflow)

---

## System Architecture

### Overview
WOS (WhyHi Operating System) is an autonomous agent orchestration platform built on MCP (Model Context Protocol). It enables both WOS-managed agents (triggered by Brain control plane) and autonomous agents (triggered by external events via n8n).

### Core Flow: MCP → Brain → Handler → n8n

```
┌─────────────────────────────────────────────────────────────┐
│                    EXECUTION FLOW                            │
└─────────────────────────────────────────────────────────────┘

WOS-Managed Agents:
  Claude Code / claude.ai
         ↓
  MCP Server (server.py)
         ↓
  Brain Control Plane (brain.py)
         ↓
  Intent Handler (e.g., daily_newsletter_digest.py)
         ↓
  n8n Executor (n8n_executor.py)
         ↓
  n8n Workflow (external automation platform)
         ↓
  Result → Artifact Publisher → Canon Index

Autonomous Agents:
  External Trigger (email, webhook, cron)
         ↓
  n8n Workflow (standalone execution)
         ↓
  Target System (Notion, Gmail, etc.)

  Note: Still registered in Intent Registry for inventory tracking
```

### Components

#### 1. MCP Server (`src/wos/server.py`)
- Exposes WOS tools to Claude instances via Model Context Protocol
- Runs as stdio server: `python3 src/wos/server.py`
- Configured in `.mcp.json` for Claude Code integration
- Tools exposed:
  - `wos_status` - System health check
  - `execute_intent` - Run WOS-managed agents
  - `list_intents` - View registered agents
  - `canon_search` - Query Canon Index
  - `canon_store` - Store artifacts
  - `register_intent` - Add new agents (founder authority)

#### 2. Brain Control Plane (`src/wos/brain.py`)
- Routes intent execution requests
- Enforces policy gates (approval requirements, workflow builder restrictions)
- Validates inputs and handles errors
- Returns standardized `Brain_Run_Response_v0` envelope
- Logs all executions for audit trail

**Brain Request Schema:**
```json
{
  "request_id": "string",
  "intent": "string (e.g., 'daily_newsletter_digest')",
  "input": {},
  "mode": "string (optional)",
  "wb_stage": "string (optional)"
}
```

**Brain Response Schema:**
```json
{
  "ok": true/false,
  "status": "Completed|Failed|Paused|PendingApproval",
  "request_id": "string",
  "execution_id": "string",
  "resolved_intent": "string",
  "intent_id": "string",
  "result": {},
  "timestamp": "ISO-8601",
  "errors": []
}
```

#### 3. Intent Registry (`src/wos/intent_registry.py`)
- SQLite database (`intent_registry.db`) tracking all agents
- Schema:
  - `intents` - Intent definitions, approval policies, execution modes
  - `n8n_workflows` - Workflow mappings
  - `intent_executions` - Audit log
  - `policy_rules` - Policy enforcement rules

**Execution Modes:**
- `wos_managed` - Brain triggers (e.g., daily digest, creator outreach)
- `autonomous_cron` - n8n cron trigger (e.g., monitoring dashboards)
- `autonomous_webhook` - External trigger (e.g., Gmail to Notion, iOS shortcuts)
- `manual` - Human triggers in n8n UI

#### 4. Intent Handlers (`src/wos/intent_handlers/`)
- Python modules implementing agent logic
- Standard interface:
  - `execute(request_id, execution_id, intent_input, intent_record) -> Dict`
  - `validate_input(intent_input) -> bool` (optional)
- Handler factory pattern in `__init__.py`
- Example: `daily_newsletter_digest.py`, `creator_outreach.py`

#### 5. n8n Executor (`src/wos/n8n_executor.py`)
- Calls n8n workflows via REST API
- Environment: `N8N_URL=https://n8n.whyhi.app`, `N8N_API_KEY`
- Timeout handling, error mapping

#### 6. Canon Index (`src/wos/canon_index.py`, `canon_tools.py`, `canon_embeddings.py`)
- SQLite database (`canon.db`) storing organizational memory
- Semantic search powered by OpenAI embeddings
- Stores: decisions, briefs, logs, agent outputs
- Schema:
  - `artifacts` - Content storage
  - `artifact_embeddings` - Vector search
  - `artifact_metadata` - Tags, categories

#### 7. Artifact Publisher (`src/wos/artifact_publisher.py`)
- Sprint 1 infrastructure utility
- Writes markdown to `/artifacts/<category>/<filename>.md`
- Records artifact URI in Canon Index
- Optional git commit
- Convenience methods: `publish_daily_artifact()`, `publish_weekly_artifact()`

#### 8. Approval Gate (`src/wos/approval_gate.py`)
- Sprint 1 HITL (Human-In-The-Loop) infrastructure
- Creates approval requests as Notion pages
- Polls for approval/rejection status
- Timeout handling (default 1 hour)
- Methods:
  - `request_approval()` - Create Notion page with "Pending" status
  - `wait_for_approval()` - Poll until status changes
  - `get_approval_status()` - Check current status

---

## Tech Stack

### Core Dependencies (`requirements.txt`)
- `mcp>=1.0.0` - Model Context Protocol
- `anthropic>=0.40.0` - Claude API
- `python-dotenv>=1.0.0` - Environment config
- `requests>=2.31.0` - HTTP requests
- `sqlite3-python>=1.0.0` - Database
- `notion-client>=2.0.0` - Notion API

### External Integrations
- **n8n** (`https://n8n.whyhi.app`) - Workflow automation platform
- **Notion** - CRM, approval queue, task management
- **OpenAI** - Embeddings for semantic search
- **Gmail** - Email ingestion/sending (via n8n)
- **Mixpanel** (planned) - Analytics

### File Structure
```
WOS-Repo/
├── .mcp.json                      # MCP server config
├── .env                           # Environment variables (gitignored)
├── .git/hooks/                    # Git hooks
├── artifacts/                     # Published agent outputs
│   └── <category>/
│       └── <filename>.md
├── docs/
│   ├── WOS_Status.md              # Project status, sprint progress
│   └── WOS_Context.md             # This file - architecture/patterns
├── packs/
│   └── P3.2/
│       ├── SCHEMAS.json           # Data schemas
│       └── WORKFLOWS/             # n8n workflow JSONs
│           ├── wos_brain_controlplane_v0.json
│           ├── wos_intent_daily_newsletter_digest_v0.json
│           ├── gmail_to_notion_task_v0_fixed.json
│           ├── apple_reminders_to_notion_sync_v0_fixed.json
│           └── creator_capture_v0.json
├── registry/
│   └── intent_registry.v0.json    # Initial intent definitions
├── src/wos/
│   ├── server.py                  # MCP server
│   ├── brain.py                   # Brain control plane
│   ├── intent_registry.py         # Intent database
│   ├── n8n_executor.py            # n8n integration
│   ├── canon_index.py             # Canon database
│   ├── canon_tools.py             # Canon retrieval
│   ├── canon_embeddings.py        # Semantic search
│   ├── artifact_publisher.py      # Artifact handling
│   ├── approval_gate.py           # HITL approval
│   ├── config.py                  # Configuration
│   └── intent_handlers/           # Agent implementations
│       ├── __init__.py
│       ├── daily_newsletter_digest.py
│       └── creator_outreach.py
├── canon.db                       # Canon Index database
├── intent_registry.db             # Intent Registry database
└── requirements.txt
```

### Environment Variables (`.env`)
```bash
# Core
WOS_CANON_DB_PATH=canon.db
WOS_REGISTRY_DB_PATH=intent_registry.db

# n8n
N8N_URL=https://n8n.whyhi.app
N8N_API_KEY=<your-key>

# Notion
NOTION_API_KEY=<your-key>
NOTION_APPROVAL_DB_ID=<database-id>
NOTION_CRM_DB_ID=<database-id>

# OpenAI (for embeddings)
OPENAI_API_KEY=<your-key>
```

---

## Design Decisions

### 1. Autonomous vs Managed Execution Modes
**Decision:** Support both WOS-managed and autonomous agents

**Rationale:**
- **WOS-Managed** (`wos_managed`): Brain triggers for complex workflows requiring approval, Canon retrieval, or multi-step orchestration
  - Example: Creator outreach (approval required), brief generation
- **Autonomous** (`autonomous_cron`, `autonomous_webhook`): Simple trigger → action workflows that don't need Brain overhead
  - Example: Gmail → Notion task, iOS shortcuts, cron monitoring
- **Benefit:** Reduces Claude API costs for simple automations while maintaining central registry for observability

### 2. SQLite for Registry + Canon
**Decision:** Use SQLite instead of cloud database

**Rationale:**
- Single-founder startup, low concurrency requirements
- File-based = simple backups (git commits)
- Zero infrastructure cost
- Fast local queries
- Easy migration path to Postgres later if needed

### 3. n8n for Workflow Execution
**Decision:** Delegate workflow execution to n8n instead of pure Python

**Rationale:**
- Visual workflow builder for non-technical adjustments
- Built-in integrations (Gmail, Notion, Slack, etc.)
- Error handling, retry logic, scheduling included
- Brain delegates to n8n via API calls
- Cost-effective (self-hosted at n8n.whyhi.app)

### 4. Notion for Approval Queue
**Decision:** Use Notion database for HITL approvals instead of custom UI

**Rationale:**
- Already using Notion for CRM, tasks, docs
- Native mobile app for on-the-go approvals
- Database views for filtering (Pending, Approved, Rejected)
- Rich content embedding (code blocks, metadata)
- Zero frontend development needed

### 5. Artifact Publisher Pattern
**Decision:** Centralized utility for all agent outputs

**Rationale:**
- Prevents inconsistent file handling across agents
- Guaranteed Canon Index integration
- Automatic git commits for version control
- Standardized paths: `/artifacts/<category>/<filename>.md`
- Reduces boilerplate in agent handlers

### 6. MCP over Direct API Calls
**Decision:** Build MCP server instead of direct Claude API integration

**Rationale:**
- Works with both Claude Code CLI and claude.ai web interface
- Future-proof: MCP is Anthropic's official protocol
- Context management handled by MCP (no manual conversation state)
- Tool use standardization
- Better developer experience

### 7. URL-Based Extraction for Social Platforms
**Decision:** Extract creator info from URLs directly instead of fetching page content

**Rationale:**
- Social platforms (YouTube, Instagram, LinkedIn, Facebook) have anti-scraping protections that cause 301 redirects and login walls
- Profile URLs contain enough info to extract handles, names, and platform type
- "Capture now, process later" workflow: Save URLs immediately, let user manually add details during batch processing
- Avoids complexity of browser automation, proxies, or API quotas
- Fast, reliable, and cost-free extraction
- Workflow: Creator Capture saves URL + basic info → User reviews/enriches → Creator Outreach generates personalized messages

**Implementation:** `creator_capture_v0_simple.json` uses JavaScript URL parsing only (no HTTP requests)

---

## Agent Patterns

### Standard Agent Structure

#### WOS-Managed Agent (Brain-Triggered)

**1. Intent Definition** (register in `intent_registry.py`):
```python
{
    "intent_id": "my_agent_v0",
    "name": "my_agent",
    "version": "0.1",
    "description": "What this agent does",
    "handler_module": "wos.intent_handlers.my_agent",
    "approval_required": True/False,
    "timeout_seconds": 60,
    "execution_mode": "wos_managed",
    "notes": "Additional context"
}
```

**2. Intent Handler** (`src/wos/intent_handlers/my_agent.py`):
```python
import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger("wos.intent_handlers.my_agent")

class MyAgentHandler:
    def __init__(self, n8n_executor, approval_gate=None, canon_tools=None, artifact_publisher=None):
        self.n8n_executor = n8n_executor
        self.approval_gate = approval_gate
        self.canon_tools = canon_tools
        self.artifact_publisher = artifact_publisher

    def execute(self, request_id: str, execution_id: str,
                intent_input: Dict[str, Any],
                intent_record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute agent logic

        Returns:
        {
            "status": "success" | "failed",
            "result": {...},
            "error": str (if failed),
            "error_code": str (if failed),
            "execution_time_ms": int
        }
        """
        start_time = datetime.utcnow()

        try:
            # Step 1: Retrieve context from Canon (if needed)
            if self.canon_tools:
                context = self.canon_tools.search(query="relevant context", limit=5)

            # Step 2: Execute core logic (often via n8n)
            result = self.n8n_executor.execute_workflow(
                workflow_name="My_Workflow_Name",
                payload={"request_id": request_id, ...},
                timeout_seconds=120
            )

            # Step 3: Request approval if required
            if intent_record.get("approval_required"):
                approval = self.approval_gate.request_approval(
                    request_id=request_id,
                    intent_id=intent_record["intent_id"],
                    content=result.get("draft_content"),
                    title="Review My Agent Output"
                )

                # Wait for approval (blocking)
                approval_result = self.approval_gate.wait_for_approval(
                    approval_id=approval["approval_id"],
                    timeout_seconds=600
                )

                if not approval_result.get("approved"):
                    return {
                        "status": "failed",
                        "error": "Approval rejected or timeout",
                        "error_code": "APPROVAL_REJECTED"
                    }

            # Step 4: Publish artifact
            if self.artifact_publisher:
                artifact = self.artifact_publisher.publish_daily_artifact(
                    markdown=result.get("output_markdown"),
                    category="my_category",
                    prefix="my-agent",
                    title="My Agent Output",
                    artifact_type="agent_output"
                )

            # Step 5: Return success
            execution_time_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            return {
                "status": "success",
                "result": {
                    "artifact_uri": artifact.get("artifact_uri"),
                    "execution_id": execution_id
                },
                "execution_time_ms": execution_time_ms
            }

        except Exception as e:
            logger.error(f"Handler error: {e}", exc_info=True)
            execution_time_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            return {
                "status": "failed",
                "error": str(e),
                "error_code": "HANDLER_ERROR",
                "execution_time_ms": execution_time_ms
            }

    def validate_input(self, intent_input: Dict[str, Any]) -> bool:
        """Validate input parameters"""
        # Check required fields
        return True

# Factory function
def create_my_agent_handler(n8n_executor, approval_gate=None, canon_tools=None):
    return MyAgentHandler(n8n_executor, approval_gate, canon_tools)
```

**3. Register in Handler Factory** (`src/wos/intent_handlers/__init__.py`):
```python
from .my_agent import create_my_agent_handler

def get_handler_factory(canon_tools, n8n_executor):
    def handler_factory(intent_id, n8n_executor, approval_gate, canon_tools):
        if intent_id == "my_agent_v0":
            return create_my_agent_handler(n8n_executor, approval_gate, canon_tools)
        # ... other handlers
    return handler_factory
```

**4. n8n Workflow** (export JSON to `packs/P3.2/WORKFLOWS/`):
- Webhook trigger (for Brain to call)
- Business logic nodes
- Return structured JSON response

#### Autonomous Agent (Event-Triggered)

**1. Intent Definition** (for tracking only):
```python
{
    "intent_id": "auto_agent_v0",
    "name": "auto_agent",
    "version": "0.1",
    "description": "What this agent does",
    "handler_module": "none",  # No Brain handler needed
    "approval_required": False,
    "timeout_seconds": 30,
    "execution_mode": "autonomous_webhook",
    "notes": "Triggered by <external trigger>. Does <action>."
}
```

**2. n8n Workflow Only**:
- External trigger (webhook, cron, email poll)
- Business logic
- Target system integration (Notion, Gmail, etc.)
- No Brain involvement

---

## Integration Details

### n8n Setup

**1. Access:**
- URL: `https://n8n.whyhi.app`
- API Key: Set in `.env` as `N8N_API_KEY`

**2. Workflow Naming Convention:**
- WOS-managed: `Intent_Name` (e.g., `Daily_Newsletter_Digest`)
- Autonomous: `<trigger>_to_<target>_<version>` (e.g., `gmail_to_notion_task_v0`)

**3. Webhook Pattern for WOS-Managed:**
```
1. Webhook node (POST)
2. Receive: { request_id, execution_id, triggered_by, timestamp, ...custom }
3. Business logic nodes
4. Respond node: { status: "success", result: {...} }
```

**4. Import/Export:**
- Export workflows to JSON: `packs/P3.2/WORKFLOWS/`
- Import via n8n UI or API
- Version workflows (v0, v1, etc.)

### Notion Setup

**1. Approval Queue Database:**
- Database ID: Set in `.env` as `NOTION_APPROVAL_DB_ID`
- Schema:
  - `Name` (Title) - Human-readable approval title
  - `Status` (Select) - Pending, Approved, Rejected
  - `Request ID` (Text) - WOS request ID
  - `Intent` (Text) - Intent ID
- Page content blocks:
  - Heading: "Content Requiring Approval"
  - Code block: Draft content (markdown)
  - Heading: "Metadata"
  - Code block: JSON metadata

**2. CRM Database (Creator Outreach):**
- Database ID: Set in `.env` as `NOTION_CRM_DB_ID`
- Schema:
  - `Name` (Title) - Creator name
  - `Platform` (Select) - Twitter, Instagram, YouTube, etc.
  - `URL` (URL) - Original content link
  - `Contact Method` (Select) - DM, Email
  - `Outreach Status` (Select) - New Lead, Draft Ready, Outreach Sent, Replied, etc.
  - `Sending Email` (Email) - Email address for sending (if applicable)

### MCP Configuration

**1. Claude Code Setup** (`.mcp.json`):
```json
{
  "mcpServers": {
    "wos": {
      "type": "stdio",
      "command": "python3",
      "args": ["/Users/tomwynn/Documents/WhyHi_Server/WOS-Repo/src/wos/server.py"],
      "env": {}
    }
  }
}
```

**2. Usage:**
- Start Claude Code: `claude` (in repo directory)
- MCP server auto-starts
- Tools available immediately
- Example: `execute the daily_newsletter_digest intent`

### Canon Index Usage

**1. Store Artifact:**
```python
from wos.canon_tools import create_canon_tools

canon = create_canon_tools(
    canon_db_path="canon.db",
    use_semantic_search=True,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

canon.store(
    artifact_id="product_decision_2026_01",
    title="Decision: Switch to Notion for Approvals",
    content="Full markdown content...",
    artifact_type="decision",
    category="product",
    summary="Brief summary for search results",
    tags=["architecture", "approval-gate"],
    auto_embed=True  # Generate embeddings for semantic search
)
```

**2. Search Canon:**
```python
results = canon.search(
    query="approval workflow decisions",
    limit=5,
    artifact_type="decision",
    category="product"
)

for r in results:
    print(f"{r['title']} - Relevance: {r['relevance_score']}/10")
    print(r['summary'])
```

---

## Common Commands

### Execute Agents (via Claude Code)

**WOS-Managed Agents:**
```bash
# Start Claude Code
~/.local/bin/claude

# Execute intent (natural language)
execute the daily_newsletter_digest intent

# Execute with parameters
execute the creator_outreach intent with status_filter='Draft Ready' and limit=2
```

**Autonomous Agents:**
- Triggered automatically by external events
- No manual execution needed
- Monitor in n8n UI: `https://n8n.whyhi.app`

### Direct MCP Tool Calls (Advanced)

**List registered intents:**
```python
# Via MCP tool: list_intents
```

**Check WOS status:**
```python
# Via MCP tool: wos_status
```

**Search Canon:**
```python
# Via MCP tool: canon_search
# Arguments: { query: "search term", limit: 5 }
```

### Database Queries

**View registered intents:**
```bash
sqlite3 intent_registry.db "SELECT intent_id, name, execution_mode, approval_required FROM intents;"
```

**View execution log:**
```bash
sqlite3 intent_registry.db "SELECT execution_id, intent_id, status, timestamp FROM intent_executions ORDER BY timestamp DESC LIMIT 10;"
```

**View Canon artifacts:**
```bash
sqlite3 canon.db "SELECT artifact_id, title, type, category FROM artifacts ORDER BY created_at DESC LIMIT 10;"
```

### Git Workflow

**Commit agent outputs:**
```bash
git add artifacts/
git commit -m "Add <agent> outputs for <date>"
```

**Commit n8n workflows:**
```bash
git add packs/P3.2/WORKFLOWS/<workflow>.json
git commit -m "Add <workflow> n8n workflow"
```

---

## Key Constraints

### Budget Limits
- **Claude API:** ~$100/month budget → Use autonomy sparingly, prefer n8n for simple tasks
- **OpenAI Embeddings:** ~$10/month → Auto-embed only important artifacts
- **n8n:** Self-hosted, fixed cost
- **Notion:** Free tier, 1000 blocks/month → Clean up approval queue regularly

### API Rate Limits
- **Notion API:** 3 requests/second → Batch operations when possible
- **Gmail API (via n8n):** 250 quota units/day → Poll Gmail twice daily, not hourly
- **OpenAI Embeddings:** 3000 requests/minute (ada-002) → Unlikely to hit

### Production Considerations
- **Single-threaded:** SQLite doesn't support high concurrency → Fine for single-founder use
- **No authentication:** MCP server runs locally → Secure environment variables
- **Manual deployments:** No CI/CD yet → Git commits are deployment record
- **Founder-in-the-loop:** Many agents require approval → Check Notion daily

---

## Development Workflow

### Status vs Context Files

**WOS_Status.md (Project Management):**
- "Where are we in the build?"
- Current sprint progress
- Agent completion status
- Next session tasks
- Blockers and decisions needed
- Updated **every session**

**WOS_Context.md (This File - System Knowledge):**
- "How does the system work and why?"
- Architecture patterns
- Tech stack details
- Design decisions
- Integration guides
- Common commands
- Updated **when architecture/patterns change**

### Automated Documentation Updates

**IMPORTANT: Claude handles documentation updates automatically.**

**During working sessions:**
- Claude tracks what's built/changed
- At natural break points or end of session, Claude asks: "Update docs?"
- User can also prompt: "update status", "update context", or "update docs"

**When user says "update status":**
1. Claude reads current WOS_Status.md
2. Updates with session changes (completed agents, sprint progress, blockers, next steps)
3. Commits with message: "Update WOS_Status.md - [brief summary] ([date])"

**When user says "update context":**
1. Claude reads current WOS_Context.md
2. Updates architecture/patterns/integrations based on changes made
3. Commits with descriptive message

**When user says "update docs":**
1. Claude updates BOTH files
2. Commits both

**Pre-commit hook = safety net:**
- If user manually commits code without updating docs, hook warns them
- Hook doesn't auto-update, just reminds

**What triggers updates:**

WOS_Status.md:
- Completing an agent
- Sprint progress changes
- New blockers or decisions
- End of working session

WOS_Context.md:
- New execution modes
- Changed agent patterns
- New integrations
- Architectural decisions
- New commands/workflows
- Constraint changes

---

## Getting Started (New Claude Instance Onboarding)

**1. Read this file first** to understand architecture
**2. Read WOS_Status.md** to see current progress
**3. Check environment setup:**
   - `.env` file exists with all keys
   - `requirements.txt` dependencies installed
   - MCP server configured in `.mcp.json`
**4. Test MCP connection:**
   - `~/.local/bin/claude` → Should connect to WOS MCP server
   - Try: `execute the wos_status tool`
**5. Explore codebase:**
   - `src/wos/brain.py` - Brain control plane
   - `src/wos/intent_handlers/` - Existing agents
   - `packs/P3.2/WORKFLOWS/` - n8n workflows
**6. Follow agent patterns** when building new agents

---

## Support & Debugging

### Common Issues

**MCP Server not connecting:**
- Check `.mcp.json` path is absolute
- Verify Python 3 installed: `python3 --version`
- Check MCP logs in Claude Code

**Intent execution fails:**
- Check `.env` variables set (N8N_API_KEY, NOTION_API_KEY, etc.)
- Verify n8n workflow exists and is active
- Check intent registered: `sqlite3 intent_registry.db "SELECT * FROM intents WHERE intent_id='...'"`

**Approval gate timeout:**
- Check Notion API key valid
- Verify approval database ID correct
- Check Notion page created (check Notion workspace)

**Canon search returns no results:**
- Check OpenAI API key set
- Verify embeddings generated: `sqlite3 canon.db "SELECT COUNT(*) FROM artifact_embeddings"`
- Try text search instead of semantic: `use_semantic_search=False`

### Logs

**MCP Server logs:**
- Stderr output from `python3 src/wos/server.py`
- Shows Brain execution, handler errors, n8n calls

**n8n Execution logs:**
- Web UI: `https://n8n.whyhi.app` → Executions tab
- Shows workflow steps, errors, response payloads

**Intent Execution logs:**
- Database: `intent_registry.db` → `intent_executions` table
- Includes status, error messages, execution time

---

**End of WOS_Context.md**

For current sprint progress and what's next, see `WOS_Status.md`.
