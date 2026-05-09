# Feature Selection Policy

## Required Feature Inputs
The agent requires exactly one selected feature with feature ID, title, problem statement, user value, scope, non-goals, acceptance criteria, priority, risk, dependencies, assumptions, open questions, and status.

## Eligible Feature Statuses
A feature is eligible when one of these is true:

- The selected feature status is `approved_for_sprint`.
- The selected feature status is `proposed` and explicit human approval for sprint contracting is present.
- The selected feature status is `blocked` and the contract is being created in `plan_only` mode to clarify blockers.
- `harness_orchestrator` explicitly accepted partial planning and routed the feature for contract drafting.

## Ambiguous Feature Handling
If the selected feature is ambiguous, missing, duplicated, or conflicts with non-goals, the agent must block and return to `harness_orchestrator` or `human`.

## Blocked Feature Handling
Blocked features may be used only in `plan_only` mode to clarify blockers unless explicit human approval authorizes drafting.

## Duplicate Feature Handling
If duplicate feature IDs or multiple selected features are present, the agent must stop unless explicit human approval allows a multi-feature sprint.

## Human Approval for Unapproved Features
Creating a contract for a feature not approved for sprint requires explicit human approval. Missing approval is not approval.

## Feature Status Recommendation Rules
The agent may recommend a feature status update, but it must not modify `feature_registry.json` directly unless explicitly approved by the workflow. It must not mark a sprint contract as human-approved without explicit approval.
