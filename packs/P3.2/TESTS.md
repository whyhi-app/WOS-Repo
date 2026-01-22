artifact_id: WOS-P3.2-TESTS-v1.0
title: Brain Control Plane v0 — Smoke Tests
phase: 3.2
type: tests
status: Locked
version: 1.0
date_locked: 2026-01-11T22:15:00Z
owner: WhyHi Ops Stack (WOS)

depends_on: WOS-P3.2-SPEC-v1.0
supersedes: N/A
implemented_in: curl + n8n execution viewer
interfaces: POST Brain endpoint; validate normalized envelope

security_class: internal
approval_required: HITL pause expected on WB deploy
timeout_s: 15

how_used: Copy/paste curl payloads to validate Brain behavior.
rollback: Deactivate workflows; re-import prior exports.

## Smoke test payloads

### Test A — Known intent routes + responds
```bash
curl -sS -X POST "https://n8n.whyhi.app/webhook/wos/brain/v0"   -H "Content-Type: application/json"   -d '{"request_id":"brain-known-final-1","intent":"daily_newsletter_digest_v0","input":{}}'
```
Expected keys:
- `ok: true`
- `status: "Completed"`
- `request_id` equals input
- `resolved_intent: "daily_newsletter_digest_v0"`
- `result.statusCode: 200`
- `result.body.message: "Workflow was started"`

### Test B — Unknown intent fails deterministically
```bash
curl -sS -X POST "https://n8n.whyhi.app/webhook/wos/brain/v0"   -H "Content-Type: application/json"   -d '{"request_id":"brain-unknown-final-1","intent":"does_not_exist","input":{}}'
```
Expected keys:
- `ok: false`
- `status: "Failed"`
- `errors[0].code: "INTENT_NOT_FOUND"`
- `errors[0].stage: "routing"`

### Test C — REQ-WB-001 guard pauses deploy
```bash
curl -sS -X POST "https://n8n.whyhi.app/webhook/wos/brain/v0"   -H "Content-Type: application/json"   -d '{"request_id":"brain-wb-proof-guard-1","intent":"daily_newsletter_digest_v0","mode":"workflow_builder","wb_stage":"deploy","input":{}}'
```
Expected keys:
- `ok: false`
- `status: "Paused"`
- `approval.approval_required: true`
- `errors[0].code: "HITL_REQUIRED"`
- No downstream intent HTTP request executes (check n8n execution graph)

## Minimal triage checklist (if a test fails)
- Is the workflow **Active** (production), not test-only?
- Is `WEBHOOK_URL` correct (https://n8n.whyhi.app/)?
- Are you calling `/webhook/` not `/webhook-test/`?
- Do the intent workflow webhook nodes include a **Respond to Webhook** node?
- Confirm the Brain Switch routing uses `resolved_intent` and `.trim()` is applied.
