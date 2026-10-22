---
id: stemma:phys.inelastic-collision
type: process
name: inelastic collision
domain: physics
subdomain: mechanics
level: foundational
status: canonical
definition: An inelastic collision describes an event where objects collide and kinetic energy is not
  conserved. Some mechanical energy transforms into other forms like thermal energy or deformation, causing
  the final speed to be lower.
same_dimensional_quantities: null
source_refs:
- stemma:src.openstax-physics
provenance:
  ai_drafted: true
  source_kind: textbook
  source: 'Physics (2020), OpenStax. Term locator: https://openstax.org/books/physics/pages/8-key-terms.
    Used as a reference; definition independently phrased.'
  writer: process:openstax-importer.v1
  drafted_by: llm:qwen3.5-9b
  original_author: Paul Peter Urone, Roger Hinrichs, Fatih Gozuacik, Denise Pattison, Catherine Tabor
  link: https://openstax.org/books/physics/pages/8-key-terms
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
  wd: Q2074917
examples:
- "Two cars crumpling in a crash lose kinetic energy to deformation."
- "Clay sticking to a wall is a perfectly inelastic collision."
formal:
  statement: An inelastic collision conserves total linear momentum while converting
    part of the kinetic energy into internal energy.
  equation: p_i = p_f and K_f < K_i
  variables:
  - symbol: p
    meaning: total momentum
    unit: kg m s^-1
  - symbol: K
    meaning: total kinetic energy
    unit: J
  conditions:
  - isolated system
  - some kinetic energy becomes heat, sound, or deformation
  dimensions: null
applications:
- "Analyzing car crash dynamics for safety barrier design."
- "Studying meteorite impacts causing atmospheric heating events."
---

An inelastic collision describes an event where objects collide and kinetic energy is not conserved. Some mechanical energy transforms into other forms like thermal energy or deformation, causing the final speed to be lower.
