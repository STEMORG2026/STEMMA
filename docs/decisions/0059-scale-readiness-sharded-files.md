# ADR-0059: Stay on Sharded Files + Merkle Manifest Through 10^5

Status: Decided — 2026-10-21
Date: 2026-10-21
Decided by: Sajan (sole owner), through the R8 work order
Relates to: ADR-0022 (determinism), ADR-0054 (consumer surface), R8 scale work

## Context

The corpus is a git repository of one Markdown file per entity. At 10^4–10^5 entities the
authoring loop must still be fast enough to run on a laptop, and consumers need a way to
verify a checkout without trusting timestamps. A database or object store would add
operational surface that the current review process does not need.

## Decision

1. Keep sharded Markdown files in git as the canonical store through **10^5 entities**.
2. Put large binary assets (PDFs, images, derived archives) behind Git LFS rather than in
   ordinary git objects.
3. Add `scripts/content_store.py`: per-file SHA-256 plus a deterministic Merkle root over
   `content/`, written to `exports/content-manifest.json`. `--check` detects drift and
   tampering; it is part of `verify_all.py`.
4. Revisit a database/object store only when a measured trigger fires (see
   `docs/SCALE-READINESS.md`), not on aesthetic grounds.

## Evidence

`scripts/scale_benchmark.py` builds a throwaway git repository and measures the authoring
loop. On the 2026-10-21 run (local filesystem, synthetic records):

- 10,000 entities: write 0.25 s; `git status` median 0.066 s; validation-shaped read median
  0.122 s.
- 100,000 entities (supplemental, `reports/scale-benchmark-100k.*`): write 3.90 s;
  `git add` 3.61 s; `git status` median 0.134 s; validation-shaped read median 2.30 s.

The numbers are environment-specific and the synthetic records are smaller than fully
sourced ones, but they show no wall before 10^5.

## Consequences

- No new runtime service is required for the current scale.
- CI must regenerate `exports/content-manifest.json` when content changes, or the
  fail-closed check stops the chain.
- Revisit at 10^6 entities, when `git status` or a full read pass exceeds 5 s, or when
  binary assets dominate clone time.
