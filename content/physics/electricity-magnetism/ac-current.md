---
id: stemma:phys.ac-current
type: concept
name: ac current
domain: physics
subdomain: electricity-magnetism
level: foundational
status: canonical
definition: Current that periodically reverses direction, usually described by a sinusoidal waveform.
  Its magnitude is quoted as a root-mean-square value for power calculations, and its frequency is set
  by the source.
same_dimensional_quantities: null
source_refs:
- stemma:src.openstax-university-physics-volume-2
provenance:
  ai_drafted: true
  source_kind: textbook
  source: 'University Physics Volume 2 (2016), OpenStax. Term locator: https://openstax.org/books/university-physics-volume-2/pages/15-key-terms.
    Used as a reference; definition independently phrased.'
  writer: process:openstax-importer.v1
  drafted_by: llm:qwen3.5-9b
  original_author: Gerald Friedman, Stephen D. Druger, Alice Kolakowska, Samuel J. Ling, David Anderson,
    Daniel Bowman, William Moebs, Lev Gasparov, Jeff Sanny, Lee LaRue, Mark Lattery, Richard Ludlow, Patrick
    Motl, Dedra Demaree, Edw. S. Ginsberg, David Smith, Joseph Trout, Kevin Wheelock, Tao Pang, Kenneth
    Podolak, Takashi Sato
  link: https://openstax.org/books/university-physics-volume-2/pages/15-key-terms
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
governed_by:
- stemma:phys.coulombs-law
- stemma:phys.faraday-law
rights:
  license: CC-BY-4.0
  attribution: Original STEMMA definition generated from the cited reference; no source prose copied.
applications:
- "Power distribution grids utilizing 50 or 60 Hz frequencies for efficient transmission."
- "Audio amplifiers converting direct signals into varying electrical currents for speakers."
- "Wireless charging systems inducing oscillating magnetic fields to transfer energy."

limitations:
- "Standard RMS formulas assume ideal sinusoidal waveforms without significant harmonic\
  \ distortion."
- "Skin effect increases resistance at very high frequencies, invalidating simple DC\
  \ models."
- "Non-linear loads generate harmonics that complicate pure sine-wave power calculations."
---

Current that periodically reverses direction, usually described by a sinusoidal waveform. Its magnitude is quoted as a root-mean-square value for power calculations, and its frequency is set by the source.
