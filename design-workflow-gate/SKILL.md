---
name: design-workflow-gate
description: End-to-end, scope-first workflow for discovering, designing, slicing, reviewing, and gating architecture or low-level specifications without expanding a bounded phase. Use when starting a design, architecture, or low-level spec; narrowing an ambiguous project; planning an MVP or bounded phase; creating implementation slices or an agent handoff; reviewing a design; deciding merge readiness; or escaping repeated review churn.
---

# Design Workflow Gate

Turn an ambiguous request into a bounded, coherent design and an executable next
slice. Treat implementation-ready as: an agent can complete the next bounded
slice autonomously until it reaches an explicit owner gate. Do not interpret it
as every future product decision being settled.

Maintain five lightweight artifacts in the repository's existing design system:

1. Scope contract.
2. Invariant checklist.
3. Implementation plan and next-slice handoff.
4. Feedback ledger.
5. Merge gate.

Keep them together or link them from canonical design pages. Do not impose new
files when a table or section fits an existing page.

## 1. Discover before asking

Read repository guidance, architecture pages, ADRs, specifications, relevant
code, and current status before asking questions. Extract existing answers and
cite their canonical locations. Separate the result into:

- **Known facts:** directly supported by repository or owner evidence.
- **Safe assumptions:** reversible defaults that do not change scope or safety.
- **Material unknowns:** answers that change scope, safety, architecture, or the
  next implementation slice.

Ask only about material unknowns that cannot be discovered. Ask one to three
concise questions per round, ordered by blocking impact. Offer a recommended
default and its consequence when safe. Continue with explicitly recorded
assumptions for non-blocking unknowns; do not stop merely to eliminate all
uncertainty.

Use this discovery bank selectively. Do not ask every question every time.

| Area | Ask only when the answer is missing and material |
| --- | --- |
| Outcome and people | What outcome matters, and who is the target user or operator? |
| Phase boundary | Where does this phase end, and what exact slice should implementation complete next? |
| Capabilities | What must work now, and what are the explicit non-goals? |
| Operating assumptions | Where will it run, at what scale, under which trust and access model? |
| Sensitive effects | What data, credentials, money, external writes, or compliance duties are involved? |
| Failure tolerance | What downtime, data loss, partial failure, and recovery behavior are acceptable? |
| Authority | Who may propose, approve, execute, override, and audit each sensitive action? |
| Constraints and reuse | Which technology, compatibility, reuse, budget, or operating constraints are fixed? |
| Owner-only values | Which business thresholds, policies, credentials, or commitments must the agent not invent? |
| Acceptance | Which measurable outcomes prove the phase and next slice are complete? |

## 2. Freeze the scope contract

Agree on this priority order before expanding low-level detail:

1. Keep the frozen phase internally consistent and safe.
2. Specify enough for the next implementation slice.
3. Apply broader best practices only when that scope requires them.

Create or update the **scope contract** with discovery answers:

| Field | Required decision |
| --- | --- |
| Objective and actors | User-visible outcome and target user/operator |
| Next slice | Concrete start, end, and measurable acceptance boundary |
| Known facts | Decisions and constraints with canonical evidence |
| Assumptions | Reversible defaults, consequences, and validation points |
| Required capabilities | Behaviors that must exist in this phase |
| Explicit non-goals | Plausible features intentionally excluded |
| Operating model | Deployment, scale, trust, access, and data sensitivity |
| Accepted risks | Known failure, recovery, security, or operational limitations |
| Owner gates | Values or decisions where implementation must stop and request input |
| Priority order | Tie-breaker when safety, scope, and completeness compete |

Do not invent a material owner decision. Ask for it when it blocks safe design;
otherwise record a named owner gate so implementation can progress up to that
point. Freeze the contract before detailed design. Route later scope changes
through an explicit owner decision.

Never add deferred infrastructure merely because it is a generic industry best
practice. First name the in-scope requirement or invariant that demands it.
Prefer removing an unnecessary feature over fully designing it.

## 3. Construct the smallest viable design

Extract hard constraints from the scope contract. Evaluate only viable options
and their meaningful tradeoffs. If one option is clearly sufficient, choose it
and state why; do not manufacture alternatives for ceremony.

Choose components, languages, and tools according to criticality and leverage:

- Put safety-, correctness-, latency-, or resource-critical behavior where the
  required guarantees are easiest to enforce.
- Use higher-leverage tools for non-critical work when they reduce delivery and
  maintenance cost.
- Prefer compatible repository capabilities and mature open-source components
  before custom implementation; check fit, operational burden, and licensing.
- Keep one foundation path. Record alternatives as deferred instead of designing
  several systems at once.

Capture important choices in a compact component table:

| Component | Responsibility | Criticality | Language/tool or reuse | Rationale and tradeoff |
| --- | --- | --- | --- | --- |

Define component boundaries and contracts before internal mechanics. Specify the
applicable interaction surfaces:

- **Authority:** creator, authorizer, executor, reader, mutator, and required
  proof for every sensitive resource or command.
- **Data:** canonical owner, schema/format boundary, validation, retention, and
  sensitivity.
- **State:** every state, entry and exit event, recovery path, and resource or
  reservation effect.
