# Coverage Mapping Policy

## Purpose
Coverage mapping ties feature value and acceptance criteria to concrete validation methods. The matrix must make missing or weak coverage visible.

## Mapping Rules
- Every planned or active feature should have acceptance criteria before complete test planning.
- Every acceptance criterion should have at least one validation method.
- Validation may be automated or manual, but manual-only coverage must be explicit.
- Each important test should map to an acceptance criterion, risk, defect, or contract.
- Verification evidence should map back to acceptance criteria when possible.
- Missing acceptance criteria must be recorded as a strategy gap.
- Do not invent product-changing acceptance criteria.

## Coverage Status Values
Use these values consistently:

- `missing`
- `planned`
- `implemented`
- `passing`
- `failing`
- `flaky`
- `skipped`
- `manual`
- `blocked`
- `unknown`

## Blocking Gaps
A gap blocks verification when the acceptance criterion cannot be considered checked with available evidence. Blocking gaps must include impact, recommended next step, and likely owner agent.

## Reconciliation
When the registry, sprint contract, QA report, and test matrix disagree, preserve the conflict and prefer direct test output over summaries. Escalate status implications to `feature_registry_curator`.
