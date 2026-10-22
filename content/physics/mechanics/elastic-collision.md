---
id: stemma:phys.elastic-collision
type: process
name: elastic collision
domain: physics
subdomain: mechanics
level: foundational
status: canonical
definition: An elastic collision occurs when objects separate after impact while conserving their total
  kinetic energy. This idealized process ensures that no mechanical energy is transformed into heat or
  sound during the interaction.
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
  wd: Q1044799
examples:
- "Idealised billiard balls rebound without losing kinetic energy."
- "Gas molecules are often modelled with elastic collisions."
formal:
  statement: An elastic collision conserves total linear momentum and total kinetic
    energy.
  equation: p_i = p_f and K_i = K_f
  variables:
  - symbol: p
    meaning: total momentum
    unit: kg m s^-1
  - symbol: K
    meaning: total kinetic energy
    unit: J
  conditions:
  - isolated system
  - no deformation or heat loss
  dimensions: null
applications:
- "Analyzing billiard ball impacts in game physics simulations."
- "Modeling neutron scattering processes in nuclear reactors."
---

An elastic collision occurs when objects separate after impact while conserving their total kinetic energy. This idealized process ensures that no mechanical energy is transformed into heat or sound during the interaction.
