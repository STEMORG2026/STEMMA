---
id: stemma:phys.first-law-thermodynamics
type: law
name: first law of thermodynamics
domain: physics
subdomain: thermal-physics
level: foundational
status: canonical
definition: The first law states that internal energy change equals heat added minus work done by the
  system. This principle establishes conservation of energy for any transition between equilibrium states.
same_dimensional_quantities: null
source_refs:
- stemma:src.openstax-university-physics-volume-2
provenance:
  ai_drafted: true
  source_kind: textbook
  source: 'University Physics Volume 2 (2016), OpenStax. Term locator: https://openstax.org/books/university-physics-volume-2/pages/3-key-terms.
    Used as a reference; definition independently phrased.'
  writer: process:openstax-importer.v1
  drafted_by: llm:qwen3.5-9b
  original_author: Gerald Friedman, Stephen D. Druger, Alice Kolakowska, Samuel J. Ling, David Anderson,
    Daniel Bowman, William Moebs, Lev Gasparov, Jeff Sanny, Lee LaRue, Mark Lattery, Richard Ludlow, Patrick
    Motl, Dedra Demaree, Edw. S. Ginsberg, David Smith, Joseph Trout, Kevin Wheelock, Tao Pang, Kenneth
    Podolak, Takashi Sato
  link: https://openstax.org/books/university-physics-volume-2/pages/3-key-terms
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
- stemma:phys.zeroth-law-thermodynamics
- stemma:phys.ideal-gas-law
rights:
  license: CC-BY-4.0
  attribution: Original STEMMA definition generated from the cited reference; no source prose copied.
examples:
- "A gas absorbing 100 J and doing 40 J of work increases its internal energy by 60\
  \ J."
- "Adiabatic compression raises internal energy because work is done on the system with\
  \ no heat transfer."
formal:
  statement: For a closed system, the change in internal energy equals the heat added
    to the system minus the work done by the system.
  equation: Delta U = Q - W
  variables:
  - symbol: U
    meaning: internal energy
    unit: J
  - symbol: Q
    meaning: heat added to the system
    unit: J
  - symbol: W
    meaning: work done by the system
    unit: J
  conditions:
  - closed system
  - 'sign convention: W is work done by the system'
  dimensions: M L^2 T^-2
historical:
  stated_by: "Rudolf Clausius"
  year: 1850
  where: "Ueber die bewegende Kraft der Wärme (1850)"
  timeline:
  - year: 1850
    event: "Clausius gives the first explicit statement of the first law for thermodynamic cycles"
applications:
- "Engine cycle analysis."
- "Building HVAC load calculations"
---

The first law states that internal energy change equals heat added minus work done by the system. This principle establishes conservation of energy for any transition between equilibrium states.
