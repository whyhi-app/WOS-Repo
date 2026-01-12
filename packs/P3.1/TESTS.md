artifact_id: `P3.1-TESTS-001`
title: `Tests — 3.1 Acceptance Demo Smoke Payloads (Client-Agnostic)`
phase: `3.1`
type: `TESTS`
status: `LOCKED`
version: `v1.1`
date_locked: `2026-01-08`
owner: `Tom`
depends_on: `P3.1-SPEC-001`
supersedes: `P3.1_ExportPack_v1.0`
implemented_in: `n8n (planned)`
interfaces: `Brain_Run_Request_v0 / Brain_Run_Response_v0`
security_class: `Internal`
approval_required: `Yes (publish path)`
timeout_s: `N/A`
how_used: `Copy/paste payloads into Brain webhook test (any client)`
rollback: `Disable Brain trigger`

## Test 1 — Minimal investor brief (no URL), client-agnostic
### Payload
```json
{
  "brief_type": "investor",
  "target_name": "Jane Doe",
  "target_org": "Example Ventures",
  "your_goal": "Warm intro → 20-min call about WhyHi + pre-seed fit",
  "context": "Met at FoundersBoost LA",
  "destination": "NOTION_DB:BRIEFS_V0",
  "web_research_enabled": false,
  "client_request_id": "demo-001",
  "client": { "name": "any-client" }
}
```

### Expected response keys
- `status`
- `requires_approval`
- `result.draft_brief_markdown`
- `tools_called` includes `Canon_Search_v0`
- `approval_payload.proposed_action`
- `approval_payload.canon_refs` length >= 1

## Test 2 — Policy enforcement (attempted publish without approval)
**Setup:** Force a router branch that attempts `Notion_Publish_Brief_v0` without gate success.
**Expected:**
- Response `status="Failed"`
- `error.code="POLICY_BLOCKED"`
- No Notion page created (`result.notion_url` remains null)

## Test 3 — Canon tools schema compliance
**Setup:** Call `Canon_Search_v0` with invalid input (missing query).
**Expected:** `ok=false` and `error.code="INVALID_INPUT"`.

## Minimal triage checklist
- Response validates against `Brain_Run_Response_v0`
- `Canon_Search_v0` called at least once
- `requires_approval=true` before any publish
- If failed: `error.code` is in the enum list
