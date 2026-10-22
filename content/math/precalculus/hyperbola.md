---
id: stemma:math.hyperbola
type: structure
name: hyperbola
domain: mathematics
subdomain: precalculus
level: foundational
status: canonical
definition: A hyperbola consists of all points in a plane where the absolute difference between distances
  to two fixed foci equals a positive constant. This curve forms two separate branches that open away
  from each other symmetrically.
same_dimensional_quantities: null
source_refs:
- stemma:src.openstax-precalculus-2e
provenance:
  ai_drafted: true
  source_kind: textbook
  source: 'Precalculus 2e (2021), OpenStax. Term locator: https://openstax.org/books/precalculus-2e/pages/10-key-terms.
    Used as a reference; definition independently phrased.'
  writer: process:openstax-importer.v1
  drafted_by: llm:qwen3.5-9b
  original_author: Jay Abramson, Valeree Falduto, Rachael Gross, David Lippman, Melonie Rasmussen, Rick
    Norwood, Nicholas Belloit, Harold Whipple, Jean-Marie Magnier, Christina Fernandez
  link: https://openstax.org/books/precalculus-2e/pages/10-key-terms
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
rights:
  license: CC-BY-4.0
  attribution: Original STEMMA definition generated from the cited reference; no source prose copied.
examples:
- "A hyperbola models the path of a comet on an unbound trajectory."
- "Two-branch curves describe some scattering trajectories."
formal:
  statement: A hyperbola is the locus of points whose absolute distance difference to
    two fixed foci is constant.
  equation: x^2 / a^2 - y^2 / b^2 = 1
  variables:
  - symbol: a
    meaning: distance from center to vertex
  - symbol: b
    meaning: conjugate-axis scale
  conditions:
  - a > 0, b > 0
  - axes aligned with the coordinate axes
  dimensions: null
applications:
- "Modeling gravitational slingshot trajectories in orbital mechanics."
- "Designing cooling towers based on structural stability needs."
---

A hyperbola consists of all points in a plane where the absolute difference between distances to two fixed foci equals a positive constant. This curve forms two separate branches that open away from each other symmetrically.
