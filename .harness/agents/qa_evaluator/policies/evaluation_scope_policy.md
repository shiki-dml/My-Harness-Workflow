# Evaluation Scope Policy

## Purpose
This policy defines the QA evaluation boundary for `qa_evaluator`. The agent evaluates implementation output against authorized contracts and evidence without modifying implementation files or product artifacts.

## Required Inputs
QA evaluation requires:

- A valid steering contract.
- A valid orchestration decision selecting `qa_evaluator`.
- A valid sprint contract.
- A valid implementation result or explicitly accepted partial implementation state.
- Repository map context.
- Changed file list.
- Acceptance criteria.
- Validation requirements.
- Approval policy.

## Allowed Runtime Outputs
Runtime QA outputs are limited to:

- `docs/qa/QA-*.md`
- `.harness/state/qa_runs/QA-*.json`
- `.harness/state/qa_manifest.json`

## Forbidden Runtime Outputs
The agent must not create or modify:

- `README.md`
- `AGENTS.md`
- `CODEMAP.md`
- `docs/approval_policy.md`
- `docs/workflow_overview.md`
- `docs/project_overview.md`
- `docs/product_backlog.md`
- `docs/product_roadmap.md`
- `docs/sprints/SPRINT-*.md`
- `feature_registry.json`
- `PROGRESS.md`
- `src/**`
- `tests/**`
- `scripts/**`
- Dependency manifests.
- Deployment or CI/CD files.
- Secret, credential, or permission files.
- Implementation result files.
- Implementation source artifacts.
- `.harness/agents/**`

## Authorized Sources of Truth
QA conclusions must be based only on:

1. `steering_contract`
2. `sprint_contract`
3. `acceptance_criteria`
4. `implementation_result`
5. `implementation_report`
6. `repository_map`
7. `approval_policy`
8. Allowed validation evidence

## Evaluation Boundaries
`qa_evaluator` evaluates whether implementation satisfies the sprint contract. It must not repair defects, rewrite tests, change contracts, update implementation artifacts, change product direction, or approve release.

## Scope Conflict Behavior
Scope conflicts, unauthorized file changes, forbidden change types, or approval-gate violations must be recorded as findings or defects and routed through `harness_orchestrator`.

## What Counts as Out of Scope
Out-of-scope work includes code changes, test changes, contract edits, backlog changes, release approvals, dependency changes, deployment changes, CI/CD changes, secret or permission changes, and any non-QA artifact modification.
