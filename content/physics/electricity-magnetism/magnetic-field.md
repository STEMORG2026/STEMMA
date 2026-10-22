---
id: stemma:phys.magnetic-field
type: concept
name: magnetic field
domain: physics
subdomain: electricity-magnetism
level: intermediate
status: canonical
definition: A magnetic field consists of directional lines indicating force magnitude and direction near
  magnets. It exerts forces on moving charges, defining the region where magnetic interactions occur.
same_dimensional_quantities: null
source_refs:
- stemma:src.openstax-physics
provenance:
  ai_drafted: true
  source_kind: textbook
  source: 'Physics (2020), OpenStax. Term locator: https://openstax.org/books/physics/pages/15-key-terms.
    Used as a reference; definition independently phrased.'
  writer: process:openstax-importer.v1
  drafted_by: llm:qwen3.5-9b
  original_author: Paul Peter Urone, Roger Hinrichs, Fatih Gozuacik, Denise Pattison, Catherine Tabor
  link: https://openstax.org/books/physics/pages/15-key-terms
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
- stemma:phys.coulombs-law
- stemma:phys.faraday-law
rights:
  license: CC-BY-4.0
  attribution: Original STEMMA definition generated from the cited reference; no source prose copied.
external_ids:
  wd: Q11408
examples:
- "A compass needle aligns with Earth's magnetic field."
- "A charged particle moving perpendicular to a magnetic field follows a circular path."
formal:
  statement: The magnetic force on a moving charge is the charge times the cross product
    of velocity and magnetic field.
  equation: F = q (v x B)
  variables:
  - symbol: F
    meaning: magnetic force
    unit: N
  - symbol: q
    meaning: charge
    unit: C
  - symbol: v
    meaning: velocity
    unit: m s^-1
  - symbol: B
    meaning: magnetic field
    unit: T
  conditions:
  - point charge
  - classical electromagnetism
  dimensions: M L T^-2
applications:
- "MRI machine imaging systems in hospitals."
- "Electric motor torque generation mechanisms."
---

A magnetic field consists of directional lines indicating force magnitude and direction near magnets. It exerts forces on moving charges, defining the region where magnetic interactions occur.
