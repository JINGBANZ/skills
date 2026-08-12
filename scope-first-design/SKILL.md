---
name: scope-first-design
description: Scope-first workflow for turning ambiguous project ideas into bounded, risk-proportional architecture and low-level designs, implementation slices, fresh-agent handoffs, and scoped design PRs. Use when starting or revising a design, architecture, or low-level spec; narrowing an ambiguous project; planning an MVP or bounded phase; selecting components, languages, or reuse; defining the next implementation slice; or preparing a design handoff or PR.
---

# Scope-First Design

Turn an ambiguous request into the smallest coherent design that supports a
bounded implementation slice. Treat implementation-ready as: a fresh agent can
complete that slice autonomously until it reaches an explicit owner gate. Do not
pre-specify the whole future product.

Do not expand an already bounded, reversible change into a design exercise when
it does not alter architecture, sensitive effects, accepted risk, owner policy,
or cross-component contracts. Inherit the repository's scope contract and
proceed with the smallest verified implementation.

Produce four logical outputs:

1. Scope contract.
2. Canonical design with only risk-relevant decisions and invariants.
3. Implementation plan and next-slice handoff.
4. Scoped design PR description.

Treat these as logical sections, not mandatory separate files. Put durable facts
in the repository's existing canonical documents. Make the PR description a
short summary that links to those facts.

## 1. Inspect and clarify

Read repository guidance, architecture pages, ADRs, specifications, relevant
code, and current status before asking questions. Extract existing answers and
cite their canonical locations. Separate the result into:

- **Known facts:** directly supported by repository or owner evidence.
- **Safe assumptions:** reversible defaults that do not change scope or safety.
- **Material unknowns:** answers that change scope, safety, architecture, or the
  next implementation slice.

Ask only about material unknowns that cannot be discovered. Ask one to three
concise questions per round, ordered by impact. Offer a recommended default and
its consequence when safe. Continue with explicitly recorded assumptions for
non-blocking unknowns; do not stop merely to eliminate all uncertainty.

Use this discovery bank selectively. Do not ask every question every time.

| Area | Ask only when the answer is missing and material |
| --- | --- |
| Outcome and people | What outcome matters, and who is the target user or operator? |
| Phase boundary | Where does this phase end, and what exact slice should implementation complete next? |
| Capabilities | What must work in this phase, what belongs to later slices, and what is outside the phase? |
| Operating assumptions | Where will it run, at what scale, under which trust and access model? |
| Sensitive effects | What data, credentials, money, external writes, or compliance duties are involved? |
| Failure tolerance | What downtime, data loss, partial failure, and recovery behavior are acceptable? |
| Authority | Who may propose, approve, execute, override, and audit each sensitive action? |
| Constraints and reuse | Which technology, compatibility, reuse, budget, or operating constraints are fixed? |
| Owner-only values | Which business thresholds, policies, credentials, or commitments must the agent not invent? |
| Acceptance | Which measurable outcomes prove the phase and next slice are complete? |

## 2. Select risk-proportional rigor

Choose the highest applicable rigor level early. Scale design depth to the cost
of being wrong, not to the amount of detail that could be written.

| Level | Typical shape | Required design depth |
| --- | --- | --- |
| Simple and reversible | Local transformation, static page, isolated utility | Outcome, non-goals, acceptance, and implementation plan |
| Stateful or integrated | Persistent data, multiple components, third-party dependency | Add interfaces, data ownership, lifecycle, and failure behavior |
| High-stakes or externally effective | Credentials, money, privileged actions, external writes, regulated or safety-sensitive data | Add authority, explicit invariants, transaction boundaries, reconciliation, and recovery |

Apply only the matrices and invariants relevant to the selected level. Never
impose transaction or authority artifacts on a simple project. Raise rigor when
one sensitive boundary demands it without burdening unrelated components.

## 3. Freeze the scope contract

Agree on this priority order before expanding low-level detail:

1. Keep the bounded phase internally consistent and safe.
2. Specify enough for the next implementation slice.
3. Apply broader practices only when the scope and risk level require them.

Create or update the **scope contract**:

| Field | Required decision |
| --- | --- |
| Objective and actors | User-visible outcome and target user/operator |
| Required capabilities | Behaviors that must exist in this phase |
| Explicit non-goals | Work explicitly outside the current phase |
| Operating assumptions | Deployment, scale, trust, access, and data sensitivity |
| Known facts | Decisions and constraints with canonical evidence |
| Safe assumptions | Reversible defaults, consequences, and validation points |
| Accepted risks | Known failure, recovery, security, or operational limitations |
| Owner gates | Material decisions or values the agent must not invent |
| Next slice | Concrete start and end boundary for implementation |
| Acceptance | Measurable completion criteria for the phase and next slice |

A capability assigned to a later slice remains part of the current phase
contract. Mark it **not in this slice**. Reserve **non-goal** for work outside the
current phase.

