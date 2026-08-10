---
name: design-review-gate
description: Scope-first, invariant-driven workflow for reviewing low-level designs and architecture specifications without turning bounded phases or MVPs into open-ended platforms. Use when drafting, tightening, reviewing, or deciding merge readiness for an MVP or other bounded design phase; when repeated review comments are causing churn; or when another agent must implement the next bounded slice autonomously.
---

# Design Review Gate

Make a design safe and implementation-ready for its next bounded slice without
pre-specifying the whole product. Treat implementation-ready as: an agent can
complete that slice autonomously until it reaches an explicit owner gate. Do not
interpret it as every future product decision being settled.

Maintain four lightweight artifacts in the repository's existing design system.
Keep them together in one document or link them from canonical design pages; do
not impose new files when a table or section fits an existing page.

## 1. Freeze the scope contract

Read the repository guidance and canonical architecture decisions first. Find
the owner of each existing fact before proposing new detail.

Agree on this priority order before expanding low-level design:

1. Keep the frozen phase internally consistent and safe.
2. Specify enough for the next implementation slice.
3. Apply broader best practices only when that scope requires them.

Create or update a **scope contract**:

| Field | Required decision |
| --- | --- |
| Objective | User-visible outcome for this phase |
| Next slice | Concrete start and end boundary for implementation |
| Assumptions | Deployment, trust, scale, actors, and operating model |
| Required capabilities | Behaviors that must exist in this slice |
| Explicit non-goals | Plausible features intentionally excluded |
| Accepted risks | Known limitations the owner accepts for this phase |
| Owner gates | Decisions or values implementation must stop and request |
| Priority order | Tie-breaker when safety, scope, and completeness compete |

Do not invent a material owner decision. Ask for it when it changes scope or
safety; otherwise record a named owner gate so implementation can progress up to
that point. Freeze the contract before reviewing implementation details. Route a
later scope change through an explicit owner decision.

Never add deferred infrastructure merely because it is a generic industry best
practice. First show which in-scope requirement or invariant demands it. Prefer
removing an unnecessary feature over fully designing it.

## 2. Specify invariants before prose

Write the smallest contracts needed to make interactions complete. Keep each
fact in one canonical place and link to it elsewhere. Avoid copying state,
authority, or failure rules across documents.

Cover the applicable interaction surfaces with compact matrices:

- **Authority:** resource or command, creator, authorizer, reader, mutator, and
  required proof.
- **State:** every state, entry event, exit event, failure/recovery path, and
  resource or reservation effect.
- **Transaction:** each external effect, durable intent, commit boundary,
  unknown-commit behavior, idempotency/retry rule, and reconciliation evidence.
- **Failure:** boundary, failure mode, safe outcome, recovery trigger, and
  operator-visible evidence.

Check every request, state, timestamp, external effect, and persistent record
against those matrices. Turn load-bearing guarantees into an **invariant
checklist**:

| ID | Invariant | Canonical location | Verification | Status |
| --- | --- | --- | --- | --- |
| INV-001 | One precise safety or correctness guarantee | Link/section | Test, trace, or review evidence | Open/Met |

Keep stable IDs. Preserve this checklist across rewrites and compression passes;
never remove or weaken a resolved invariant silently. Mark an invariant changed
only with its scope decision and replacement guarantee.

## 3. Review by domain, then triage once

Review the frozen candidate in focused passes. Run them independently, and in
parallel when agent capacity permits:

1. Scope and non-goals.
2. Authority, trust, and security boundaries.
3. State machines and lifecycle completeness.
4. Transactions, idempotency, failure, and recovery.
5. Implementability, operations, and owner gates for the next slice.

Give every reviewer this brief:

> Review only the frozen scope and next implementation slice. For each finding,
> name the violated requirement or invariant and explain whether it blocks that
> slice. Do not recommend deferred infrastructure unless an in-scope guarantee
> requires it.

Collect findings before editing. Maintain a **feedback ledger**:

| ID | Finding | Class | Invariant or requirement | Decision | Disposition | Status |
| --- | --- | --- | --- | --- | --- | --- |
| REV-001 | Concise issue | Blocker/Clarify/Defer/Out of scope | ID or scope field | Accept/Reject | Canonical edit or deferred location | Open/Closed |

Classify findings consistently:

- **Blocker:** prevent the next slice from proceeding, violate an in-scope safety
  invariant, or make a required outcome unreachable.
- **Clarify:** remove implementation ambiguity without expanding scope.
- **Defer:** capture a valid future requirement outside the current slice.
- **Out of scope:** reject a suggestion that has no current requirement or
  invariant; record the reason without designing it.

Do not equate a comment with an obligation to edit. Do not use unresolved comment
count as a quality metric.

## 4. Batch corrections and protect settled decisions

Group accepted findings by root cause. Make one coherent correction pass across
canonical sources, diagrams, and tests instead of pushing once per comment.
Update links and derived summaries after the canonical rule changes.

Before accepting the pass:

- Re-run every previously met invariant against the diff.
- Check that simplification did not erase authority, locking, ordering, retry,
  recovery, or fail-closed guarantees.
- Remove newly unnecessary detail rather than completing it speculatively.
- Keep deferred work in the ledger or backlog, not in executable current-phase
  contracts.

Freeze a candidate after the batch. Triage new feedback against the same ledger
before changing it; do not reopen the whole design automatically.

## 5. Apply the merge gate

Create or update a **merge gate** for the frozen candidate:

| Gate | Evidence | Result |
| --- | --- | --- |
| Candidate identity | Exact commit or immutable revision | Pass/Fail |
| Scope | Contract frozen; non-goals and accepted risks explicit | Pass/Fail |
| Implementability | Next slice can proceed until a named owner gate | Pass/Fail |
| Invariants | No unresolved in-scope safety or correctness blocker | Pass/Fail |
| Interactions | Authority, state, transaction, and failure paths complete for the slice | Pass/Fail |
| Consistency | One canonical source per fact; links and diagrams agree | Pass/Fail |
| Validation | Repository checks and relevant design validation pass | Pass/Fail |
| Review freshness | Any required final review references the candidate commit | Pass/Fail/N/A |
| Feedback | Remaining findings are explicitly clarified, deferred, or rejected | Pass/Fail |

Declare the design ready when every required gate passes. Stop reviewing based on
these implementation and safety criteria, not because reviewers produced zero
comments. Require any additional formal review round to name a specific blocking
invariant, show evidence that the frozen candidate violates it, and explain why
the next slice cannot safely proceed.

End each use of this skill with:

1. The candidate revision and readiness decision.
2. Any blocking invariant or owner gate.
3. The next bounded implementation slice.
4. Deferred findings that must not silently re-enter MVP scope.
