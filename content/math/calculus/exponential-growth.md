---
id: stemma:math.exponential-growth
type: concept
name: exponential growth
domain: mathematics
subdomain: calculus
level: foundational
status: canonical
definition: Exponential growth describes a dynamic process where system quantities increase at rates proportional
  to their current values. This behavior follows a specific mathematical model characterized by the equation
  y equals y sub zero times e raised to the power of k t.
same_dimensional_quantities: null
source_refs:
- stemma:src.openstax-calculus-volume-1
provenance:
  ai_drafted: true
  source_kind: textbook
  source: 'Calculus Volume 1 (2016), OpenStax. Term locator: https://openstax.org/books/calculus-volume-1/pages/6-key-terms.
    Used as a reference; definition independently phrased.'
  writer: process:openstax-importer.v1
  drafted_by: llm:qwen3.5-9b
  original_author: Gilbert Strang, Joseph Lakey, Elaine A. Terry, Alfred K. Mulzet, Sheri J. Boyd, Joyati
    Debnath, Michelle Merriweather, David Smith, Nicoleta Virginia Bila, Valeree Falduto, Kirsten R. Messer,
    William Radulovich, Erica M. Rutter, David Torain, Edwin “Jed” Herman, Catherine Abbott, Julie Levandosky,
    David McCune
  link: https://openstax.org/books/calculus-volume-1/pages/6-key-terms
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
- "A population with unlimited resources can grow exponentially at first."
- "Compound interest at a fixed rate follows exponential growth."
formal:
  statement: A quantity exhibits exponential growth when its rate of change is proportional
    to its current value.
  equation: N(t) = N_0 e^{k t}
  variables:
  - symbol: N
    meaning: quantity at time t
  - symbol: N_0
    meaning: initial quantity
  - symbol: k
    meaning: positive growth constant
    unit: s^-1
  - symbol: t
    meaning: time
    unit: s
  conditions:
  - constant positive growth rate
  - unlimited resources in the modelled regime
  dimensions: null
applications:
- "Forecasting viral spread during early pandemic phases."
- "Estimating compound interest on long-term investments."
---

Exponential growth describes a dynamic process where system quantities increase at rates proportional to their current values. This behavior follows a specific mathematical model characterized by the equation y equals y sub zero times e raised to the power of k t.
