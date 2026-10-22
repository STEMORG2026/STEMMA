---
id: stemma:earth.adaptive-optics
type: technique
name: adaptive optics
domain: earth-space
subdomain: astronomy
level: intermediate
status: canonical
definition: Adaptive optics are advanced systems integrated into telescopes to correct image distortions
  caused by Earth's atmosphere. By rapidly adjusting mirror shapes in response to atmospheric turbulence,
  these technologies restore sharpness and significantly improve the resolution of astronomical observations.
examples: []
same_dimensional_quantities: null
source_refs:
- stemma:src.openstax-astronomy-2e
provenance:
  ai_drafted: true
  source_kind: textbook
  source: 'Astronomy 2e (2022), OpenStax. Term locator: https://openstax.org/books/astronomy-2e/pages/6-key-terms.
    Used as a reference; definition independently phrased.'
  writer: process:openstax-importer.v1
  drafted_by: llm:qwen3.5-9b
  original_author: Andrew Fraknoi, David Morrison, Sidney Wolff
  link: https://openstax.org/books/astronomy-2e/pages/6-key-terms
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
- "Enabling high-resolution imaging of exoplanets."
- "Improving laser guide star performance for astronomy."
- "Enhancing medical endoscopy through tissue distortion."

limitations:
- "Requires bright reference stars or lasers nearby."
- "Computationally intensive with latency constraints."
- "Limited effectiveness in highly turbulent conditions."
---

Adaptive optics are advanced systems integrated into telescopes to correct image distortions caused by Earth's atmosphere. By rapidly adjusting mirror shapes in response to atmospheric turbulence, these technologies restore sharpness and significantly improve the resolution of astronomical observations.
