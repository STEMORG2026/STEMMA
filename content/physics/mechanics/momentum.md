---
id: stemma:phys.momentum
type: concept
name: momentum
domain: physics
subdomain: mechanics
level: foundational
status: canonical
definition: Momentum represents the measure of an object's quantity of motion. It is calculated as the
  product of mass and velocity, serving as a vector quantity that accounts for both how fast an object
  moves and its inertia.
same_dimensional_quantities: null
source_refs:
- stemma:src.openstax-university-physics-volume-1
provenance:
  ai_drafted: true
  source_kind: textbook
  source: 'University Physics Volume 1 (2016), OpenStax. Term locator: https://openstax.org/books/university-physics-volume-1/pages/9-key-terms.
    Used as a reference; definition independently phrased.'
  writer: process:openstax-importer.v1
  drafted_by: llm:qwen3.5-9b
  original_author: Stephen D. Druger, William Moebs, Samuel J. Ling, Jeff Sanny, David Anderson, Daniel
    Bowman, Gerald Friedman, Edw. S. Ginsberg, Kenneth Podolak, Takashi Sato, David Smith, Joseph Trout,
    Kevin Wheelock, Dedra Demaree, Richard Ludlow, Patrick Motl, Lev Gasparov, Lee LaRue, Mark Lattery,
    Tao Pang, Alice Kolakowska
  link: https://openstax.org/books/university-physics-volume-1/pages/9-key-terms
  retrieved_at: '2026-10-20'
  review_mode: owner_delegated
  reviewer: process:content-validator.v1
  reviewed_at: '2026-10-20T00:00:00+00:00'
  verification:
    method: schema + source-resolution + no-verbatim + definition-quality
    verifier: process:content-verifier.v1
    verified_at: '2026-10-20'
    notes: Deterministic checks over the cited OpenStax inventory row; no human review claimed.
    checks:
    - name: schema
      status: pass
      evidence: process:content-validator.v1
    - name: source-resolution
      status: pass
      evidence: process:content-validator.v1
    - name: no-verbatim
      status: pass
      evidence: process:content-verifier.v1
    - name: definition-quality
      status: pass
      evidence: process:content-verifier.v1
  delegation:
    delegated_by: human:curator.001
    delegation_ref: docs/decisions/0060-owner-delegated-content-canonicalization.md
    scope: OpenStax-derived bachelor STEM content tranche, 2026-10-20 inventory
    sanctioned_at: '2026-10-20'
    retire_when: a domain human reviewer is registered and accepts the tranche
    limitations:
    - reference grade is Tier C (NC-SA) or Tier B; no source prose reused
    - machine checks cover schema, provenance, source resolution, and copying only
    - not a substitute for domain-expert review of scientific correctness
governed_by:
- stemma:phys.newtons-second-law
- stemma:phys.conservation-energy
rights:
  license: CC-BY-4.0
  attribution: Original STEMMA definition generated from the cited reference; no source prose copied.
external_ids:
  wd: Q41273
examples:
- "A 1,000 kg car moving at 20 m/s has momentum 20,000 kg m/s in its direction of travel."
- "A bowling ball and a tennis ball can share momentum if their masses and speeds compensate."
formal:
  statement: Linear momentum is the product of an object's mass and its velocity.
  equation: p = m v
  variables:
  - symbol: p
    meaning: linear momentum
    unit: kg m s^-1
  - symbol: m
    meaning: mass
    unit: kg
  - symbol: v
    meaning: velocity
    unit: m s^-1
  conditions:
  - non-relativistic speed
  - constant mass
  dimensions: M L T^-1
applications:
- "Engineering airbag deployment timing for passenger safety."
- "Analyzing billiard ball collisions in sports physics simulations."
- "Designing rocket propulsion systems relying on exhaust recoil forces."

limitations:
- "Conservation strictly applies only to isolated, frictionless systems."
- "Classical formula fails at relativistic speeds approaching light speed."
- "Does not account for energy dissipation during inelastic impacts."
---

Momentum represents the measure of an object's quantity of motion. It is calculated as the product of mass and velocity, serving as a vector quantity that accounts for both how fast an object moves and its inertia.
