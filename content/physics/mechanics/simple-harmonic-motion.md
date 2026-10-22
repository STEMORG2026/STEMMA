---
id: stemma:phys.simple-harmonic-motion
type: phenomenon
name: simple harmonic motion
domain: physics
subdomain: mechanics
level: foundational
status: canonical
definition: Simple harmonic motion describes oscillatory movement in systems where net force follows Hooke's
  law. This specific type of periodic motion occurs when restoring forces are directly proportional to
  displacement from equilibrium.
same_dimensional_quantities: null
source_refs:
- stemma:src.openstax-physics
provenance:
  ai_drafted: true
  source_kind: textbook
  source: 'Physics (2020), OpenStax. Term locator: https://openstax.org/books/physics/pages/5-key-terms.
    Used as a reference; definition independently phrased.'
  writer: process:openstax-importer.v1
  drafted_by: llm:qwen3.5-9b
  original_author: Paul Peter Urone, Roger Hinrichs, Fatih Gozuacik, Denise Pattison, Catherine Tabor
  link: https://openstax.org/books/physics/pages/5-key-terms
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
  wd: Q835975
examples:
- "A mass on an ideal spring oscillates with constant period."
- "A small-angle pendulum approximates simple harmonic motion."
formal:
  statement: Simple harmonic motion is periodic motion whose acceleration is proportional
    to displacement and directed toward the equilibrium position.
  equation: a = -omega^2 x
  variables:
  - symbol: a
    meaning: acceleration
    unit: m s^-2
  - symbol: omega
    meaning: angular frequency
    unit: rad s^-1
  - symbol: x
    meaning: displacement from equilibrium
    unit: m
  conditions:
  - linear restoring force
  - small oscillations about stable equilibrium
  dimensions: L T^-2
applications:
- "Tuning guitar strings for specific musical note frequencies."
- "Designing building dampers to reduce earthquake structural sway."
- "Analyzing pendulum clocks for precise timekeeping mechanisms."

limitations:
- "Assumes ideal springs with zero internal friction or damping."
- "Breaks down when amplitudes become large enough to distort linearity."
- "Requires strictly linear restoring forces proportional to displacement."
---

Simple harmonic motion describes oscillatory movement in systems where net force follows Hooke's law. This specific type of periodic motion occurs when restoring forces are directly proportional to displacement from equilibrium.
