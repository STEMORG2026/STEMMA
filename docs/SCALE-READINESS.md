# Scale Readiness

**Decision:** stay on sharded Markdown files in git through 10^5 entities, with Git LFS for
binary assets and a Merkle manifest for verification (ADR-0059).

## Measured limits

Run: `python3 scripts/scale_benchmark.py` (10,000 synthetic entities, 2026-10-21, local
filesystem). Supplemental 100,000-entity run: `reports/scale-benchmark-100k.json`.

| Operation | 10,000 | 100,000 |
|---|---:|---:|
| Write files | 0.25 s | 3.90 s |
| `git add` | — | 3.61 s |
| `git status` (median) | 0.066 s | 0.134 s |
| Edit 1% sample | — | 0.027 s |
| `git diff --stat` (median) | — | 0.103 s |
| Validation-shaped read (median) | 0.122 s | 2.30 s |

Timings vary by machine; synthetic records are smaller than fully sourced ones. The benchmark
does not measure export, JSON-LD, SHACL, or bundle construction.

## Verification

`exports/content-manifest.json` records every `content/**/*.md` file's SHA-256 and a
deterministic Merkle root. `python3 scripts/content_store.py --check` fails on a missing,
added, or changed file. The check is part of `verify_all.py`.

## Revisit triggers

Move to a database or object store only if one of these is measured:

- `git status` on a clean corpus exceeds 5 s.
- A full validation-shaped read exceeds 5 s.
- Clone time is dominated by binary assets even with LFS.
- The corpus reaches 10^6 entities.
- Cross-entity queries needed by the review workflow cannot be answered from the export and
  views within the same budget.

Until then, extra storage machinery is operational cost without evidence of need.
