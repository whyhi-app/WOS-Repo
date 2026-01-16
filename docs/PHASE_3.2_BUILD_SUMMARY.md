# Phase 3.2 Brain Control Plane — Build Summary

**Status:** ✅ Phase 3.2 v0 Core Implementation Complete

**Date:** 2026-01-15
**Phase:** 3.2 (WOS Runtime v0)
**Type:** Brain Control Plane (Intent Router)

---

## What Was Built

**5 Core Modules** implementing Phase 3.2 Brain Control Plane for WOS MCP:

### 1. **intent_registry.py** — Intent Registry & SQLite Schema
- SQLite database schema for intent definitions
- Intent registration, lookup, versioning
- n8n workflow mappings (for wiring up later)
- Execution audit logging (AOS compliance)
- Policy rules storage

**Key Classes:**
- `IntentRegistry` — Main registry interface
- `INITIAL_INTENTS` — V0 intent definitions (brief_generator, daily_email_digest)

**Usage:**
```python
registry = IntentRegistry(db_path="wos.db")
registry.register_intent(
    intent_id="brief_gen_v0",
    name="brief_generator",
    version="0.1",
    handler_module="wos.intent_handlers.brief_generator",
    approval_required=True
)
```

### 2. **brain.py** — Brain Control Plane (Intent Router)
- Receives normalized Brain_Run_Request_v0
- Validates request, resolves intent name
- Enforces policy gates (workflow_builder deploy)
- Routes to appropriate handler
- Returns Brain_Run_Response_v0 envelope

**Key Classes:**
- `Brain` — Main router
- `RequestStatus` — Enum for response statuses

**Request Flow:**
1. Normalize request (trim intent, apply defaults)
2. Validate required fields
3. Look up intent in registry
4. Check policy gates (HITL deploy guard)
5. Check approval requirements
6. Execute handler
7. Log execution (audit trail)
8. Return response envelope

**Response Envelope** (Brain_Run_Response_v0):
```json
{
  "ok": boolean,
  "status": "Completed|Failed|Paused|PendingApproval",
  "request_id": string,
  "execution_id": string,
  "resolved_intent": string,
  "result": object,
  "timestamp": ISO8601,
  "errors": [{code, message, stage}],
  "approval": {approval_required, reason} (if pending)
}
```

### 3. **approval_gate.py** — HITL Approval Gate
- Checks if request needs approval
- Stores approval requests
- Provides approval/rejection interface
- V0: Stub (ready for Notion integration)

**Key Classes:**
- `ApprovalGate` — Main approval logic

### 4. **canon_tools.py** — Canon Retrieval Interface
- Search Canon Index for artifacts
- Retrieve full artifacts by ID
- Store new artifacts
- List artifacts by type
- V0: Stub (ready for SQLite implementation)

**Key Classes:**
- `CanonTools` — Canon interface

### 5. **n8n_executor.py** — n8n Workflow Executor
- Calls n8n workflows via REST API
- Handles request/response transformation
- Error handling, timeouts, retries
- Execution timing and logging

**Key Classes:**
- `N8nExecutor` — n8n workflow caller

**Usage:**
```python
executor = N8nExecutor(
    n8n_base_url="https://n8n.whyhi.app",
    api_key=os.getenv("N8N_API_KEY")
)

result = executor.execute_workflow(
    workflow_name="daily_email_digest",
    payload={"user_id": 123},
    timeout_seconds=30
)
```

---

## Architecture

```
Claude Code (you) 
  ↓ (MCP call)
WOS MCP Server
  ↓ (process_request)
Brain.py (Intent Router)
  ├→ IntentRegistry (lookup intent definition)
  ├→ ApprovalGate (check HITL requirements)
  ├→ Intent Handler (execute logic)
  │   ├→ CanonTools (retrieve artifacts)
  │   ├→ N8nExecutor (call workflows)
  │   └→ Format response
  └→ Return Brain_Run_Response_v0
  ↑ (MCP response)
Claude Code receives result
```

---

## What's Complete ✅

- [x] Intent Registry (SQLite schema + management)
- [x] Brain Control Plane (full router logic)
- [x] Request normalization + validation
- [x] Policy gates (workflow_builder deploy guard)
- [x] Approval gate interface (stub)
- [x] Canon retrieval interface (stub)
- [x] n8n executor (complete)
- [x] Response envelope generation
- [x] Audit logging (AOS compliance)
- [x] Error handling throughout

---

## What's NOT Complete (Next Steps)

- [ ] Wire up existing n8n workflows to intent registry
- [ ] Implement intent handlers (brief_generator, daily_digest)
- [ ] Implement Canon Index SQLite schema
- [ ] Integrate approval gate with Notion HITL
- [ ] Dynamic handler module loading
- [ ] Phase 3.3 (Toolbox v0 implementation)

---

## How to Deploy

1. **Copy files to your WOS repo:**
   ```bash
   cp intent_registry.py /Users/tomwynn/Documents/WhyHi_Server/WOS-Repo/src/wos/
   cp brain.py /Users/tomwynn/Documents/WhyHi_Server/WOS-Repo/src/wos/
   cp approval_gate.py /Users/tomwynn/Documents/WhyHi_Server/WOS-Repo/src/wos/
   cp canon_tools.py /Users/tomwynn/Documents/WhyHi_Server/WOS-Repo/src/wos/
   cp n8n_executor.py /Users/tomwynn/Documents/WhyHi_Server/WOS-Repo/src/wos/
   ```

2. **Integrate into src/wos/server.py:**
   - Import Brain, IntentRegistry, etc.
   - Initialize in MCP server setup
   - Add Brain processing to existing tools

3. **Test:**
   - Create intent registry
   - Register test intents
   - Call Brain via Claude Code MCP

---

## AOS Alignment

✅ **Constitution:** Reliability first (deterministic routing, no silent failures)
✅ **Governance:** Founder authority (HITL gates, policy guards)
✅ **Security:** Explicit trust (validated requests, logged operations)
✅ **Memory:** Audit trail (all executions logged to SQLite)
✅ **Task Execution:** Deterministic boundaries (single intent per request)
✅ **Agent Registry:** Foundational structure for agent lifecycle

---

## Next Checkpoint Actions

1. **Wire up n8n workflows** → Map Gmail_to_Notion, Apple_Reminders, etc. to intents
2. **Build intent handlers** → brief_generator, daily_digest execution logic
3. **Implement Canon Index** → SQLite schema + search/retrieval
4. **Test end-to-end flow** → Request → Brain → n8n workflow → Response

---

## Files Summary

| File | Lines | Purpose |
|------|-------|---------|
| intent_registry.py | 250+ | Intent definitions, SQLite schema, registration |
| brain.py | 300+ | Request routing, policy gates, response envelopes |
| approval_gate.py | 70 | HITL approval logic (stub) |
| canon_tools.py | 60 | Canon retrieval interface (stub) |
| n8n_executor.py | 120 | n8n REST API caller |

**Total:** ~800 lines of production Python code
