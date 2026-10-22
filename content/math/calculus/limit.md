---
id: stemma:math.limit
type: concept
name: limit
domain: mathematics
subdomain: calculus
level: intermediate
status: canonical
definition: The value that a function or sequence approaches as its input or index approaches a target.
  Limits formalize closeness without requiring the target point itself to be reached, and they underpin
  continuity, derivatives, and convergence.
same_dimensional_quantities: null
source_refs:
- stemma:src.openstax-calculus-volume-1
provenance:
  ai_drafted: true
  source_kind: textbook
  source: 'Calculus Volume 1 (2016), OpenStax. Term locator: https://openstax.org/books/calculus-volume-1/pages/2-key-terms.
    Used as a reference; definition independently phrased.'
  writer: process:openstax-importer.v1
  drafted_by: llm:qwen3.5-9b
  original_author: Gilbert Strang, Joseph Lakey, Elaine A. Terry, Alfred K. Mulzet, Sheri J. Boyd, Joyati
    Debnath, Michelle Merriweather, David Smith, Nicoleta Virginia Bila, Valeree Falduto, Kirsten R. Messer,
    William Radulovich, Erica M. Rutter, David Torain, Edwin “Jed” Herman, Catherine Abbott, Julie Levandosky,
    David McCune
  link: https://openstax.org/books/calculus-volume-1/pages/2-key-terms
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
- "The limit of sin(x)/x as x approaches 0 is 1."
- "A function can have a limit at a point where it is undefined."
formal:
  statement: For every positive epsilon there exists a positive delta such that inputs
    within delta of a, but distinct from a, map within epsilon of L.
  equation: lim_{x -> a} f(x) = L
  variables:
  - symbol: a
    meaning: target input
  - symbol: L
    meaning: limit value
  - symbol: epsilon
    meaning: output tolerance
  - symbol: delta
    meaning: input tolerance
  conditions:
  - two-sided limit
  - f defined on a punctured neighbourhood of a
  dimensions: null
applications:
- "Designing tolerance limits for manufacturing parts."
- "Ensuring algorithm stability under varying data inputs."
---

The value that a function or sequence approaches as its input or index approaches a target. Limits formalize closeness without requiring the target point itself to be reached, and they underpin continuity, derivatives, and convergence.
