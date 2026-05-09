# File Discovery Policy

## Static Inspection Only
`repo_cartographer` may inspect repository paths and selected text files statically. It must not execute project code or arbitrary project scripts.

## Allowed Inspection Targets
Allowed inspection targets include:

- File and directory names.
- File paths.
- File extensions.
- Small governance and documentation files.
- Harness agent definition files.
- Known configuration files by summary only.
- Scripts by static reading only.

## Restricted Paths
Restricted paths include:

- `.git/**`
- `node_modules/**`
- `vendor/**`
- `dist/**`
- `build/**`
- `coverage/**`
- `.venv/**`
- `venv/**`
- `__pycache__/**`
- `.pytest_cache/**`
- `.mypy_cache/**`
- `.DS_Store`
- Binary files.
- Large generated files.
- `.env`
- `.env.*`
- Secret files.
- Key files.
- Certificate files.
- Credential files.

## Ignored Paths
Ignored paths should be recorded by path and reason. Ignoring a path must not hide a safety risk; restricted or unknown paths should be surfaced in the repository map without exposing contents.

## Secret and Credential Handling
Secret values, tokens, private keys, certificates, credentials, and environment values must not be printed. The map may record that a restricted path exists and classify it as `restricted_sensitive`.

## Large or Binary File Handling
Large or binary files should be listed by path, size if known, and category only. Their contents must not be printed.

## No External Network Rule
`repo_cartographer` must not call external networks, package registries, remote APIs, or external services.

## No Script Execution Rule
Scripts may be read statically only. The agent must not execute project scripts, build tools, package commands, or commands that may modify the repository.
