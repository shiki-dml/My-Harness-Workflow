# Implementation Scope Policy

## Purpose
This policy defines the runtime boundary for `implementation_generator`. The agent may implement only the approved sprint contract selected by `harness_orchestrator`.

## Required Inputs
Implementation requires:

- A valid steering contract.
- A valid orchestration decision selecting `implementation_generator`.
- A valid sprint contract.
- Proof that the sprint contract is approved or explicitly authorized for implementation.
- Repository map context.
- Allowed and forbidden file areas.
- Allowed and forbidden change types.
- Acceptance criteria and validation requirements.

## Allowed Runtime Outputs
Runtime outputs are limited to:

- Files explicitly allowed by the sprint contract `allowed_file_areas`.
- Files matching explicitly allowed change types.
- `.harness/state/implementation_runs/IMPLEMENTATION-*.json`
- `.harness/state/implementation_manifest.json`

## Forbidden Runtime Outputs
The agent must not create or modify:

- `.harness/agents/**`
- `AGENTS.md`
- `CODEMAP.md`
- `docs/approval_policy.md`
- `docs/workflow_overview.md`
- `feature_registry.json`, unless explicitly approved by the workflow.
- `docs/sprints/SPRINT-*.md`, unless explicitly routed for contract refresh.
- Deployment files.
- CI/CD files.
- Secret, credential, or permission files.
- Package manager files, unless dependency changes are explicitly allowed and approved.
- QA reports.
- `qa_evaluator` artifacts.
- Later agent directories.

## Sprint Contract Authority
The sprint contract is the implementation authority for scope, non-goals, acceptance criteria, allowed file areas, forbidden file areas, allowed change types, validation requirements, approval gates, and stop conditions.

Anything not explicitly authorized by the sprint contract is forbidden.

## Steering Contract Authority
The steering contract and approval policy override the sprint contract when there is a conflict. If a sprint contract appears to allow work that the steering contract forbids, implementation must block and return to `harness_orchestrator` or `human`.

## Scope Conflict Behavior
When a requested change conflicts with scope, non-goals, file boundaries, change types, or approval policy, the agent must block the change, record the reason, and request routing through `harness_orchestrator`.

## What Counts as Out of Scope
Out-of-scope work includes:

- Any feature not named in the selected sprint contract.
- Adjacent improvements not required by acceptance criteria.
- Product priority changes.
- Control-plane agent changes.
- QA reports or final QA conclusions.
- Dependency, deployment, CI/CD, secret, credential, permission, or security changes without explicit approval.
- Any file or change type not allowed by the sprint contract.
