# Operational Lens

## Lens Name
Operational Lens

## Purpose
Evaluate ownership, support burden, operational readiness, reliability, day-two consequences, resiliency, incident risk, and sustainment. This lens is designed to test whether the proposal can survive real production life after launch.

## When to Use
- When the change affects reliability, support, on-call, platform ownership, or service boundaries.
- When a new shared capability, migration path, or team responsibility is introduced.
- When the proposal looks good at delivery time but the long-term support model is still fuzzy.

## Key Questions
- Who owns this after delivery, and do they have the mandate and capacity to run it well?
- What new failure modes, support paths, or escalation patterns does this introduce?
- What happens during incidents, turnover, or degraded states?
- Does this reduce or increase long-term toil?
- Are observability, readiness, and rollback expectations being treated as first-class concerns?

## What This Lens Looks For
- Unclear day-two ownership and sustainment gaps.
- Hidden toil and support complexity created by shared systems.
- Reliability and resiliency risks that appear only once scale and incidents enter the picture.
- Operational dependencies that make the idea harder to run than to build.
- Places where the operating model depends on heroics or institutional memory.

## Common Risks / Failure Modes
- Shipping a technically valid solution with no durable support model.
- Concentrating failure into a shared path without improving readiness or recovery.
- Creating a support burden that silently lands on the wrong team.
- Underinvesting in observability, runbooks, and incident handling because they are not part of the "core" proposal.
- Allowing ownership ambiguity to surface only during incidents.

## Signals or Evidence to Consider
- On-call load, incident history, and support queue patterns.
- Current operational hotspots, brittle dependencies, and toil-heavy workflows.
- Ownership maps and escalation paths across related systems.
- Monitoring, alerting, logging, and rollback maturity.
- What happened operationally in previous efforts with similar shape.

## Output Expectations
- Clarify the operating model required for the decision to work.
- Highlight hidden support cost, toil, and readiness gaps.
- Describe the operational risks that could turn a good idea into a long-term drag.
- Recommend how to make the decision survivable in day-two reality.

## Recommendation Style
Be concrete and operationally literate. Recommendations should emphasize ownership clarity, readiness, and failure handling rather than abstract reliability ideals.
