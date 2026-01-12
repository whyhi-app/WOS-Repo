artifact_id: WOS-P3.2-DECISIONS-v1.0
title: Brain Control Plane v0 — Decisions
phase: 3.2
type: decisions
status: Locked
version: 1.0
date_locked: 2026-01-11T22:15:00Z
owner: WhyHi Ops Stack (WOS)

depends_on: WOS-P3.2-SPEC-v1.0
supersedes: N/A
implemented_in: n8n workflows + Docker Compose env vars
interfaces: Routing via HTTP Request nodes to intent webhooks

security_class: internal
approval_required: HITL required for WB deploy
timeout_s: 15

how_used: Rationale and deferred scope for Brain v0 implementation.
rollback: Revert to prior workflow exports; revert docker-compose env vars.

## Decisions
1) **Use HTTP Request → webhook endpoints** for routing intents (vs. internal sub-workflow execution).
- Reason: reliable, explicit interface boundary; works well with future MCP allowlists and client-swappability.

2) **Exact-match intents + `.trim()` only** (no fuzzy matching).
- Reason: keep v0 deterministic and debuggable; fuzzy intent resolution is a later layer.

3) **REQ-WB-001 guard enforced in Brain** by pausing deploy-stage WB requests (HITL required).
- Reason: “deploy” is inherently risky; enforce at control plane so no intent can bypass it.

4) **Execution history pruning configured at host level** (7-day retention).
- Reason: keep Postgres lean; do not treat executions as the durable memory layer.

## Deferred (explicit)
- Intent Registry / dynamic routing table (manual Switch for v0)
- Dedupe/idempotency for side-effect intents
- Budget/caps enforcement beyond simple scaffolding
- Auth between Brain and intent endpoints (kept minimal to avoid breaking the flow; revisit in Phase 3.5)
