---
id: stemma:eng.normalization
type: process
name: normalization
domain: engineering
subdomain: data-engineering
level: intermediate
status: canonical
definition: Normalization is a data preprocessing technique that scales numerical values into a consistent
  range, typically between zero and one. By eliminating scale differences across variables, this method
  facilitates accurate comparisons and improves the performance of machine learning algorithms.
examples: []
same_dimensional_quantities: null
source_refs:
- stemma:src.openstax-principles-data-science
provenance:
  ai_drafted: true
  source_kind: textbook
  source: 'Principles of Data Science (2025), OpenStax. Term locator: https://openstax.org/books/principles-data-science/pages/2-key-terms.
    Used as a reference; definition independently phrased.'
  writer: process:openstax-importer.v1
  drafted_by: llm:qwen3.5-9b
  original_author: Dr. Shaun V. Ault, Dr. Soohyun Nam Liao, Larry Musolino, Wisam Bukaita, Aeron Zentner
  link: https://openstax.org/books/principles-data-science/pages/2-key-terms
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
applications:
- "Preparing image pixel values for neural network training."
- "Comparing sensor readings with vastly different physical units."
- "Balancing input features before applying gradient descent methods."

limitations:
- "Distorts data distributions if outliers are not handled."
- "Assumes linear relationships between original and scaled values."
- "May lose interpretability of absolute magnitude in raw data."
---

Normalization is a data preprocessing technique that scales numerical values into a consistent range, typically between zero and one. By eliminating scale differences across variables, this method facilitates accurate comparisons and improves the performance of machine learning algorithms.
