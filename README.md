# AI Workspace Continuity

A Codex skill for making project context durable across AI providers, agents, accounts, and sessions.

**Version:** `1.0.1`

## What It Does

The skill treats the workspace, not chat history, as the project's source of truth. It helps an agent:

- audit project continuity;
- create or update `README.md` and `AGENTS.md`;
- add a `CLAUDE.md` pointer without duplicating rules;
- record decisions under `AI_History/`;
- use Git checkpoints safely;
- keep secrets, customer data, large files, models, and generated output out of ordinary Git;
- prepare a workspace so another model or agent can resume it from local files.

## Install

Place the skill folder under the Codex skills directory:

```text
%USERPROFILE%\.codex\skills\ai-workspace-continuity
```

The folder should contain:

```text
SKILL.md
agents/openai.yaml
scripts/audit_workspace.py
scripts/init_workspace.py
references/workspace-spec.md
references/decision-records.md
```

## Usage

In a Codex task, invoke it explicitly:

```text
使用 $ai-workspace-continuity 对当前工作区做增量治理：先只读审计，保留现有 README.md、AGENTS.md、CLAUDE.md、.gitignore 和用户未提交改动，只补缺失治理文件；不移动或删除数据；提交前检查敏感文件和大文件；如果工作区已有未提交改动，不要自动提交，否则只提交治理文件；不配置远端、不推送。
```

For audit only:

```text
使用 $ai-workspace-continuity 对当前工作区做一次只读审计，不修改任何文件。
```

## Scripts

Audit only:

```powershell
python scripts/audit_workspace.py "C:\path\to\project" --json --large-mb 20 --max-files 30000
```

Dry-run scaffolding:

```powershell
python scripts/init_workspace.py "C:\path\to\project" --language zh
```

Write scaffolding after reviewing the dry run:

```powershell
python scripts/init_workspace.py "C:\path\to\project" --language zh --write
```

The initializer does not initialize Git, commit, push, or overwrite existing files.

## Safety

- Chat history is not the authoritative project record.
- Customer data, contracts, pricing, credentials, private paths, and internal tool output are sensitive by default.
- Never publish secrets, `.env` files, SSH keys, tokens, or raw agent-session state.
- A backup is not publication, and a Git commit is not a backup.
- Data-heavy or mixed-purpose roots should use an explicit repository boundary or a default-deny allowlist.

## Validation

```powershell
python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" "$env:USERPROFILE\.codex\skills\ai-workspace-continuity"
python -m py_compile scripts/audit_workspace.py scripts/init_workspace.py
```

## Changelog

See `CHANGELOG.md`.

## License

MIT License. See `LICENSE`.
