artifact_id: WOS-P3.2-README-v1.0
title: Phase 3.2 Brain Workflow (Control Plane) — Export Pack
phase: 3.2
type: readme
status: Locked
version: 1.0
date_locked: 2026-01-11T22:15:00Z
owner: WhyHi Ops Stack (WOS)

depends_on: WOS-P3.1 Runtime v0 (Brief → Approve → Publish)
supersedes: N/A
implemented_in: n8n (self-hosted) workflows + curl client
interfaces: POST /webhook/wos/brain/v0 ; POST /webhook/wos/intent/daily_email_digest_v0

security_class: internal
approval_required: HITL for WB deploy (policy pause)
timeout_s: 15

how_used: Import workflows into n8n; call Brain endpoint with JSON body containing request_id + intent.
rollback: Disable workflows in n8n OR re-import prior workflow exports; revert docker-compose env vars if needed.

## What’s in this pack
- `WORKFLOWS/wos_brain_controlplane_v0.json` — Brain control plane workflow (router + normalization + WB guard).
- `WORKFLOWS/wos_intent_daily_email_digest_v0.json` — Intent workflow for `daily_email_digest_v0`.
- `SCHEMAS.json` — Request/response contracts (Brain + intent).
- `SPEC.md` — Behavioral spec for Brain v0.
- `DECISIONS.md` — Key decisions + deferred scope.
- `TESTS.md` — Smoke tests + hardening checks.
- `CANON_INDEX_ENTRIES.md` — Notion-ready Canon Index entries.

## How to use
- In n8n: import both workflow JSON files.
- Activate both workflows (Production).
- Call Brain:
  - `POST https://n8n.whyhi.app/webhook/wos/brain/v0`
  - JSON body must include: `request_id`, `intent`, optional `input`, optional WB fields.
- For direct intent testing (optional):
  - `POST https://n8n.whyhi.app/webhook/wos/intent/daily_email_digest_v0`

## Environment / compatibility
- n8n: 2.1.3 self-hosted (Docker)
- DB: DigitalOcean managed Postgres (postgresdb driver)
- Reverse proxy: nginx (as shown in responses)
- Assumptions:
  - `WEBHOOK_URL=https://n8n.whyhi.app/`
  - Workflows are imported with the same webhook paths (avoid duplicates).

## Deployment state + rollback
- State: **Built + Deployed** (validated via production `/webhook` curl calls).
- Rollback:
  - In n8n, deactivate the Brain workflow first (stops routing).
  - Deactivate the intent workflow(s).
  - Re-import prior workflow JSON exports (or restore from backup).
  - If execution pruning causes issues, revert `EXECUTIONS_DATA_*` env vars and restart container.

## Security / hygiene
- No secrets in docs/files.
- Credentials referenced by name only.
- Writes / deploy actions require approval when applicable (REQ-WB-001 guard).

## Lifecycle
- “Locked” means authoritative until superseded.
- Updates create a new version and supersede the prior artifact_id.
- Deprecated artifacts remain for traceability.
