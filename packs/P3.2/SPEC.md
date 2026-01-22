artifact_id: WOS-P3.2-SPEC-v1.0
title: Brain Control Plane v0 — Spec
phase: 3.2
type: spec
status: Locked
version: 1.0
date_locked: 2026-01-11T22:15:00Z
owner: WhyHi Ops Stack (WOS)

depends_on: WOS-P3.2-README-v1.0
supersedes: N/A
implemented_in: n8n workflow: wos_brain_controlplane_v0.json
interfaces: Brain webhook + internal routing to intent webhooks

security_class: internal
approval_required: HITL for WB deploy (policy pause)
timeout_s: 15

how_used: Defines runtime request routing/normalization for WOS Brain v0.
rollback: Re-import prior spec + workflow version; deactivate current workflow.

## 1. Purpose
Brain v0 is the WOS **control plane**: it accepts a normalized request, resolves an intent, enforces minimal policies, routes to the correct intent workflow, and returns a standardized run envelope.

## 2. Inputs
### 2.1 Brain request (POST /webhook/wos/brain/v0)
Required:
- `request_id` (string)
- `intent` (string)

Optional:
- `input` (object; default `{}`)
- `mode` (string; e.g., `workflow_builder`)
- `wb_stage` (string; `propose|test|approve|deploy`)

Normalization rules:
- `resolved_intent = intent.trim()` (prevents trailing-space bugs)
- If fields are missing/empty, defaults are applied.

## 3. Routing
Routing is implemented as an n8n Switch over `resolved_intent`.

v0 routes:
- `daily_newsletter_digest_v0` → HTTP Request to `/webhook/wos/intent/daily_newsletter_digest_v0`
- Fallback → Normalize Unknown Intent (INTENT_NOT_FOUND)

## 4. Policy guard (REQ-WB-001)
If:
- `mode == "workflow_builder"` AND
- `wb_stage == "deploy"`

Then:
- Brain MUST return `status="Paused"`, `ok=false`, and `approval.approval_required=true`
- No downstream HTTP intent call should run.

Implementation:
- Guard is implemented as an IF gate before routing, leading to Normalize Paused.

## 5. Execution + response normalization
### 5.1 Success
If an intent HTTP call returns a successful response (2xx / < 400), Brain returns:
- `ok=true`, `status="Completed"`
- `request_id`, `run_id`, `resolved_intent`
- `result` includes statusCode/body/headers from the intent call (as available)

### 5.2 Error
If the intent HTTP call returns >= 400 or throws:
- `ok=false`, `status="Failed"`
- `errors[0].code="BRAIN_ERROR"` or an intent-specific code in future versions
- `result` may include captured error details for debugging

### 5.3 Unknown intent
If routing has no match:
- `ok=false`, `status="Failed"`
- `errors[0].code="INTENT_NOT_FOUND"`, `stage="routing"`

## 6. Caps (v0)
v0 stubs telemetry fields; caps enforcement is deferred to v1 (Phase 3.3+), but the request schema includes a `caps` object for forward compatibility.

## 7. Non-goals (v0)
- No intent registry DB (manual Switch rules only)
- No fuzzy intent matching (exact match + trim)
- No web research (default OFF; not wired)
- No idempotency/dedupe (caller must avoid replaying side-effect requests)
