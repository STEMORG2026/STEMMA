---
id: stemma:math.mean
type: concept
name: Mean
domain: mathematics
subdomain: statistics-probability
level: intermediate
status: canonical
definition: A measure of central location found by adding all observations and dividing by their count.
  The arithmetic mean is sensitive to extreme values, while weighted, geometric, and harmonic means suit
  different data structures and rates.
same_dimensional_quantities: null
source_refs:
- stemma:src.openstax-introductory-statistics-2e
provenance:
  ai_drafted: true
  source_kind: textbook
  source: 'Introductory Statistics 2e (2023), OpenStax. Term locator: https://openstax.org/books/introductory-statistics-2e/pages/2-key-terms.
    Used as a reference; definition independently phrased.'
  writer: process:openstax-importer.v1
  drafted_by: llm:qwen3.5-9b
  original_author: Barbara Illowsky, Susan Dean, Daniel Birmajer, Bryan Blount, Sheri Boyd, Matthew Einsohn,
    Nancy Foreman, James Helmreich, Lynette Kenyon, Sheldon Lee, Jeff Taub
  link: https://openstax.org/books/introductory-statistics-2e/pages/2-key-terms
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
- "The mean of 2, 4, and 9 is 5."
- "A trimmed mean reduces the influence of outliers."
formal:
  statement: The arithmetic mean is the sum of observations divided by the number of
    observations.
  equation: x_bar = (1/n) sum_{i=1}^{n} x_i
  variables:
  - symbol: x_bar
    meaning: sample mean
  - symbol: x_i
    meaning: i-th observation
  - symbol: n
    meaning: number of observations
  conditions:
  - quantitative data
  - n > 0
  dimensions: null
applications:
- "Determining average household income in economic reports."
- "Balancing chemical reaction stoichiometry ratios."
---

A measure of central location found by adding all observations and dividing by their count. The arithmetic mean is sensitive to extreme values, while weighted, geometric, and harmonic means suit different data structures and rates.
