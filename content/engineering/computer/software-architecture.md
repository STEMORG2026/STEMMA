---
id: stemma:eng.software-architecture
type: model
name: software architecture
domain: engineering
subdomain: computer
level: intermediate
status: canonical
definition: Software architecture is the high-level structure defining a system's major components, their
  responsibilities, and how they interact. This blueprint guides development teams in building scalable
  solutions while ensuring that interrelationships between modules support long-term maintainability.
examples: []
same_dimensional_quantities: null
source_refs:
- stemma:src.openstax-introduction-computer-science
provenance:
  ai_drafted: true
  source_kind: textbook
  source: 'Introduction to Computer Science (2024), OpenStax. Term locator: https://openstax.org/books/introduction-computer-science/pages/9-key-terms.
    Used as a reference; definition independently phrased.'
  writer: process:openstax-importer.v1
  drafted_by: llm:qwen3.5-9b
  original_author: Dr. Jean-Claude Franchitti, Amal Alhosban, Mark Buckler, Joanna Gilberti, Scott Gray,
    Matthew Hertz, Andrew Hurd, Kevin Lin, Sai Mukkavilli, Phuc (Brian) Nguyen, Shahab Tayeb, Zdeněk Troníček,
    Kevin Wortman, Mohamed Zahran
  link: https://openstax.org/books/introduction-computer-science/pages/9-key-terms
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
- "Designing cloud-native platforms for global e-commerce sites."
- "Structuring safety-critical avionics control systems."
- "Planning enterprise data lakes for analytics workloads."

limitations:
- "Overly rigid architectures struggle with rapid market shifts."
- "Complex diagrams often fail to capture dynamic behaviors."
- "Early architectural decisions are hard to reverse later."
---

Software architecture is the high-level structure defining a system's major components, their responsibilities, and how they interact. This blueprint guides development teams in building scalable solutions while ensuring that interrelationships between modules support long-term maintainability.
