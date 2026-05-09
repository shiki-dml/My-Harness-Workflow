# My Harness Workflow

**Language:** English | [中文](README.zh-CN.md)

This is a contract-driven agent harness workspace. It currently includes three executable harnesses:

- Contract Validation Harness: validates `.harness/agents/*` contracts, schemas, examples, and code line budgets.
- Issue Triage Harness: runs a full 11-agent issue triage, sprint planning, QA, and handoff workflow from an offline GitHub-like fixture.
- Release Readiness Harness: models release engineering for a FastAPI-inspired Python API framework, including dependencies, CI matrix, risk gates, validation strategy, and handoff.

The design is intentionally compact: split agent work into verifiable contracts, explicit state, reproducible inputs, machine-checkable outputs, and end-to-end tests. Runtime code has no third-party dependency, and the self-check enforces a 300-line budget for Python code files.

## Quick Start

```powershell
python -m harness .
python -m harness . --json
python -m harness issue-triage examples\issue_triage\issues.json --capacity 13
python -m harness release-readiness examples\release_readiness\manifest.json --risk-budget 72
python -m unittest discover -s tests -v
```

## Architecture

![My Harness Workflow architecture](docs/assets/harness-architecture.png)

## Existing Agents

| Agent | Role |
| --- | --- |
| `human_steering` | Captures goals, constraints, approvals, risks, and stop conditions. |
| `harness_orchestrator` | Routes the workflow, enforces phase order, and blocks unsafe progress. |
| `initializer_agent` | Initializes or normalizes task input into a stable working shape. |
| `repo_cartographer` | Maps the repository or fixture source so later stages know what exists. |
| `product_planner` | Converts inputs into prioritized product/backlog decisions. |
| `sprint_contract_agent` | Creates bounded sprint contracts with acceptance criteria and capacity. |
| `implementation_generator` | Produces scoped implementation plans or change records. |
| `qa_evaluator` | Independently checks acceptance criteria, validation results, and risks. |
| `handoff_writer` | Produces handoff summaries and next-step records. |
| `feature_registry_curator` | Maintains stable feature records and duplicate/status reconciliation. |
| `test_strategist` | Plans validation commands, coverage, and regression strategy. |

## Harness Architectures

Each harness is intentionally small, explicit, and testable. The sections below show the boundary, entrypoint, files, agent coverage, and execution flow for each architecture.

---

## Harness Architecture 01 - Contract Validation Harness

**Detailed README:** [harness/README.md](harness/README.md)

**Purpose:** validate the control-plane contracts that define the available agents.

**Entrypoint:**

```powershell
python -m harness .
python -m harness . --json
```

**At a glance:**

| Aspect | Design |
| --- | --- |
| Input | `.harness/agents/*` contract directories |
| Output | `PASS/FAIL` report with structured findings |
| Scope | Agent specs, JSON schemas, examples, interface shape, Python line budget |
| Runtime dependency | Python standard library only |
| Failure mode | Non-zero exit code when any error-level finding exists |

**Core files:**

| File | Purpose |
| --- | --- |
| [harness/common.py](harness/common.py) | Shared agent pipeline, JSON loading, input validation, status rendering, and common guard helpers. |
| [harness/core.py](harness/core.py) | Discovers agents, validates required files, checks JSON schemas/examples, and enforces Python line budget. |
| [harness/__main__.py](harness/__main__.py) | CLI entrypoint for contract validation and executable sample harnesses. |
| [harness/__init__.py](harness/__init__.py) | Public Python API exports. |
| [tests/test_harness.py](tests/test_harness.py) | Regression tests for schema validation, agent checks, CLI JSON, and line-budget enforcement. |

**Agents used:**

- Discovers and validates every agent under `.harness/agents/*`.
- It does not execute agent behavior; it verifies contracts, schemas, examples, and support files.

**Architecture flow:**

