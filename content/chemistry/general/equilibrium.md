---
id: stemma:chem.equilibrium
type: concept
name: equilibrium
domain: chemistry
subdomain: general
level: foundational
status: canonical
definition: A condition in a reversible process where opposing reaction rates balance, so the amounts
  of reactants and products stop changing at the macroscopic level. The system remains dynamic at the
  molecular scale, with both directions continuing at equal rates.
same_dimensional_quantities: null
source_refs:
- stemma:src.openstax-chemistry-2e
provenance:
  ai_drafted: true
  source_kind: textbook
  source: 'Chemistry 2e (2019), OpenStax. Term locator: https://openstax.org/books/chemistry-2e/pages/13-key-terms.
    Used as a reference; definition independently phrased.'
  writer: process:openstax-importer.v1
  drafted_by: llm:qwen3.5-9b
  original_author: Paul Flowers, Don Frantz, Paul Hooker, George Kaminski, Jennifer Look, Carol Martinez,
    Andrew Eklund, Mark Blaser, Klaus Theopold, Richard Langley, Tom Sorensen, Allison Soult, Troy Milliken,
    Vicki Moravec, Jason Powell, Emad El-Giar, Simon Bott, Don Carpenetti, William R. Robinson, PhD
  link: https://openstax.org/books/chemistry-2e/pages/13-key-terms
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
- "At equilibrium, the forward and reverse rates of a reaction match."
- "Adding reactant shifts the equilibrium position toward products."
formal:
  statement: At equilibrium, the reaction quotient equals the equilibrium constant expressed
    in activities.
  equation: K = prod a_products^{nu} / prod a_reactants^{nu}
  variables:
  - symbol: K
    meaning: equilibrium constant
  - symbol: a
    meaning: activity
  - symbol: nu
    meaning: stoichiometric coefficient
  conditions:
  - dynamic equilibrium
  - activities at equilibrium
  - stated temperature
  dimensions: null
applications:
- "Optimizing yield in industrial chemical synthesis processes."
- "Understanding blood pH regulation via buffer systems."
- "Analyzing atmospheric gas composition changes."
---

A condition in a reversible process where opposing reaction rates balance, so the amounts of reactants and products stop changing at the macroscopic level. The system remains dynamic at the molecular scale, with both directions continuing at equal rates.
