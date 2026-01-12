artifact_id: `P3.1-SPEC-001`
title: `Acceptance Demo Spec — Prospect/Investor Brief Generator v0 (Client-Agnostic)`
phase: `3.1`
type: `SPEC`
status: `LOCKED`
version: `v1.1`
date_locked: `2026-01-08`
owner: `Tom`
depends_on: `Canon_Search_v0 (planned), Canon_Get_v0 (planned), Approval_Gate_v0 (planned), Notion_Publish_Brief_v0 (planned)`
supersedes: `P3.1_ExportPack_v1.0`
implemented_in: `n8n (planned)`
interfaces: `Brain_Run_Request_v0, Brain_Run_Response_v0, Approval_Payload_v0, Gate_Response_v0`
security_class: `Internal`
approval_required: `Yes (any write/publish/outbound)`
timeout_s: `Tool-specific; defaults below`
how_used: `Defines the Phase 3 acceptance demo behavior and constraints`
rollback: `Disable Brain trigger; disable publish tool; revert workflow imports`

## 0) Boundary rule (non-negotiable)
The WOS client is swappable. The client (ChatGPT, Gemini, etc.) is only a UI/invoker that sends and receives JSON.
- Do not rely on client-specific “memory” for durable behavior.
- Canon (index + artifacts) is the durable knowledge base and is client-agnostic.
- All orchestration, policy, HITL, and publishing live in n8n + tools.

## 1) Goal
Run an end-to-end autonomous flow in n8n that:
1) generates a structured brief,
2) proves retrieval-first via Canon tools,
3) enforces HITL before any write,
4) publishes to Notion upon approval,
5) returns final status + Notion URL to the client.

## 2) Inputs (minimal)
- `brief_type`: `"prospect"` | `"investor"` (default: `"investor"`)
- `target_name`: string (required)
- `target_org`: string (optional)
- `target_url`: string (optional but strongly recommended)
- `your_goal`: string (required)
- `context`: string (optional)
- `destination`: string (required; Notion destination key)
- `web_research_enabled`: boolean (default: `false`)
- `client_request_id`: string (optional but recommended; enables cross-client dedupe later)
- `client`: object (optional; for logging only)

## 3) Required behavior (hard requirements)
- Must call `Canon_Search_v0` at least once per run.
- May call `Canon_Get_v0` if selecting a result for deeper context.
- Must produce a draft brief in the standard format (see §4).
- Must generate an `approval_payload` and route to `Approval_Gate_v0` before any Notion write.
- Must only call `Notion_Publish_Brief_v0` if gate outcome is `approve` or `edit`.
- Must return a `Brain_Run_Response_v0` object to the client.

## 4) Brief output format (markdown)
1. One-liner (who they are + why they matter)
2. What we know (Canon)
3. Hypotheses / angles
4. Risks / watchouts
5. Questions to ask (2–5)
6. Suggested next step (single)
7. Sources
   - Canon refs (artifact_id + title)
   - Web refs (only if research enabled)

## 5) Approval policy (hard rules)
Approval required for:
- Any Notion write/publish/update
- Any task creation
- Any outbound messaging

Unattended allowed:
- Canon retrieval + drafting + formatting
- Web research only if explicitly enabled per run (default OFF)

## 6) Safety caps (v0 defaults)
- `max_tool_calls_per_run`: `6`
- `max_agent_steps`: `10`
- `max_loops_per_step_type`: `2`
- `per_tool_timeout_sec`: `20` (fast tools), `60` (web research if enabled)
- `max_draft_length_chars`: `6000`

Fail-closed:
- If a tool fails twice or loop cap is hit: stop without publishing and return `Failed` or `NeedsApproval` with reason.
