---
id: stemma:phys.center-of-mass
type: concept
name: center of mass
domain: physics
subdomain: mechanics
level: foundational
status: canonical
definition: The center of mass is defined as the weighted average position of all mass in a system. It
  acts as the single point where external forces effectively influence the translational motion of the
  entire object.
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
  wd: Q2945123
examples:
- "A uniform rod balances at its midpoint."
- "A binary star system orbits about a point between the two stars."
formal:
  statement: The center of mass is the mass-weighted average position of all parts of
    a system.
  equation: r_cm = (sum m_i r_i) / (sum m_i)
  variables:
  - symbol: r_cm
    meaning: center-of-mass position
    unit: m
  - symbol: m_i
    meaning: mass of particle i
    unit: kg
  - symbol: r_i
    meaning: position of particle i
    unit: m
  conditions:
  - any mass distribution
  - external forces act as if applied at this point
  dimensions: L
applications:
- "Balancing vehicle chassis for stable handling dynamics."
- "Designing spacecraft attitude control systems around gravity centers."
---

The center of mass is defined as the weighted average position of all mass in a system. It acts as the single point where external forces effectively influence the translational motion of the entire object.