- **Transaction:** durable intent, commit boundary, unknown-commit behavior,
  idempotency/retry rule, and reconciliation evidence for each external effect.
- **Failure:** failure mode, safe outcome, recovery trigger, and
  operator-visible evidence at each boundary.

Keep each fact in one canonical place and link to it elsewhere. Do not specify
internal contracts for deferred components.

Turn load-bearing guarantees into an **invariant checklist**:

| ID | Invariant | Canonical location | Verification | Status |
| --- | --- | --- | --- | --- |
| INV-001 | One precise safety or correctness guarantee | Link/section | Test, trace, or review evidence | Open/Met |

Keep stable IDs. Preserve the checklist across rewrites and compression passes;
never remove or weaken a resolved invariant silently. Change an invariant only
with its scope decision and replacement guarantee.

## 4. Slice the work and prepare the handoff

Decompose the design into ordered vertical slices that produce verifiable value.
Minimize cross-slice scaffolding and postpone deferred capabilities.

Create the **implementation plan and next-slice handoff**:

| Slice | Outcome | Inputs | Outputs | Dependencies | Verification | Owner gate |
| --- | --- | --- | --- | --- | --- | --- |

For the immediate slice, state:

- Goal and explicit non-goals.
- Files, components, and canonical contracts in scope.
- Preconditions, inputs, outputs, and dependencies.
- Invariants that must remain true.
- Ordered implementation steps where order matters.
- Tests, repository gates, and observable acceptance criteria.
- Exact conditions that require owner input or stop the slice.

Check that a fresh agent can start from the handoff, discover the cited context,
and finish the slice without choosing product policy or silently widening scope.

## 5. Review the frozen candidate

Review only after the design and handoff are coherent. Run focused passes
independently, and in parallel when agent capacity permits:

1. Scope, assumptions, non-goals, and accepted risks.
2. Component choices, reuse, and boundary clarity.
3. Authority, trust, data, and security boundaries.
4. State machines and lifecycle completeness.
5. Transactions, idempotency, failure, and recovery.
6. Slice ordering, implementability, verification, and owner gates.

Give every reviewer this brief:

> Review only the frozen scope and next implementation slice. For each finding,
> name the violated requirement or invariant and explain whether it blocks that
> slice. Do not recommend deferred infrastructure unless an in-scope guarantee
> requires it.

Collect findings before editing. Maintain the **feedback ledger**:

| ID | Finding | Class | Invariant or requirement | Decision | Disposition | Status |
| --- | --- | --- | --- | --- | --- | --- |
| REV-001 | Concise issue | Blocker/Clarify/Defer/Out of scope | ID or scope field | Accept/Reject | Canonical edit or deferred location | Open/Closed |

Classify findings consistently:

- **Blocker:** prevents the next slice, violates an in-scope safety invariant, or
  makes a required outcome unreachable.
- **Clarify:** removes implementation ambiguity without expanding scope.
- **Defer:** captures a valid future requirement outside the current slice.
- **Out of scope:** has no current requirement or invariant; record the rejection
  reason without designing it.

Do not equate a comment with an obligation to edit. Do not use unresolved comment
count as a quality metric.

## 6. Batch corrections and protect settled decisions

Group accepted findings by root cause. Make one coherent correction pass across
canonical sources, diagrams, tests, and the handoff instead of pushing once per
comment. Update links and derived summaries after canonical rules change.

Before accepting the pass:

- Re-run every previously met invariant against the diff.
- Check that simplification did not erase authority, locking, ordering, retry,
  recovery, or fail-closed guarantees.
- Remove newly unnecessary detail rather than completing it speculatively.
- Keep deferred work in the ledger or backlog, not in current-phase contracts.

Freeze a candidate after the batch. Triage new feedback against the same ledger
before changing it; do not reopen the whole design automatically.

## 7. Apply the merge gate

Create or update the **merge gate** for the frozen candidate:

| Gate | Evidence | Result |
| --- | --- | --- |
| Candidate identity | Exact commit or immutable revision | Pass/Fail |
| Scope | Contract frozen; non-goals and accepted risks explicit | Pass/Fail |
| Design | Smallest viable choices and boundaries satisfy the frozen scope | Pass/Fail |
| Implementability | Next slice can proceed until a named owner gate | Pass/Fail |
| Invariants | No unresolved in-scope safety or correctness blocker | Pass/Fail |
| Interactions | Authority, data, state, transaction, and failure paths complete for the slice | Pass/Fail |
| Consistency | One canonical source per fact; links and diagrams agree | Pass/Fail |
| Validation | Repository checks and relevant design validation pass | Pass/Fail |
| Review freshness | Any required final review references the candidate commit | Pass/Fail/N/A |
| Feedback | Remaining findings are explicitly clarified, deferred, or rejected | Pass/Fail |

Declare the design ready when every required gate passes. Stop reviewing based on
implementation and safety criteria, not because reviewers produced zero comments.
Require any additional formal review round to name a specific blocking invariant,
show evidence that the frozen candidate violates it, and explain why the next
slice cannot safely proceed.

End each use of this skill with:

1. The candidate revision and readiness decision.
2. Any blocking invariant or owner gate.
3. The next bounded implementation slice and handoff location.
4. Deferred findings that must not silently re-enter current scope.
