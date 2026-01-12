artifact_id: `P3.1-DECISIONS-001`
title: `Decisions — 3.1 Acceptance Demo Lock + Guardrails (Client-Agnostic)`
phase: `3.1`
type: `DECISIONS`
status: `LOCKED`
version: `v1.1`
date_locked: `2026-01-08`
owner: `Tom`
depends_on: `P3.1-SPEC-001`
supersedes: `P3.1_ExportPack_v1.0`
implemented_in: `n8n (planned)`
interfaces: `Brain_Run_Request_v0, Brain_Run_Response_v0`
security_class: `Internal`
approval_required: `Yes`
timeout_s: `N/A`
how_used: `Traceability for non-obvious choices`
rollback: `N/A`

1) Demo is locked to `Prospect/Investor Brief Generator v0` (Brief → Approve → Publish).
2) Client is swappable (ChatGPT/Gemini/etc.). We will not rely on client-specific memory or wrappers.
3) Canon is the durable, client-agnostic knowledge base; retrieval is via `Canon_Search_v0` and `Canon_Get_v0`.
4) Implement `Canon_Search_v0` and `Canon_Get_v0` first; Brain depends on them and they are MCP-safe candidates later.
5) Writes require approval always (Notion publish, tasks, outbound).
6) Web research default OFF unless explicitly enabled per run.
7) Caps chosen (6 tool calls, 10 steps, loop cap 2) to prevent runaway behavior; fail-closed on repeated failures.
