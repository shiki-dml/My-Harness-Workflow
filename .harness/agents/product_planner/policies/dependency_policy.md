# Dependency Policy

## Product Dependencies
Product dependencies are relationships between capabilities, user flows, or outcomes. They describe what product decision or capability must exist before another feature makes sense.

## Repository Dependencies
Repository dependencies come from the repository map, such as missing scaffold artifacts, unknown areas, or relevant documentation locations. They must not prescribe code changes.

## Human Decision Dependencies
Human decision dependencies include unresolved scope questions, priority tradeoffs, user or stakeholder decisions, and explicit acceptance of product direction.

## Approval Dependencies
Approval dependencies include any action requiring human approval, such as expanding scope, changing the project goal, approving a feature for sprint, changing approved statuses, or handling privacy, security, compliance, or user-data-sensitive decisions.

## What Must Not Be Treated as an Implementation Dependency
Implementation libraries, file-level changes, source code structure choices, test design, deployment steps, and architecture decisions must not be introduced as product planning dependencies.

## Dependency Blocking Behavior
If a dependency prevents safe planning, the related feature must be marked `blocked` or `deferred`, and the dependency must be recorded for `harness_orchestrator`.
