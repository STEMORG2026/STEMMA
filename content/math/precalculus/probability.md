---
id: stemma:math.probability
type: concept
name: probability
domain: mathematics
subdomain: precalculus
level: foundational
status: canonical
definition: A number from zero to one expressing how likely an event is under a stated model or experiment.
  Frequencies over repeated trials approach theoretical probabilities, and the rules of probability combine
  events through complements, unions, and conditional dependence.
same_dimensional_quantities: null
source_refs:
- stemma:src.openstax-precalculus-2e
provenance:
  ai_drafted: true
  source_kind: textbook
  source: 'Precalculus 2e (2021), OpenStax. Term locator: https://openstax.org/books/precalculus-2e/pages/11-key-terms.
    Used as a reference; definition independently phrased.'
  writer: process:openstax-importer.v1
  drafted_by: llm:qwen3.5-9b
  original_author: Jay Abramson, Valeree Falduto, Rachael Gross, David Lippman, Melonie Rasmussen, Rick
    Norwood, Nicholas Belloit, Harold Whipple, Jean-Marie Magnier, Christina Fernandez
  link: https://openstax.org/books/precalculus-2e/pages/11-key-terms
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
- "A fair coin has probability 1/2 of landing heads."
- "The probability of rolling an even number on a fair die is 1/2."
formal:
  statement: For equally likely outcomes, the probability of an event is the number
    of favorable outcomes divided by the total number of outcomes.
  equation: P(A) = |A| / |Omega|
  variables:
  - symbol: A
    meaning: event
  - symbol: Omega
    meaning: sample space
  conditions:
  - finite sample space
  - outcomes equally likely
  dimensions: null
applications:
- "Predicting weather patterns and insurance risk assessment."
- "Designing randomized controlled trials in clinical research."
---

A number from zero to one expressing how likely an event is under a stated model or experiment. Frequencies over repeated trials approach theoretical probabilities, and the rules of probability combine events through complements, unions, and conditional dependence.
