---
name: ai-workspace-continuity
description: "Create, audit, or update durable, model-agnostic AI project workspaces. Use when project context, decisions, code, data, or delivery assets must survive changes of AI provider, agent, account, or session; or when a project needs README/AGENTS context, AI_History decision records, Git checkpoints, backup boundaries, or secret hygiene."
metadata:
  version: 1.0.0
  updated: 2026-09-21
---

# AI Workspace Continuity

Treat the workspace, not a model account or chat history, as the project's source of truth. Optimize so a different agent can resume the project from files without access to the previous conversation.

## Mental Model

- **Workspace**: source code, data, documents, papers, results, and other project assets.
- **Knowledge**: `README.md`, agent instructions, architecture notes, SOPs, and compressed decision records.
- **Session**: raw chat transcripts, tool traces, and terminal logs. Use these to recover a work scene, not as the permanent knowledge base.

Changing the provider, model, agent, or account should change only the compute/execution layer. It should not remove project context.

## Choose The Mode

Infer the narrowest applicable mode from the request:

- **Audit**: inspect an existing workspace and report missing continuity controls without modifying it.
- **Bootstrap**: safely create missing context files in a new or unprepared project.
- **Decision record**: capture a significant problem, choice, or rejected approach.
- **Checkpoint**: prepare a Git checkpoint after a verified, coherent change.
- **Handoff**: write enough context for another person or agent to resume safely.

## Workflow

1. Inspect before changing anything. Read existing project instructions and relevant docs. Check Git state, file sensitivity, and whether the project is too large or data-heavy for one repository.
2. For an audit, run:

   ```bash
   python <skill-dir>/scripts/audit_workspace.py <project-path> --json
   ```

   Treat its findings as evidence, not as a mandate to mutate the workspace.
3. For safe scaffolding, run the initializer in dry-run mode first:

   ```bash
   python <skill-dir>/scripts/init_workspace.py <project-path>
   ```

   Add `--write` only after the user has authorized those files to be created. The initializer must never overwrite existing files and must never initialize Git, commit, or push.
4. Keep one canonical agent-instruction source. Prefer `AGENTS.md` as canonical. `CLAUDE.md`, if present, should be a short pointer to it so competing rule sets do not drift.
5. After meaningful debugging, architecture work, data changes, or agent-assisted refactoring, write a compact decision record under `AI_History/`. Read `references/decision-records.md` for the schema and examples.
6. Use Git checkpoints around working states. Commit only when the user explicitly requests a local commit. Push only when the user explicitly requests publication. A commit is not a backup, and a backup is not a publication.
7. Close a session by updating only the durable artifacts that changed: `README.md`, agent instructions, decision records, specs, or a handoff note. Report absolute paths and unresolved risks.

## Safety Boundaries

- Never treat chat history as the authoritative project record.
- Treat customer data, contracts, pricing, credentials, private paths, and internal tool output as sensitive unless the project explicitly says otherwise.
- Never place secrets, `.env` files, SSH keys, tokens, password stores, or raw agent-session state into a public repository.
- Do not default to initializing one Git repository over an entire data-heavy or mixed-purpose root. Prefer repositories per code/knowledge unit, with a manifest and separate backup for large or sensitive assets.
- Do not delete or replace a malformed `.git` directory without explicit confirmation after verifying it contains no usable history.
- Backups and public sharing are separate decisions. A project may need a private remote, encrypted archive, NAS copy, or no remote at all.

## Required Outcomes

For an audit or bootstrap, ensure the project has or explicitly lacks:

```text
README.md             human project entry point
AGENTS.md             canonical agent-readable rules
CLAUDE.md             optional pointer to AGENTS.md
AI_History/           decision and problem records
.gitignore            secret/generated-file boundaries
docs/                 optional durable human documentation
```

Do not create empty directories merely to match a diagram. Add a structure only when it has a real role.

## References

- Read `references/workspace-spec.md` when deciding directory roles, data/repository boundaries, backup classes, or what belongs in the workspace.
- Read `references/decision-records.md` when recording a debugging result, design decision, experiment outcome, architecture change, or rejected approach.
- Use `scripts/audit_workspace.py` for evidence-based workspace checks.
- Use `scripts/init_workspace.py` for non-overwriting scaffolding.