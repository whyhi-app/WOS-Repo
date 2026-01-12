# CANON INDEX ENTRIES (Notion-ready)

artifact_id: WOS-P3.2-README-v1.0
title: Phase 3.2 Brain Workflow (Control Plane) — Export Pack
domain: WOS/Core Runtime
type: Reference
status: Approved
version: 1.0
updated_at: 2026-01-11
source: ChatGPT project thread “Phase 3.2 Brain Workflow (Control Plane)”
tags: brain, control-plane, routing, n8n, webhook
summary: Packaged artifacts for Brain v0 routing and normalization with REQ-WB-001 guard.

artifact_id: WOS-P3.2-SPEC-v1.0
title: Brain Control Plane v0 — Spec
domain: WOS/Core Runtime
type: Spec
status: Approved
version: 1.0
updated_at: 2026-01-11
source: Same as above
tags: spec, routing, intents, hitl
summary: Defines Brain v0 request schema, routing rules, normalization, and workflow-builder deploy guard.

artifact_id: WOS-P3.2-DECISIONS-v1.0
title: Brain Control Plane v0 — Decisions
domain: WOS/Core Runtime
type: Decision
status: Approved
version: 1.0
updated_at: 2026-01-11
source: Same as above
tags: decisions, http-request, pruning
summary: Records key choices (HTTP routing, exact-match intents, HITL deploy guard, 7-day pruning) and deferred scope.

artifact_id: WOS-P3.2-SCHEMAS-v1.0
title: Brain Control Plane v0 — Schemas
domain: WOS/Core Runtime
type: Reference
status: Approved
version: 1.0
updated_at: 2026-01-11
source: Same as above
tags: schemas, json, contract
summary: JSON contracts for Brain v0 and daily email digest intent endpoint.

artifact_id: WOS-P3.2-WF-BRAIN-v0
title: n8n Workflow Export — WOS Brain Control Plane v0
domain: WOS/Core Runtime
type: Artifact
status: Approved
version: 0
updated_at: 2026-01-11
source: n8n workflow export
tags: workflow, n8n, brain
summary: Exported Brain v0 workflow implementing request normalization, routing, and REQ-WB-001 guard.

artifact_id: WOS-P3.2-WF-INTENT-DAILYEMAILDIGEST-v0
title: n8n Workflow Export — Intent daily_email_digest_v0
domain: WOS/Core Runtime
type: Artifact
status: Approved
version: 0
updated_at: 2026-01-11
source: n8n workflow export
tags: workflow, n8n, intent
summary: Exported intent workflow that triggers the Daily Newsletter Digest automation via webhook.

artifact_id: WOS-P3.2-TESTS-v1.0
title: Brain Control Plane v0 — Smoke Tests
domain: WOS/Core Runtime
type: Checklist
status: Approved
version: 1.0
updated_at: 2026-01-11
source: Same as above
tags: tests, smoke, curl
summary: Copy/paste curl payloads + expected keys to validate Brain v0 behavior.
