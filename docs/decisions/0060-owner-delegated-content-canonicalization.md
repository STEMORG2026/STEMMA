# ADR-0060: Owner-Delegated Machine Canonicalization

Status: Decided — 2026-10-20
Date: 2026-10-20
Decided by: Sajan (sole owner), direct instruction to build bachelor-level content and
canonicalize it without waiting for per-item owner review.
Relates to: ADR-0043 (dual verification), ADR-0057 (multi-stage promotion), ADR-0049
(delegated authority), ADR-0061 (schema 1.4), ADR-0062 (open content acquisition),
ENF-STEMMA-HITL-001..005

## Context

The repository's default canonicalization path is intentionally human-only: a canonical entity
needs a registered human writer, a registered human reviewer, and an ordered promotion chain
(ADR-0057). On 2026-10-20 the owner directed the agent to build content up to bachelor level
across physics, chemistry, biology, astronomy, mathematics, and civil/electrical/chemical/
mechanical/computer engineering, to verify it, and to make it canonical without waiting for
per-item owner review.

That instruction cannot be satisfied by silently weakening the human rule. It also cannot be
satisfied by fabricating human reviewer identities. Both would destroy the audit trail the
human rule exists to protect. The owner's authority is real, so the correct move is to record a
**separate, explicit, bounded authority path**: the owner delegates canonicalization to
deterministic machine gates for a named scope.

## Decision

### 1. Add `review_mode: owner_delegated`

An entity may set `provenance.review_mode: owner_delegated`. This is not the default and does
not apply to human-reviewed records. When set, the entity must also carry:

- `provenance.delegation.delegated_by` — a registered, active `human:` SOLE_OWNER;
- `provenance.delegation.delegation_ref` — this ADR or a later owner decision;
- `provenance.delegation.scope` — the domains/source family/tranche covered;
- `provenance.delegation.sanctioned_at` and `retire_when`;
- `provenance.reviewer` — a registered `process:` or `llm:` verifier (never a fake human);
- `provenance.reviewed_at`;
- `provenance.verification.checks` — at least two **passing** checks by registered machine
  agents, with named evidence.

### 2. Canonical is legal on this path only through the delegation gate

`scripts/validate.py` accepts `status: canonical` with `review_mode: owner_delegated` only when
`check_delegation_block()` passes. The human promotion chain is not fabricated or back-filled.
The delegated path may claim only `canonical` among reviewed statuses; intermediate human
statuses remain reserved for human review.

### 3. The human path remains the default

Absent `review_mode`, every existing rule applies unchanged. ADR-0057's human chain,
independence waiver, and same-day separation remain in force for human canonicalization.

### 4. Delegation is scoped and revocable

`scope` names what the delegation covers. `retire_when` names the condition that ends it
(for example, when a domain reviewer is registered or when a source tranche is exhausted).
Delegation is not a blanket waiver of source verification, schema validation, licensing, or
duplicate checks.

### 5. Honest provenance

`provenance.writer` and `provenance.reviewer` on delegated records identify the actual machine
agents (`process:...` / `llm:...`). The delegation block identifies the human who authorized
the path. No field claims that a human read the artifact.

## Consequences

**Easier.** The owner can authorize a content campaign at the scale the mandate requires while
keeping the audit trail truthful. Consumers can distinguish human-reviewed from
owner-delegated canonical content with one field.

**Harder.** Delegated content carries a higher verification burden: two named machine checks,
source resolution, license checks, duplicate detection, and a recorded scope. A failure in any
of those keeps the record non-canonical.

**Risk.** Machine verification can be wrong at scale. Mitigations: conservative source policy
(ADR-0062), independent second-pass checks, explicit limitations, sampled human audit, and the
ability to retire the delegation and demote records. Delegated canonical status is not a claim
of infallibility; it is a claim that the recorded gates passed.

## Verification

- `scripts/validate.py:check_delegation_block` rejects missing/weak delegation.
- `tests/governance/test_delegated_canonicalization.py` covers positive, negative, and
  no-fabricated-human cases.
- `ENF-STEMMA-HITL-005` records the rule in the machine-readable enforcement registry.
