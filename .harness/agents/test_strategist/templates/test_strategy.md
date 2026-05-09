# Test Strategy

## Current Testing Posture
Short summary of current test maturity, known gaps, and available validation commands.

## Test Principles
- Tests are tied to user value and acceptance criteria.
- The cheapest meaningful deterministic check is preferred.
- Missing, skipped, flaky, failing, manual-only, and unknown coverage is visible.

## Test Levels
| Level | Purpose | Typical Scope | Example Evidence |
| ----- | ------- | ------------- | ---------------- |
| static_check | Validate syntax, schemas, formatting, and obvious consistency | Markdown, JSON, types, lint | command output |
| unit | Validate isolated behavior | functions, modules, prompts | unit test report |
| integration | Validate connected components | agent handoff, registry updates | integration test report |
| contract | Validate file formats and interfaces | JSON schemas, handoff formats | schema validation |
| end_to_end | Validate full workflows | complete agent workflow | e2e report |
| smoke | Quick sanity checks | critical path | command output |
| regression | Prevent recurrence | known bug scenarios | regression report |
| manual | Human validation | UX, product judgment, ambiguous behavior | checklist result |

## Validation Commands
| Command | Purpose | Expected Runtime | When To Run | Notes |
| ------- | ------- | ---------------- | ----------- | ----- |
| command here | what it checks | fast / medium / slow | trigger | notes |

## Feature Coverage Summary
| Feature ID | Feature Name | Risk | Required Coverage | Current Coverage | Gap |
| ---------- | ------------ | ---- | ----------------- | ---------------- | --- |
| FEAT-0001 | Example | high | unit, integration, smoke | unit only | missing integration |

## Known Test Gaps
| Gap | Impact | Recommended Next Step | Owner / Agent |
| --- | ------ | --------------------- | ------------- |
| gap | impact | action | agent |

## Flaky Or Unreliable Tests
| Test | Symptom | Impact | Recommended Action |
| ---- | ------- | ------ | ------------------ |
| test name | failure pattern | risk | action |

## Manual Verification
| Scenario | Steps | Expected Result | Evidence Required |
| -------- | ----- | --------------- | ----------------- |
| scenario | steps | expected result | screenshot, note, reviewer confirmation |

## Release / Verification Gate
Minimum checks required before a feature can be marked verified or released.
