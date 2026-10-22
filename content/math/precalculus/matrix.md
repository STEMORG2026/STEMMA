---
id: stemma:math.matrix
type: structure
name: matrix
domain: mathematics
subdomain: precalculus
level: intermediate
status: canonical
definition: A rectangular array of numbers, symbols, or expressions arranged in rows and columns. Matrices
  encode linear transformations and systems of equations; they are added entrywise, multiplied under a
  row-by-column rule, and analyzed through determinants, rank, and eigenvalues.
same_dimensional_quantities: null
source_refs:
- stemma:src.openstax-precalculus-2e
provenance:
  ai_drafted: true
  source_kind: textbook
  source: 'Precalculus 2e (2021), OpenStax. Term locator: https://openstax.org/books/precalculus-2e/pages/9-key-terms.
    Used as a reference; definition independently phrased.'
  writer: process:openstax-importer.v1
  drafted_by: llm:qwen3.5-9b
  original_author: Jay Abramson, Valeree Falduto, Rachael Gross, David Lippman, Melonie Rasmussen, Rick
    Norwood, Nicholas Belloit, Harold Whipple, Jean-Marie Magnier, Christina Fernandez
  link: https://openstax.org/books/precalculus-2e/pages/9-key-terms
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
- "A 2x3 matrix has two rows and three columns."
- "Matrix multiplication composes two linear transformations."
formal:
  statement: The entry in row i and column j of a product matrix is the dot product
    of row i of the first factor with column j of the second.
  equation: (AB)_{ij} = sum_k A_{ik} B_{kj}
  variables:
  - symbol: A, B
    meaning: compatible matrices
  - symbol: i, j, k
    meaning: row, column, and summation indices
  conditions:
  - inner dimensions match
  - entries from a common field
  dimensions: null
applications:
- "Rendering 3D graphics transformations in computer software."
- "Solving large-scale economic input-output models efficiently."
---

A rectangular array of numbers, symbols, or expressions arranged in rows and columns. Matrices encode linear transformations and systems of equations; they are added entrywise, multiplied under a row-by-column rule, and analyzed through determinants, rank, and eigenvalues.
