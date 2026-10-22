---
id: stemma:chem.limiting-reactant
type: concept
name: limiting reactant
domain: chemistry
subdomain: general
level: foundational
status: canonical
definition: The limiting reactant exists in an amount lower than required by stoichiometric ratios. Consequently,
  this specific substance determines the maximum quantity of product that can be generated before the
  reaction ceases.
same_dimensional_quantities: null
source_refs:
- stemma:src.openstax-chemistry-2e
provenance:
  ai_drafted: true
  source_kind: textbook
  source: 'Chemistry 2e (2019), OpenStax. Term locator: https://openstax.org/books/chemistry-2e/pages/4-key-terms.
    Used as a reference; definition independently phrased.'
  writer: process:openstax-importer.v1
  drafted_by: llm:qwen3.5-9b
  original_author: Paul Flowers, Don Frantz, Paul Hooker, George Kaminski, Jennifer Look, Carol Martinez,
    Andrew Eklund, Mark Blaser, Klaus Theopold, Richard Langley, Tom Sorensen, Allison Soult, Troy Milliken,
    Vicki Moravec, Jason Powell, Emad El-Giar, Simon Bott, Don Carpenetti, William R. Robinson, PhD
  link: https://openstax.org/books/chemistry-2e/pages/4-key-terms
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
- "With 2 mol H2 and 1 mol O2, oxygen limits water formation."
- "Excess reagent remains after the reaction stops."
formal:
  statement: The limiting reactant is the reagent whose stoichiometric requirement is
    exhausted first, fixing the maximum product amount.
  equation: compare n_i / nu_i across reactants
  variables:
  - symbol: n_i
    meaning: moles of reactant i
    unit: mol
  - symbol: nu_i
    meaning: stoichiometric coefficient of reactant i
  conditions:
  - balanced chemical equation
  - reaction goes to completion
  dimensions: null
applications:
- "Optimizing raw material usage in manufacturing plants."
- "Scaling up pharmaceutical synthesis protocols safely."
- "Balancing chemical equations for waste reduction."
---

The limiting reactant exists in an amount lower than required by stoichiometric ratios. Consequently, this specific substance determines the maximum quantity of product that can be generated before the reaction ceases.