```mermaid
%%{init: {"theme":"base","flowchart":{"curve":"linear","htmlLabels":true},"themeVariables":{"background":"#ffffff","mainBkg":"#ffffff","primaryTextColor":"#0f172a","fontSize":"20px","lineColor":"#334155"}}}%%
flowchart LR
    A["Input<br/>Project Root"] --> B["Discover<br/>Agent Specs"]
    B --> C["Validate<br/>Files + Schemas"]
    C --> D["Validate<br/>Examples"]
    D --> E["Check<br/>300-Line Budget"]
    E --> F{"Clean?"}
    F -->|Yes| G["PASS"]
    F -->|No| H["FAIL<br/>Findings"]
    classDef source fill:#eff6ff,stroke:#2563eb,stroke-width:3px,color:#0f172a
    classDef step fill:#f0fdf4,stroke:#16a34a,stroke-width:3px,color:#0f172a
    classDef decision fill:#fefce8,stroke:#ca8a04,stroke-width:3px,color:#0f172a
    classDef result fill:#fff7ed,stroke:#f97316,stroke-width:3px,color:#0f172a
    class A source
    class B,C,D,E step
    class F decision
    class G,H result
    linkStyle default stroke:#334155,stroke-width:3px
```

---

## Harness Architecture 02 - Issue Triage Harness

**Detailed README:** [examples/issue_triage/README.md](examples/issue_triage/README.md)

**Purpose:** run a realistic but compact GitHub issue triage workflow from offline fixture data.

**Entrypoint:**

```powershell
python -m harness issue-triage examples\issue_triage\issues.json --capacity 13
python -m harness issue-triage examples\issue_triage\issues.json --capacity 13 --json
```

**At a glance:**

| Aspect | Design |
| --- | --- |
| Input | Offline GitHub-like issue/PR JSON fixture |
| Output | Backlog, related groups, sprint contract, test strategy, QA, handoff |
| Scope | Full 11-agent workflow from steering to handoff |
| Runtime dependency | Python standard library only |
| Failure mode | Non-zero exit code when QA invariants fail |

**Core files:**

| File | Purpose |
| --- | --- |
| [harness/issue_triage.py](harness/issue_triage.py) | Normalizes issues, detects related issues, ranks backlog, packs sprint capacity, creates QA and handoff output. |
| [examples/issue_triage/issues.json](examples/issue_triage/issues.json) | Offline GitHub-like issue/PR fixture. |
| [examples/issue_triage/README.md](examples/issue_triage/README.md) | Detailed guide for the issue triage harness. |
| [tests/test_issue_triage.py](tests/test_issue_triage.py) | End-to-end tests for all-agent execution, scoring, duplicate detection, capacity, CLI JSON, and invalid input. |

**Agents used:**

1. `human_steering`
2. `harness_orchestrator`
3. `initializer_agent`
4. `repo_cartographer`
5. `feature_registry_curator`
6. `product_planner`
7. `sprint_contract_agent`
8. `implementation_generator`
9. `test_strategist`
10. `qa_evaluator`
11. `handoff_writer`

**Architecture flow:**

```mermaid
%%{init: {"theme":"base","flowchart":{"curve":"linear","htmlLabels":true},"themeVariables":{"background":"#ffffff","mainBkg":"#ffffff","primaryTextColor":"#0f172a","fontSize":"20px","lineColor":"#334155"}}}%%
flowchart LR
    A["Input<br/>Issue JSON"] --> B["Steer + Route<br/>human / orchestrator"]
    B --> C["Normalize + Map<br/>initializer / cartographer"]
    C --> D["Register + Rank<br/>registry / planner"]
    D --> E["Sprint Contract<br/>contract agent"]
    E --> F["Plan + Test<br/>implementation / test strategist"]
    F --> G["QA + Handoff<br/>evaluator / writer"]
    classDef source fill:#eff6ff,stroke:#2563eb,stroke-width:3px,color:#0f172a
    classDef stage fill:#f0fdf4,stroke:#16a34a,stroke-width:3px,color:#0f172a
    classDef output fill:#fff7ed,stroke:#f97316,stroke-width:3px,color:#0f172a
    class A source
    class B,C,D,E,F stage
    class G output
    linkStyle default stroke:#334155,stroke-width:3px
```

