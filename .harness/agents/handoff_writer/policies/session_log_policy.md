# Session Log Policy

`SESSION_LOG.jsonl` is append-only in normal operation.

Each appended line must be one standalone valid JSON object. The line must not depend on previous lines for validity or meaning.

## Required Fields
Each entry must include:

- `timestamp`
- `session_id`
- `trigger`
- `agents_involved`
- `summary`
- `files_changed`
- `feature_ids`
- `validation`
- `decisions`
- `risks`
- `next_actions`

## Append Rules
- Append exactly one entry for the current handoff session unless blocked.
- Do not rewrite prior entries except under explicit repair mode and with approval.
- Do not remove prior entries.
- Do not append invalid JSON.
- Do not use comments or trailing commas.
- Do not use placeholder values when actual values are unknown. Use empty arrays or explicit `unknown` status records where appropriate.
