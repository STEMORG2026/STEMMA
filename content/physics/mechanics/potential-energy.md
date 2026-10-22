---
id: stemma:phys.potential-energy
type: concept
name: potential energy
domain: physics
subdomain: mechanics
level: foundational
status: canonical
definition: Potential energy is a position-dependent function representing stored capacity to do work.
  Its value relies on the configuration of objects relative to one another within the system.
same_dimensional_quantities: null
source_refs:
- stemma:src.openstax-university-physics-volume-1
provenance:
  ai_drafted: true
  source_kind: textbook
  source: 'University Physics Volume 1 (2016), OpenStax. Term locator: https://openstax.org/books/university-physics-volume-1/pages/8-key-terms.
    Used as a reference; definition independently phrased.'
  writer: process:openstax-importer.v1
  drafted_by: llm:qwen3.5-9b
  original_author: Stephen D. Druger, William Moebs, Samuel J. Ling, Jeff Sanny, David Anderson, Daniel
    Bowman, Gerald Friedman, Edw. S. Ginsberg, Kenneth Podolak, Takashi Sato, David Smith, Joseph Trout,
    Kevin Wheelock, Dedra Demaree, Richard Ludlow, Patrick Motl, Lev Gasparov, Lee LaRue, Mark Lattery,
    Tao Pang, Alice Kolakowska
  link: https://openstax.org/books/university-physics-volume-1/pages/8-key-terms
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
- stemma:phys.newtons-second-law
- stemma:phys.conservation-energy
rights:
  license: CC-BY-4.0
  attribution: Original STEMMA definition generated from the cited reference; no source prose copied.
external_ids:
  wd: Q155640
examples:
- "A raised book stores gravitational potential energy relative to the floor."
- "A compressed spring stores elastic potential energy."
formal:
  statement: The change in potential energy equals the negative of the work done by
    a conservative force.
  equation: Delta U = -W_conservative
  variables:
  - symbol: U
    meaning: potential energy
    unit: J
  - symbol: W
    meaning: work done by the conservative force
    unit: J
  conditions:
  - conservative force field
  - reference zero chosen for U
  dimensions: M L^2 T^-2
applications:
- "Designing hydroelectric dam reservoirs for power generation cycles."
- "Sizing spring mechanisms in mechanical watches or vehicle suspensions."
- "Modeling chemical bond stability in molecular structure analysis."

limitations:
- "Values depend entirely on arbitrary reference point selection."
- "Only defined strictly within conservative force field contexts."
- "Ignores non-conservative forces like air resistance during transitions."
---

Potential energy is a position-dependent function representing stored capacity to do work. Its value relies on the configuration of objects relative to one another within the system.
