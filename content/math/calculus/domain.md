---
id: stemma:math.domain
type: concept
name: domain
domain: mathematics
subdomain: calculus
level: foundational
status: canonical
definition: The domain of a function specifies the complete set of allowable input values for which the
  rule is defined. Identifying this restriction ensures mathematical validity by excluding inputs that
  would cause undefined operations like division by zero or taking square roots of negative numbers.
same_dimensional_quantities: null
source_refs:
- stemma:src.openstax-calculus-volume-1
provenance:
  ai_drafted: true
  source_kind: textbook
  source: 'Calculus Volume 1 (2016), OpenStax. Term locator: https://openstax.org/books/calculus-volume-1/pages/1-key-terms.
    Used as a reference; definition independently phrased.'
  writer: process:openstax-importer.v1
  drafted_by: llm:qwen3.5-9b
  original_author: Gilbert Strang, Joseph Lakey, Elaine A. Terry, Alfred K. Mulzet, Sheri J. Boyd, Joyati
    Debnath, Michelle Merriweather, David Smith, Nicoleta Virginia Bila, Valeree Falduto, Kirsten R. Messer,
    William Radulovich, Erica M. Rutter, David Torain, Edwin “Jed” Herman, Catherine Abbott, Julie Levandosky,
    David McCune
  link: https://openstax.org/books/calculus-volume-1/pages/1-key-terms
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
- "Ensuring software inputs avoid division by zero errors."
- "Validating sensor readings within physical measurement limits."
---

The domain of a function specifies the complete set of allowable input values for which the rule is defined. Identifying this restriction ensures mathematical validity by excluding inputs that would cause undefined operations like division by zero or taking square roots of negative numbers.
