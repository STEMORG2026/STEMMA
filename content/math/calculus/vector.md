---
id: stemma:math.vector
type: concept
name: vector
domain: mathematics
subdomain: calculus
level: foundational
status: canonical
definition: A quantity with both magnitude and direction that combines under vector addition and scalar
  multiplication. Vectors represent displacements, velocities, and forces, and in coordinate systems they
  are written as ordered components with a norm and inner product.
same_dimensional_quantities: null
source_refs:
- stemma:src.openstax-calculus-volume-3
provenance:
  ai_drafted: true
  source_kind: textbook
  source: 'Calculus Volume 3 (2016), OpenStax. Term locator: https://openstax.org/books/calculus-volume-3/pages/2-key-terms.
    Used as a reference; definition independently phrased.'
  writer: process:openstax-importer.v1
  drafted_by: llm:qwen3.5-9b
  original_author: Gilbert Strang, Nicoleta Virginia Bila, Sheri J. Boyd, David Smith, Elaine A. Terry,
    David Torain, Edwin “Jed” Herman, Kirsten R. Messer, Alfred K. Mulzet, William Radulovich, Erica M.
    Rutter, David McCune, Michelle Merriweather, Joseph Lakey, Julie Levandosky, Valeree Falduto, Catherine
    Abbott, Joyati Debnath
  link: https://openstax.org/books/calculus-volume-3/pages/2-key-terms
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
- "A displacement of 3 m east and 4 m north has magnitude 5 m."
- "Wind velocity combines speed with direction."
formal:
  statement: A vector in three dimensions is a linear combination of orthonormal basis
    vectors.
  equation: v = v_x i + v_y j + v_z k
  variables:
  - symbol: v
    meaning: vector
  - symbol: v_x, v_y, v_z
    meaning: components
  - symbol: i, j, k
    meaning: orthonormal basis vectors
  conditions:
  - chosen coordinate system
  - Euclidean space
  dimensions: null
applications:
- "Navigating aircraft using wind velocity correction vectors."
- "Analyzing stress tensors in structural engineering beams."
- "Rendering 3D graphics through position and direction data."
---

A quantity with both magnitude and direction that combines under vector addition and scalar multiplication. Vectors represent displacements, velocities, and forces, and in coordinate systems they are written as ordered components with a norm and inner product.
