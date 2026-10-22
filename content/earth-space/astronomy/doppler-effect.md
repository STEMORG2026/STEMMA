---
id: stemma:earth.doppler-effect
type: phenomenon
name: Doppler effect
domain: earth-space
subdomain: astronomy
level: foundational
status: canonical
definition: The Doppler effect describes the shift in radiation frequency caused by relative motion between
  source and observer. When an object moves away, wavelengths stretch to redshift; approaching objects
  compress waves into blueshift, allowing astronomers to measure stellar velocities.
same_dimensional_quantities: null
source_refs:
- stemma:src.openstax-astronomy-2e
provenance:
  ai_drafted: true
  source_kind: textbook
  source: 'Astronomy 2e (2022), OpenStax. Term locator: https://openstax.org/books/astronomy-2e/pages/5-key-terms.
    Used as a reference; definition independently phrased.'
  writer: process:openstax-importer.v1
  drafted_by: llm:qwen3.5-9b
  original_author: Andrew Fraknoi, David Morrison, Sidney Wolff
  link: https://openstax.org/books/astronomy-2e/pages/5-key-terms
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
- "A receding galaxy shows redshifted spectral lines."
- "An approaching ambulance siren sounds higher-pitched."
formal:
  statement: For motion much slower than light, the fractional wavelength shift equals
    the line-of-sight velocity divided by the speed of light.
  equation: Delta lambda / lambda = v / c
  variables:
  - symbol: lambda
    meaning: rest wavelength
    unit: m
  - symbol: Delta lambda
    meaning: observed wavelength shift
    unit: m
  - symbol: v
    meaning: line-of-sight velocity
    unit: m s^-1
  - symbol: c
    meaning: speed of light
    unit: m s^-1
  conditions:
  - v much less than c
  - non-relativistic approximation
  dimensions: null
applications:
- "Measuring stellar radial velocities in labs."
- "Determining galaxy recession rates cosmologically."
- "Analyzing blood flow via medical ultrasound."

limitations:
- "Requires known rest frequency reference."
- "Relativistic corrections needed at high speeds."
- "Transverse motion causes secondary redshift effects."
---

The Doppler effect describes the shift in radiation frequency caused by relative motion between source and observer. When an object moves away, wavelengths stretch to redshift; approaching objects compress waves into blueshift, allowing astronomers to measure stellar velocities.
