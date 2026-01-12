artifact_id: `P3.1-README-001`
title: `Export Pack README — Phase 3.1 Acceptance Demo Lock (Client-Agnostic)`
phase: `3.1`
type: `README`
status: `LOCKED`
version: `v1.1`
date_locked: `2026-01-08`
owner: `Tom`
depends_on: `Canon_Search_v0 (planned), Canon_Get_v0 (planned), Approval_Gate_v0 (planned), Notion_Publish_Brief_v0 (planned)`
supersedes: `P3.1_ExportPack_v1.0`
implemented_in: `n8n (planned)`
interfaces: `Brain_Run_Request_v0, Brain_Run_Response_v0, Approval_Payload_v0, Gate_Response_v0, Canon_Search_v0, Canon_Get_v0`
security_class: `Internal`
approval_required: `Yes (any write/publish/outbound)`
timeout_s: `Tool-specific; defaults defined in SPEC`
how_used: `Use this pack as the authoritative contract for building Brain + tools in 3.2/3.3 with clean client/runtime boundaries`
rollback: `Disable Brain trigger; disable publish tool; revert workflow imports to prior exports`

## Drive folder path (intended)
`/WhyHi/WOS/WOS MCP Development/Phase 3 — WOS Runtime v0 (Brief → Approve → Publish)/P3.1/`

## What’s in this pack
- Locked acceptance demo definition for Phase 3.1 (Prospect/Investor Brief Generator v0)
- Success criteria + approval policy + safety caps (fail-closed)
- Client-agnostic boundary rules (client can be ChatGPT, Gemini, etc.)
- JSON interface contracts for Brain + Gate + Canon tools (search/get)
- Smoke test payloads (copy/paste) + expected keys
- Canon Index entries for these artifacts

## How to use
- Treat `P3.1-SPEC-001` as the source-of-truth for behavior/rules in 3.2–3.4.
- Implement schemas exactly in n8n: Brain webhook input validation + deterministic tool I/O.
- Enforce “no writes before approval” at the router level (policy block if violated).
- Implement `Canon_Search_v0` and `Canon_Get_v0` first; Brain depends on them and they are client-agnostic.
- Keep the client/runtime boundary clean: the client only sends/receives JSON; all state, routing, HITL, and publishing live in n8n + Canon.

## Security/Hygiene
- No secrets in docs/files.
- Credentials referenced by name only.
- Writes require approval where applicable.

## Lifecycle
- Locked means authoritative until superseded.
- Updates create new version + supersedes prior artifact_id.
- Deprecated artifacts remain for traceability.

## Environment / Compatibility (assumptions)
- Runtime: n8n (self-hosted) is the execution substrate; n8n execution history is the trace.
- Client: any LLM UI/integration (ChatGPT, Gemini, etc.) that can send/receive JSON over HTTP/webhook.
- Nodes assumed: Webhook, IF/Switch, Set, Code, HTTP (optional), Notion, Wait (for HITL gate), Merge.
- External deps: Notion workspace + Canon store in Notion (Canon Index DB + artifact pages/bodies).

## Deployment state
- Planned (specs/contracts locked; workflows not yet exported in this pack).

## Rollback (concrete)
- Disable Brain workflow trigger (Webhook/Chat trigger off).
- Disable/rename Notion publish workflow to prevent accidental writes.
- Re-import prior workflow exports if later phases deploy changes.
