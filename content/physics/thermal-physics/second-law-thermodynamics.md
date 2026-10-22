---
id: stemma:phys.second-law-thermodynamics
type: law
name: second law of thermodynamics
domain: physics
subdomain: thermal-physics
level: intermediate
status: canonical
definition: The second law dictates that total entropy never decreases in a spontaneous process. It implies
  the directionality of natural changes and limits the efficiency of heat engines.
same_dimensional_quantities: null
source_refs:
- stemma:src.openstax-physics
provenance:
  ai_drafted: true
  source_kind: textbook
  source: 'Physics (2020), OpenStax. Term locator: https://openstax.org/books/physics/pages/12-key-terms.
    Used as a reference; definition independently phrased.'
  writer: process:openstax-importer.v1
  drafted_by: llm:qwen3.5-9b
  original_author: Paul Peter Urone, Roger Hinrichs, Fatih Gozuacik, Denise Pattison, Catherine Tabor
  link: https://openstax.org/books/physics/pages/12-key-terms
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
- stemma:phys.first-law-thermodynamics
- stemma:phys.zeroth-law-thermodynamics
historical:
  stated_by: "Rudolf Clausius and William Thomson"
  year: 1850
  where: "Clausius (1850); Thomson (1851)"
  timeline:
  - year: 1824
    event: "Carnot publishes his principle on heat-engine efficiency"
  - year: 1850
    event: "Clausius states the heat-flow form of the second law"
  - year: 1851
    event: "Thomson states the Kelvin-Planck form"
applications:
- "Refrigerator performance rating."
- "Climate change energy models"

limitations:
- "Idealized reversible processes excluded."
---

The second law dictates that total entropy never decreases in a spontaneous process. It implies the directionality of natural changes and limits the efficiency of heat engines.
