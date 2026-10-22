---
id: stemma:chem.calorimetry
type: technique
name: calorimetry
domain: chemistry
subdomain: general
level: foundational
status: canonical
definition: Calorimetry describes the experimental technique for measuring heat transfer during chemical
  or physical changes. This method relies on observing temperature variations within an insulated system
  to calculate energy exchange values accurately.
same_dimensional_quantities: null
source_refs:
- stemma:src.openstax-chemistry-2e
provenance:
  ai_drafted: true
  source_kind: textbook
  source: 'Chemistry 2e (2019), OpenStax. Term locator: https://openstax.org/books/chemistry-2e/pages/5-key-terms.
    Used as a reference; definition independently phrased.'
  writer: process:openstax-importer.v1
  drafted_by: llm:qwen3.5-9b
  original_author: Paul Flowers, Don Frantz, Paul Hooker, George Kaminski, Jennifer Look, Carol Martinez,
    Andrew Eklund, Mark Blaser, Klaus Theopold, Richard Langley, Tom Sorensen, Allison Soult, Troy Milliken,
    Vicki Moravec, Jason Powell, Emad El-Giar, Simon Bott, Don Carpenetti, William R. Robinson, PhD
  link: https://openstax.org/books/chemistry-2e/pages/5-key-terms
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
- "A bomb calorimeter measures the heat of combustion."
- "Coffee-cup calorimetry follows temperature change of a solution."
formal:
  statement: Calorimetry measures heat exchange as the temperature change of a known
    mass and specific heat.
  equation: q = m c Delta T
  variables:
  - symbol: q
    meaning: heat transferred
    unit: J
  - symbol: m
    meaning: mass
    unit: g
  - symbol: c
    meaning: specific heat capacity
    unit: J g^-1 K^-1
  - symbol: Delta T
    meaning: temperature change
    unit: K
  conditions:
  - no phase change
  - isolated calorimeter
  - constant specific heat over the range
  dimensions: M L^2 T^-2
applications:
- "Determining nutritional energy content of food products accurately."
- "Designing thermal management systems for electronics cooling needs."
- "Analyzing combustion efficiency in engine development projects worldwide."

limitations:
- "Heat loss to surroundings introduces unavoidable experimental error always."
- "Assumes specific heat capacities remain constant over temperature ranges tested."
- "Requires well-insulated containers which may be impractical at scale industrially."
---

Calorimetry describes the experimental technique for measuring heat transfer during chemical or physical changes. This method relies on observing temperature variations within an insulated system to calculate energy exchange values accurately.