---

## Harness Architecture 03 - Release Readiness Harness

**Detailed README:** [examples/release_readiness/README.md](examples/release_readiness/README.md)

**Purpose:** evaluate whether a FastAPI-inspired Python API framework release is ready to ship under a defined risk budget.

**Entrypoint:**

```powershell
python -m harness release-readiness examples\release_readiness\manifest.json --risk-budget 72
python -m harness release-readiness examples\release_readiness\manifest.json --risk-budget 72 --json
```

**At a glance:**

| Aspect | Design |
| --- | --- |
| Input | Offline release manifest inspired by FastAPI dependency and CI concerns |
| Output | Dependency graph, change registry, risk ledger, release contract, QA, handoff |
| Scope | Full 11-agent release workflow from steering to release handoff |
| Runtime dependency | Python standard library only |
| Failure mode | Non-zero exit code when release QA invariants fail |

**Core files:**

| File | Purpose |
| --- | --- |
| [harness/release_readiness.py](harness/release_readiness.py) | Normalizes release manifests, builds dependency graph, scores release risk, creates release contract, QA, and handoff. |
| [examples/release_readiness/manifest.json](examples/release_readiness/manifest.json) | Offline FastAPI-inspired release fixture. |
| [examples/release_readiness/README.md](examples/release_readiness/README.md) | Detailed guide for the release readiness harness. |
| [tests/test_release_readiness.py](tests/test_release_readiness.py) | Tests for agent coverage, dependency graph, risk budget, test matrix, CLI JSON, and invalid manifests. |

**Agents used:**

1. `human_steering`
2. `harness_orchestrator`
3. `initializer_agent`
4. `repo_cartographer`
5. `feature_registry_curator`
6. `product_planner`
7. `sprint_contract_agent`
8. `implementation_generator`
9. `test_strategist`
10. `qa_evaluator`
11. `handoff_writer`

**Architecture flow:**

```mermaid
%%{init: {"theme":"base","flowchart":{"curve":"linear","htmlLabels":true},"themeVariables":{"background":"#ffffff","mainBkg":"#ffffff","primaryTextColor":"#0f172a","fontSize":"20px","lineColor":"#334155"}}}%%
flowchart LR
    A["Input<br/>Release Manifest"] --> B["Steer + Route<br/>release boundary"]
    B --> C["Normalize + Map<br/>manifest + source"]
    C --> D["Registry + Risk<br/>changes + risk ledger"]
    D --> E["Release Contract<br/>risk budget gate"]
    E --> F["Plan + CI Matrix<br/>actions + tests"]
    F --> G["QA + Handoff<br/>ship / block"]
    classDef source fill:#eff6ff,stroke:#2563eb,stroke-width:3px,color:#0f172a
    classDef stage fill:#f0fdf4,stroke:#16a34a,stroke-width:3px,color:#0f172a
    classDef output fill:#fff7ed,stroke:#f97316,stroke-width:3px,color:#0f172a
    class A source
    class B,C,D,E,F stage
    class G output
    linkStyle default stroke:#334155,stroke-width:3px
```

---

## Quality Gates

The current verification chain is:

```powershell
python -m unittest discover -s tests -v
python -m harness .
python -m harness issue-triage examples\issue_triage\issues.json --capacity 13
python -m harness release-readiness examples\release_readiness\manifest.json --risk-budget 72
python -m py_compile harness\__init__.py harness\__main__.py harness\common.py harness\core.py harness\issue_triage.py harness\release_readiness.py tests\test_harness.py tests\test_issue_triage.py tests\test_release_readiness.py
```

Expected results:

- 24 tests pass.
- `python -m harness .` returns `PASS: 11 agent(s) checked`.
- Issue triage returns `PASSED`, `agents: 11/11`, and a capacity-respecting sprint.
- Release readiness returns `PASSED`, `agents: 11/11`, and a risk-budget-respecting release contract.
