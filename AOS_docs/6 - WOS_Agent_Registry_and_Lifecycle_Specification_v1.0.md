# 6. WOS Agent Registry & Lifecycle Specification (v1.0)

AOS Document 6 of 6

1\. Purpose

This document defines how Agents are registered, identified, governed,
executed, paused, retired, and audited within the WhyHi Operating System
(WOS).

Its purpose is to ensure that:\
- All Agents operating within WOS are explicitly declared\
- Agent capabilities and authority are known, bounded, and auditable\
- Agent execution is predictable, controllable, and observable\
- Agents may evolve safely over time without destabilizing the system

This specification prioritizes clarity, founder control, and safety over
scale or autonomy.

2\. Scope

This document applies to all automated, semi-automated, and assistive
Agents operating under WOS, including system-level and task-level
Agents, regardless of implementation layer.

3\. Definitions (Normative)

All terms used in this document are defined in Appendix A --- Canonical
Definitions. Appendix A is authoritative.

4\. Agent Conceptual Model

An Agent is a named, registered execution entity that performs work
within declared capabilities, executes Tasks within Runs, and produces
observable outcomes.

Agents are not autonomous, self-authorizing, or implicitly persistent.

5\. Agent Identity

Each Agent MUST have:\
- A unique Agent ID\
- A human-readable name\
- A version identifier\
- A declared Agent Type

6\. Agent Registry

The Agent Registry is the authoritative source of truth for all Agents.
No Agent may execute unless registered and Active.

Required registry fields include:\
agent_id, name, version, description, agent_type, owner, status,
allowed_capabilities, allowed_tools, execution_scope,
observability_level, override_policy, created_at, last_modified.

Only the Founder may create, modify, enable, or retire Agents.

7\. Agent Types

Supported Agent types:\
- Task-scoped Agents\
- Run-scoped Agents\
- Persistent Agents

8\. Agent Lifecycle States

Lifecycle states:\
Draft → Registered → Active → Paused → Deprecated → Retired

9\. Execution Rules

Agents may execute only when Active, authorized by the Run, and within
declared capabilities.

All violations MUST be logged.

10\. Versioning & Evolution

Agent versions are immutable. Changes require a new version and registry
update.

11\. Observability & Audit

Each Agent execution MUST emit Agent ID, version, Run ID, Task ID, tool
calls, artifacts, violations, and termination reason.

12\. Failure & Recovery

Agent failures MUST be recorded. Recovery behavior is governed by the
invoking Run.

13\. Security Alignment

This document aligns with the WOS Constitution, Governance Model, Task
Execution Model, and Security Model.

Founder authority prevails, with violations recorded.

14\. Status

This document is normative for WOS AOS v1.0.