Do not invent an owner-only business value. Ask when it blocks safe design;
otherwise record a named owner gate so implementation can progress up to that
point. Freeze the contract before detailed design. Route later scope changes
through an explicit owner decision.

Never add out-of-phase infrastructure merely because it is a generic industry
best practice. First name the in-scope requirement or risk that demands it.
Prefer removing an unnecessary feature over fully designing it.

Review feedback is evidence, not a new specification. Correct confirmed
violations of the frozen scope contract or applicable safety, security, and
privacy constraints. Treat feedback that changes required behavior, accepted
risk, phase non-goals, or materially introduces lifecycle states, retry/timer
semantics, or cross-component coordination as a scope proposal requiring owner
approval.

## 4. Construct the smallest viable design

Extract hard constraints from the scope contract. Evaluate only viable options
and meaningful tradeoffs. If one option is clearly sufficient, choose it and
state why; do not manufacture alternatives for ceremony.

Choose components, languages, and tools according to criticality and leverage:

- Put correctness-, safety-, latency-, or resource-critical behavior where its
  guarantees are easiest to enforce.
- Use higher-leverage tools for non-critical work when they reduce delivery and
  maintenance cost.
- Prefer compatible repository capabilities and mature open-source components
  before custom implementation; check functional fit, operational burden,
  maintenance health, and licensing.
- Keep one foundation path. Mention alternatives only when their tradeoff affects
  the current decision or a named future trigger.

When multiple components or runtimes are material, capture:

| Component | Responsibility | Criticality | Language/tool or reuse | Rationale and tradeoff |
| --- | --- | --- | --- | --- |

Define boundaries before internal mechanics. Apply only the sections selected by
the rigor level:

- **Interfaces:** inputs, outputs, validation, compatibility, and error contract.
- **Data ownership:** canonical writer, schema/format, retention, and sensitivity.
- **Lifecycle:** states, transitions, restart behavior, and resource ownership.
- **Failure:** safe outcome, retry behavior, recovery trigger, and visible
  evidence.
- **Authority:** proposer, approver, executor, mutator, and required proof for
  sensitive actions.
- **Transactions:** durable intent, commit boundary, unknown-commit behavior,
  idempotency, and reconciliation for external effects.

For high-stakes guarantees, state concise invariants with stable IDs, canonical
locations, and verification evidence. Do not create an invariant checklist for
ordinary details.

Keep each fact in one canonical place and link to it elsewhere. Do not specify
internal contracts for phase non-goals. Specify a later-slice component only as
far as its current interface or dependency requires.

## 5. Slice the work and prepare the handoff

Decompose the design into ordered vertical slices that produce verifiable value.
Minimize cross-slice scaffolding. Keep later-slice capabilities in the phase
contract while excluding them from the immediate handoff.

Create the **implementation plan and next-slice handoff**:

| Slice | Outcome | Inputs | Outputs | Dependencies | Verification | Owner gate |
| --- | --- | --- | --- | --- | --- | --- |

For the immediate slice, state:

- Goal, capabilities in this slice, phase capabilities marked **not in this
  slice**, and phase non-goals.
- Files, components, and canonical design sections in scope.
- Preconditions, inputs, outputs, and dependencies.
- Risk-relevant decisions and invariants that must remain true.
- Ordered implementation steps where order matters.
- Tests, repository checks, and observable acceptance criteria.
- Exact conditions that require owner input or stop the slice.

Check that a fresh agent can locate the cited context and finish the slice
without choosing product policy or silently widening scope.

## 6. Validate the design

Validate in proportion to the selected rigor level:

- Map every required capability to a design decision, implementation slice, and
  acceptance criterion.
- Confirm that phase non-goals did not enter components, contracts, or planned
  work.
- Confirm that every material assumption is recorded or converted to an owner
  gate.
- Check only relevant interfaces, data paths, lifecycles, failure paths,
  authorities, transactions, and recovery paths for completeness.
- Verify canonical links, diagrams, terminology, and repository-required checks.
- Re-read the handoff from a fresh agent's perspective.

Fix inconsistencies in their canonical locations. Do not add ceremony or future
infrastructure merely to make the document look comprehensive.

## 7. Publish the scoped design PR

When publication is authorized or required by repository guidance, commit the
canonical design changes and open or update one scoped design PR. Use this body:

```markdown
## Objective

## Frozen scope / In scope

## Explicit non-goals

## Operating assumptions and accepted risks

## Key design decisions and reuse

## Owner gates / unresolved owner decisions

## Next implementation slice

## Acceptance and validation
```

Summarize and link to canonical design sections instead of duplicating the full
specification. Keep phase non-goals out of executable scope and mark later-slice
capabilities **not in this slice**. If scope changes, update the canonical scope
contract and PR summary first, then change low-level details.

End with:

1. Canonical design location or locations.
2. Frozen scope summary.
3. Material assumptions and owner gates.
4. Next bounded implementation slice.
5. PR URL and status, when published.
