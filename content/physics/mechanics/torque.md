---
id: stemma:phys.torque
type: concept
name: torque
domain: physics
subdomain: mechanics
level: intermediate
status: canonical
definition: Torque results from taking the cross product of force and lever arm distance. This vector
  quantity determines the rotational effect produced on an object around a specific axis.
same_dimensional_quantities: null
source_refs:
- stemma:src.openstax-university-physics-volume-1
provenance:
  ai_drafted: true
  source_kind: textbook
  source: 'University Physics Volume 1 (2016), OpenStax. Term locator: https://openstax.org/books/university-physics-volume-1/pages/10-key-terms.
    Used as a reference; definition independently phrased.'
  writer: process:openstax-importer.v1
  drafted_by: llm:qwen3.5-9b
  original_author: Stephen D. Druger, William Moebs, Samuel J. Ling, Jeff Sanny, David Anderson, Daniel
    Bowman, Gerald Friedman, Edw. S. Ginsberg, Kenneth Podolak, Takashi Sato, David Smith, Joseph Trout,
    Kevin Wheelock, Dedra Demaree, Richard Ludlow, Patrick Motl, Lev Gasparov, Lee LaRue, Mark Lattery,
    Tao Pang, Alice Kolakowska
  link: https://openstax.org/books/university-physics-volume-1/pages/10-key-terms
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
  wd: Q48103
examples:
- "Pushing a door far from its hinges produces more torque than pushing near the hinges."
- "A wrench multiplies torque when force is applied at a larger lever arm."
formal:
  statement: Torque is the cross product of the position vector from the pivot to the
    point of force application and the force vector.
  equation: tau = r x F
  variables:
  - symbol: tau
    meaning: torque
    unit: N m
  - symbol: r
    meaning: position vector from pivot
    unit: m
  - symbol: F
    meaning: force
    unit: N
  conditions:
  - rigid body
  - fixed pivot or axis
  dimensions: M L^2 T^-2
applications:
- "Sizing engine crankshafts to handle maximum load stresses."
- "Designing bolt tightening procedures for structural assembly safety."
- "Optimizing wrench lengths for loosening rusted fasteners effectively."

limitations:
- "Calculation assumes rigid bodies without deformation under load."
- "Depends critically on precise definition of rotation axis location."
- "Ignores frictional losses at pivot points in real mechanisms."
---

Torque results from taking the cross product of force and lever arm distance. This vector quantity determines the rotational effect produced on an object around a specific axis.
