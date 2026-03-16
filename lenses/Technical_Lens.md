# Technical Lens

## Lens Name
Technical Lens

## Purpose
Evaluate feasibility, complexity, scalability, maintainability, architecture impact, technical debt implications, dependencies, and long-term engineering consequences. This lens is meant to test whether the idea is genuinely reducing complexity or simply relocating it into a different part of the system.

## When to Use
- When the idea changes architecture, ownership boundaries, platform direction, or system interfaces.
- When a migration, consolidation, platform investment, or foundational capability is being considered.
- When the proposal feels technically right but implementation complexity or long-term maintainability is still unclear.

## Key Questions
- What problem is the technical change actually solving, and is that problem real enough to justify the complexity?
- Does this reduce long-term complexity, or does it mostly move complexity into a shared or hidden layer?
- What dependencies, coupling, or sequencing constraints could change the implementation story?
- What does rollback, coexistence, or partial adoption look like if reality does not match the plan?
- Which assumptions are driving the design, and how expensive would it be if they prove false?

## What This Lens Looks For
- Architecture simplification versus architecture theater.
- Hidden dependencies, brittle integrations, and scaling constraints.
- Maintenance burden after the initial project energy is gone.
- Misalignment with platform direction, standards, or engineering principles.
- Places where the design is elegant in isolation but awkward in the real system.

## Common Risks / Failure Modes
- Building a shared abstraction before the problem is stable enough to deserve one.
- Underestimating migration and compatibility complexity.
- Creating a new central dependency with vague ownership and high future maintenance cost.
- Solving for local technical neatness while making the broader system harder to evolve.
- Assuming future scale or reuse without evidence strong enough to justify the upfront cost.

## Signals or Evidence to Consider
- Dependency maps, architecture diagrams, and critical path integrations.
- Existing pain points in delivery speed, reliability, or maintenance load.
- Incident patterns, defect trends, or support burden tied to the current shape of the system.
- Similar past investments that either paid off or quietly became long-term drag.
- Areas where teams are already working around the current architecture.

## Output Expectations
- Name the likely implementation shape and its complexity profile.
- Surface the architectural consequences that are easy to miss in the initial framing.
- Call out hidden dependencies and the conditions under which this becomes hard to support.
- Offer a recommendation that distinguishes between directionally right and execution-ready.

## Recommendation Style
Use grounded, technically candid language. Recommendations should avoid false certainty and should separate strategic soundness from delivery readiness.
