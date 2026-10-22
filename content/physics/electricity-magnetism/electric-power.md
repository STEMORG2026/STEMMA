---
id: stemma:phys.electric-power
type: concept
name: electric power
domain: physics
subdomain: electricity-magnetism
level: foundational
status: canonical
definition: Electric power quantifies the rate at which electric energy transfers through an electrical
  circuit. It measures how quickly work is performed by moving charges under the influence of voltage
  and current.
same_dimensional_quantities: null
source_refs:
- stemma:src.openstax-physics
provenance:
  ai_drafted: true
  source_kind: textbook
  source: 'Physics (2020), OpenStax. Term locator: https://openstax.org/books/physics/pages/19-key-terms.
    Used as a reference; definition independently phrased.'
  writer: process:openstax-importer.v1
  drafted_by: llm:qwen3.5-9b
  original_author: Paul Peter Urone, Roger Hinrichs, Fatih Gozuacik, Denise Pattison, Catherine Tabor
  link: https://openstax.org/books/physics/pages/19-key-terms
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
examples:
- "A 60 W lamp running on 120 V draws 0.5 A."
- "A resistor dissipates power as heat according to I squared R."
formal:
  statement: Electric power is the rate at which electrical energy is transferred by
    a current through a potential difference.
  equation: P = I V
  variables:
  - symbol: P
    meaning: electric power
    unit: W
  - symbol: I
    meaning: current
    unit: A
  - symbol: V
    meaning: potential difference
    unit: V
  conditions:
  - steady current
  - resistive or general circuit element
  dimensions: M L^2 T^-3
applications:
- "Appliance wattage ratings on packaging labels."
- "Utility billing calculations for household usage."
---

Electric power quantifies the rate at which electric energy transfers through an electrical circuit. It measures how quickly work is performed by moving charges under the influence of voltage and current.
