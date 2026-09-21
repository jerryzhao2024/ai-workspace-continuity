# Workspace Specification

## Purpose

Use this reference when deciding what belongs in a project, what should be versioned, and how continuity can survive an agent, model, or provider change.

## Directory Roles

| Path | Purpose | Typical retention |
|---|---|---|
| `src/` | Executable source, scripts, tests, application code | Track in Git |
| `data/` | Raw, processed, or reference data plus schemas/manifests | Selectively track; often external |
| `docs/` | Human-readable specifications, architecture, operations, and SOPs | Track in Git |
| `papers/` | Papers, standards, reports, reading notes, citations | Track metadata and notes; large binaries optional |
| `results/` | Experiment output, figures, reports, metrics, generated deliverables | Track source/parameters; large output optional |
| `AI_History/` | Compressed decisions, problem resolutions, rejected approaches | Track in Git |
| `README.md` | Human entry point and project navigation | Track in Git |
| `AGENTS.md` | Canonical agent-readable rules and constraints | Track in Git |
| `CLAUDE.md` | Optional pointer to `AGENTS.md` | Track if used |
| `.git/` | Local version database | Never copy manually |

Do not create directories that have no concrete role. Empty structure is not continuity.

## Knowledge Ownership

- `README.md` answers: What is this? Why does it exist? What works now? How is it run? What is unresolved?
- `AGENTS.md` answers: What may an agent change? What is forbidden? What tests are required? What domain assumptions and data boundaries apply?
- `AI_History/` answers: What problem occurred? Why was this solution chosen? What changed? Which alternatives were rejected?
- `docs/` answers: What are the stable specifications and operating procedures?
- Session transcripts answer: What exactly happened in one work session?

Keep agent instructions in one canonical place. If both `AGENTS.md` and `CLAUDE.md` are required by different tools, make one point to the other instead of duplicating an entire ruleset.

## Repository Boundary

A workspace is a logical source of truth; it does not have to be one Git repository.

Track in Git when content is:

- text-based or reasonably diffable;
- important for understanding or reproducing the project;
- safe to place in the selected remote's visibility model;
- not so large that normal Git workflows become unreliable.

Keep outside normal Git when content is:

- personal, customer, contract, credential, or regulated data;
- a very large binary, model, video, raw archive, or dataset;
- reproducible but expensive output that can be regenerated from tracked inputs;
- licensed material that cannot be redistributed.

For external assets, keep a manifest in the repository. Record at least: asset identifier, source, owner, date, version, checksum when practical, storage location, access class, and retention rule.

## Data And Access Classes

Use the project's own policy when one exists. Otherwise classify conservatively:

- **Public**: may be published after review.
- **Internal**: internal business context; private storage only.
- **Confidential**: customer, pricing, contracts, personal data, or sensitive operational details.
- **Restricted**: credentials, keys, regulated data, export-controlled material, or content with legal restrictions.

The access class controls model use, repository visibility, backup encryption, and who may receive the content. Do not upload confidential or restricted data to an external model or public service without explicit authorization and an applicable policy.

## Git Checkpoint Rhythm

Use checkpoints around verified, coherent states:

```text
Working baseline -> commit
Feature added -> test -> commit
Refactor completed -> test -> commit
Experiment -> branch
Failure -> rollback or abandon branch
```

Before staging, review:

- `git status --short`
- the diff for the files being committed
- generated files and accidental secrets
- whether the commit contains one understandable change

Never use Git as the only backup. Never push merely because a local commit exists.

## Backup Classes

Choose by recovery requirement and sensitivity, not by file count:

- **Source/knowledge**: private Git remote plus a second independent copy.
- **Client/data assets**: encrypted backup to approved storage; verify restoration.
- **Large generated output**: retain only if expensive or impossible to regenerate; otherwise keep the recipe and a checksum.
- **Agent sessions/config**: optional operational backup, access-controlled, never public by default.

For important projects, aim for at least three copies, two storage media or systems, and one off-site copy. Document the restore procedure and test it periodically.

## Minimum Continuity Package

A new agent should be able to answer these questions without the previous chat:

1. What is the project and its current state?
2. Which files are authoritative?
3. How is the project run or used?
4. What rules and constraints apply?
5. What important decisions have already been made?
6. Which data is sensitive or external?
7. What has been tested, and what remains unresolved?