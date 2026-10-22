---
id: stemma:phys.velocity
type: concept
name: velocity
domain: physics
subdomain: mechanics
level: foundational
status: canonical
definition: Velocity is defined as the speed and direction of an object's motion. This vector quantity
  distinguishes itself from scalar speed by explicitly incorporating directional information to describe
  how position changes over time.
same_dimensional_quantities: null
source_refs:
- stemma:src.openstax-physics
provenance:
  ai_drafted: true
  source_kind: textbook
  source: 'Physics (2020), OpenStax. Term locator: https://openstax.org/books/physics/pages/2-key-terms.
    Used as a reference; definition independently phrased.'
  writer: process:openstax-importer.v1
  drafted_by: llm:qwen3.5-9b
  original_author: Paul Peter Urone, Roger Hinrichs, Fatih Gozuacik, Denise Pattison, Catherine Tabor
  link: https://openstax.org/books/physics/pages/2-key-terms
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
  wd: Q11465
examples:
- "A car that travels 120 km east in 2 h has average velocity 60 km/h east."
- "A satellite in a circular orbit has a velocity tangent to its path even though its\
  \ speed is constant."
formal:
  statement: Velocity is the time derivative of position; average velocity is displacement
    divided by elapsed time.
  equation: v = dx/dt
  variables:
  - symbol: v
    meaning: velocity
    unit: m s^-1
  - symbol: x
    meaning: position
    unit: m
  - symbol: t
    meaning: time
    unit: s
  conditions:
  - classical mechanics
  - position measured in a chosen reference frame
  dimensions: L T^-1
applications:
- "Navigating aircraft through wind currents for accurate flight paths."
- "Programming autonomous vehicles to maintain lane and speed limits."
- "Tracking migratory bird patterns relative to Earth's rotation."

limitations:
- "Requires consistent coordinate system definitions across observers."
- "Instantaneous values can be noisy without high-frequency sampling."
- "Does not describe acceleration unless time derivative is taken."
---

Velocity is defined as the speed and direction of an object's motion. This vector quantity distinguishes itself from scalar speed by explicitly incorporating directional information to describe how position changes over time.
