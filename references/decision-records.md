# Decision And Problem Records

## Purpose

Use `AI_History/` to preserve the compressed reasoning that is expensive to reconstruct. Keep raw session transcripts separate from durable project knowledge.

Write a record when at least one of these is true:

- the team resolved a non-obvious bug;
- an architectural or interface choice was made;
- a data model, pricing rule, workflow, or domain assumption changed;
- an experiment produced a decision-relevant result;
- a plausible approach was rejected for a durable reason;
- a future agent could repeat the same mistake without the record.

Do not create a record for routine edits, formatting, or decisions already captured in a higher-level source of truth.

## File Naming

Use one record per decision or problem:

```text
AI_History/
|-- 2026-09-14-singular-matrix.md
|-- 2026-09-18-transport-model.md
|-- 2026-09-22-reaction-rate.md
`-- architecture-decisions.md
```

Use a date prefix for event records. Use a topic name for living indexes such as `architecture-decisions.md`. Do not rename old records merely to fit a newer convention unless all references can be updated.

## Minimum Schema

```markdown
# <Short Decision Or Problem Title>

- Date: YYYY-MM-DD
- Status: proposed | accepted | rejected | superseded
- Owner: <person or team>
- Related files: <paths or links>

## Context

What situation or constraint made a decision necessary?

## Problem

What failed, was unclear, or needed a choice?

## Options Considered

1. Option A
2. Option B
3. Option C

## Decision

What was chosen and why?

## Consequences

What improves, what becomes harder, and what risks remain?

## Verification

What test, evidence, or review supports the decision?

## Rejected Approaches

Which plausible approaches were rejected, and why?

## Follow-up

What remains unresolved or must be revisited?
```

## Compression Example

A two-hour debugging session can become:

```markdown
# 11x11 Matrix Became Singular

- Date: 2026-09-14
- Status: accepted
- Related files: solveLocalGradients.m

## Problem

The 11x11 system became singular during gradient evaluation.

## Root Cause

Two constraints were linearly dependent, leaving the system rank-deficient.

## Decision

Remove the redundant equation and reformulate the boundary condition.

## Verification

The matrix rank and residual tests pass on the regression case.

## Rejected Approaches

Regularizing the matrix without fixing the redundant constraint hid the
symptom but did not remove the rank deficiency.
```

The goal is not to reproduce the conversation. The goal is to preserve facts another agent would need to avoid repeating the investigation.

## Session Versus Decision Record

- Session: useful for exact commands, tool output, and resuming an interrupted work scene.
- Decision record: useful for understanding why the project is in its current state.
- README/spec: useful for understanding how the project works now.

When these conflict, inspect the actual code, data, and Git history. Treat the most recently verified durable record as context, not as unquestionable truth.