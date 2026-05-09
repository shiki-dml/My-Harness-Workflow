# Validation Command Policy

## Purpose
Validation commands give future agents repeatable evidence paths. Commands must be concrete, scoped, and honest about whether they were run.

## Command Record Requirements
For each command, record:

- Command.
- Purpose.
- Expected runtime if known.
- When to run it.
- Required environment or dependencies.
- Safety classification.
- Expected evidence output.
- Status: `run`, `skipped`, `unknown`, or `not_applicable`.

## Safety Classification
Use these classifications:

- `cheap`: Fast and routine.
- `safe`: Non-destructive but may take longer than cheap checks.
- `medium`: Useful but not appropriate for every loop.
- `expensive`: Slow or resource-heavy.
- `destructive`: May delete, mutate, deploy, or irreversibly change state.
- `environment_sensitive`: Requires services, secrets, browsers, network, hardware, or external state.
- `unknown`: Safety has not been established.

## Evidence Rules
- Do not claim a command passed unless it was run and output is available.
- If the command was not run, mark it `skipped` or `unknown`.
- Do not treat stale command output as fresh evidence.
- Failed output remains evidence and must not be hidden.
- Flaky output must be recorded as flaky, not passing.
- Separate local validation from CI validation.
- Separate required checks from optional checks.

## Approval Rules
Do not recommend destructive commands as default validation. Do not run expensive, destructive, or environment-sensitive checks unless the current orchestration decision and approval context allow it.
