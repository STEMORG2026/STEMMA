---
id: stemma:math.combination
type: concept
name: combination
domain: mathematics
subdomain: precalculus
level: foundational
status: canonical
definition: A selection of items in which order is irrelevant, so choosing the same members in a different
  sequence counts as one outcome. Combinations are counted with binomial coefficients and are used for
  sampling and unordered subsets.
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
- "Choosing 3 students from 10 to form a committee gives C(10,3) = 120 combinations."
- "A five-card poker hand is a combination because card order does not matter."
formal:
  statement: The number of k-element subsets of an n-element set is n factorial divided
    by k factorial times n minus k factorial.
  equation: C(n,k) = n! / (k! (n-k)!)
  variables:
  - symbol: n
    meaning: total number of items
  - symbol: k
    meaning: number selected
  conditions:
  - 0 <= k <= n
  - order does not matter
  - no repetition
  dimensions: null
applications:
- "Sampling without replacement in statistical surveys."
- "Determining possible lottery ticket combinations mathematically."
---

A selection of items in which order is irrelevant, so choosing the same members in a different sequence counts as one outcome. Combinations are counted with binomial coefficients and are used for sampling and unordered subsets.
