---
id: stemma:math.parabola
type: structure
name: parabola
domain: mathematics
subdomain: precalculus
level: foundational
status: canonical
definition: A parabola is the set of points equidistant from a fixed point known as the focus and a non-intersecting
  line called the directrix. This unique geometric definition creates an open curve symmetric about its
  axis.
same_dimensional_quantities: null
source_refs:
- stemma:src.openstax-precalculus-2e
provenance:
  ai_drafted: true
  source_kind: textbook
  source: 'Precalculus 2e (2021), OpenStax. Term locator: https://openstax.org/books/precalculus-2e/pages/10-key-terms.
    Used as a reference; definition independently phrased.'
  writer: process:openstax-importer.v1
  drafted_by: llm:qwen3.5-9b
  original_author: Jay Abramson, Valeree Falduto, Rachael Gross, David Lippman, Melonie Rasmussen, Rick
    Norwood, Nicholas Belloit, Harold Whipple, Jean-Marie Magnier, Christina Fernandez
  link: https://openstax.org/books/precalculus-2e/pages/10-key-terms
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
- "A projectile's path near Earth is approximately a parabola."
- "Parabolic mirrors focus parallel light to a point."
formal:
  statement: A parabola is the locus of points equidistant from a fixed focus and a
    fixed directrix.
  equation: y = a x^2 + b x + c
  variables:
  - symbol: a, b, c
    meaning: coefficients with a not zero
  conditions:
  - a not equal to 0
  - axis parallel to the y-axis in this form
  dimensions: null
applications:
- "Designing satellite dishes for optimal signal reflection paths."
- "Calculating projectile motion trajectories in physics labs."
---

A parabola is the set of points equidistant from a fixed point known as the focus and a non-intersecting line called the directrix. This unique geometric definition creates an open curve symmetric about its axis.
