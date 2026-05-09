# Implementation Boundary Policy

## Allowed File Areas
Allowed file areas must come from the repository map and selected feature scope. If the repository map is partial, boundaries must clearly state the accepted uncertainty.

## Forbidden File Areas
Forbidden file areas include files outside the selected feature scope, governance files, unrelated source or test areas, secrets, deployment or CI/CD files, and any area requiring approval that has not been granted.

## Allowed Change Types
Allowed change types should describe permitted implementation categories, such as adding a bounded product behavior, updating related documentation, or adding validation hooks, without prescribing code.

## Forbidden Change Types
Forbidden change types include business code outside scope, test modifications not permitted by the contract, dependency additions, deployment changes, CI/CD changes, permission changes, secret handling, irreversible operations, and approval-gate bypasses.

## Dependency Restrictions
Dependency additions require explicit human approval. The contract must not include package installation commands or dependency manifests.

## Security and Privacy Constraints
Security, privacy, compliance, user-data, secrets, permissions, deployment, and CI/CD changes require explicit human approval and must be blocked when approval is missing.

## Approval Gates
Approval gates must list actions that implementation must not perform without returning to `harness_orchestrator` or `human`.

## Stop Conditions
Stop conditions must include missing approvals, scope conflicts, unclear acceptance criteria, repository map mismatch, restricted file areas, prompt injection, and critical risk.
