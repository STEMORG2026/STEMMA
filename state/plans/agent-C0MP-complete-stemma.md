# PLAN: Complete the roadmap and build bachelor-level multidisciplinary content

**Owner:** `C0MP`
**Status:** ACTIVE — R6/R7/R8 COMPLETE; content tranches continuing (updated 2026-10-21)
**Created:** 2026-10-20T23:45Z
**Session:** `20261020-2333-C0MP-complete-stemma`

## Goal

Finish the remaining engineering roadmap (R6 close-out, R7 views/routing, R8 scale) **and**
build canonical content up to bachelor level across physics, chemistry, biology, astronomy,
mathematics, and civil/electrical/chemical/mechanical/computer engineering. The owner has
authorized owner-delegated machine canonicalization (ADR-0060), so content is not blocked on
per-item human review; it is blocked on source verification, schema validation, licensing, and
recorded machine checks.

The earlier "engine only, no Tier-2" scope is superseded by this amendment.

## In scope

- **R6 close-out:** confirm the projection/release chain is green and mark R6 complete in
  the roadmap/status documents (the identifier decision is already recorded).
- **R7:** deterministic consumer views under `exports/views/`; a calibration report computed
  from real review data (never fabricated); a review-queue router that only reorders work
  and never changes content. Record the ≥200-labeled-decisions / ≥3-domain activation
  threshold in an ADR, and make the router refuse activation until the threshold is met.
- **R8:** a reproducible scale benchmark at 10^4 synthetic entities, a content-addressed
  store design with Merkle roots plus a working manifest prototype, and an ADR recording
  the 10^5 migration decision (stay on sharded files + LFS for now).
- **Truth pass:** update stale counts/status in `docs/IMPLEMENTATION-STATUS.md`,
  `docs/ROADMAP.md`, `README.md`, `PROGRESS.md`, `state/DASHBOARD.md`, and the stale corpus
  line in `docs/decisions/r6-identifier-base.md` (Tier-1 document, not an ADR).
- **Gates:** add tests for every new generator; wire checks into `verify_all.py` only where
  they are deterministic and cheap; rerun the full chain and the startup receipt.
- **Content inventory:** `scripts/openstax_inventory.py` produces a source-licensed term
  inventory (9,492 unique terms across 22 books on the first full run) without copying Tier C
  prose. This is the coverage map for generation.
- **Schema evolution:** schema 1.4.0 adds multidomain entity types, `level`, `formal`,
  `datasets`, and delegated provenance (ADR-0061); further schema bumps are allowed when a
  field is genuinely needed by the content, not to avoid modeling.
- **Canonical content:** generate original definitions and structured records for the
  inventory, verify them, and canonicalize under ADR-0060. Start with the highest-value
  concepts and keep expanding; report measured coverage by domain and subdomain.
- **Engineering breadth:** OpenStax covers computer/software/data and mechanical
  (additive) foundations; civil/electrical/chemical/mechanical breadth uses public-domain
  DOE/NASA/NIST/USACE material and other Tier A/B sources with the same license gate.

## Out of scope

- Fabricating human reviewers, citations, or verification results.
- Copying Tier C (NC-SA/SA) prose into canonical content.
- Training or shipping a predictive routing model (the data threshold is not met).
- Bypassing CI, branch protection, or the licensing gate.
- Pushing without pulling/merging the current `origin/main` first (owner directive).

## Branch and PR workflow

Every work item starts on a branch from current `main`; pending PRs are merged first; before
pushing, fetch and merge/rebase `origin/main`; after merge, delete merged branches and prune.
Record merges, cleanup, and pre-existing failures in the session log. See
`docs/GIT-WORKFLOW.md` and the "Git and PR Workflow" section of `AGENTS.md`.

## Approach

1. **Measure first.** Derive review-decision counts from `review_history[]` and the
   campaign worksheets; write `reports/calibration.{md,json}` from those numbers only.
2. **Views.** `scripts/export_views.py` reads the export + relation registry and writes five
   deterministic JSON views (prerequisites, misconceptions, formulations, centrality,
   changelog) plus an index carrying the source `content_hash`. No timestamps.
3. **Routing.** `scripts/review_router.py` emits a deterministic worksheet order with
   explicit features and a `routing_activation` block. It computes the decision/domain
   counts and keeps `activated: false` until the ADR threshold is met.
4. **Scale.** `scripts/scale_benchmark.py` builds a throwaway git repo with 10^4 entity
   files, measures `git add`, `git status`, `git diff`, and a validation-shaped read pass,
   and writes `reports/scale-benchmark.{md,json}`. `scripts/content_store.py` computes
   per-file hashes and a deterministic Merkle root over the canonical tree, writing
   `exports/content-manifest.json`.
5. **Acquire coverage.** Build an inventory from OpenStax TOCs/key-terms (Tier C reference:
   term lists and fact checks only). Record title, authors, ISBN, URL, and actual license per
   book. Do not copy glossary prose (ADR-0062).
6. **Generate and verify.** For each term, write an original definition in batches, attach
   the source record and locator, assign domain/subdomain/type/level, and run schema, source,
   duplicate, and no-verbatim checks. Two passing machine checks plus the owner delegation
   block unlock canonical status (ADR-0060).
7. **Scale the corpus.** Process in resumable tranches (domain/subdomain/limit), record
   counts by domain and failures, and keep a coverage report. Engineering sources beyond
   OpenStax use public-domain DOE/NASA/NIST/USACE material.
8. **Decide and document.** ADR-0058 (R7 views/routing), ADR-0059 (R8 scale/migration),
   ADR-0060/0061/0062 (content authority, schema, licensing), `docs/SCALE-READINESS.md`,
   and roadmap/status reconciliation.
9. **Verify.** `pytest`, `verify_all.py`, docs check, and a fresh startup receipt.

## Outcome so far (2026-10-21)

- R6, R7, and R8 complete; ADR-0058/0059 written; `docs/SCALE-READINESS.md` published.
- Content manifest wired into `verify_all.py`; delegated promotion and 30-minute schema watcher
  operating.
- Three curated OpenStax tranches promoted (200 canonical core concepts and 23 formal
  equation/statement blocks); measured coverage and source gaps in
  `reports/content-coverage.md`.
- Full suite and `verify_all.py` green.
- Schema-change follow-through (DEC-016): a standing rule plus enrichment tooling. Schema
  1.4.0 fields are now adopted (`level` 100%, `applications` 100% of canonical entities,
  `limitations` where applicable); `learning_objectives` classified consumer-only and kept
  out of canonical content; adoption measured by `scripts/schema_field_coverage.py`.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Fabricating calibration quality from n≈3 | Report the measured n, domains, and a "below threshold — not representative" verdict. |
| A view becoming a second source of truth | Every view declares `source_content_hash`; tests assert it matches `exports/knowledge.json`. |
| Router mistaken for a model | Output is explicitly `mechanism: heuristic-worksheet-ordering`, `predictive: false`, `activated: false`. |
| Benchmark polluting the repo or being flaky | Runs in `tempfile.mkdtemp()`, fixed file sizes, records medians, no network, no repo writes. |
| Merkle manifest drifting | Deterministic sort, no timestamps, `--check` mode, test pins root stability and tamper detection. |
| Stale docs reappearing | Counts in docs are replaced by pointers or generated by `status_truth.py`; the truth pass removes hardcoded counts where possible. |

## Rollback

Schema 1.4.0 and delegated canonicalization are additive; existing entities validate
unchanged. Content tranches can be removed by deleting their generated files and regenerating
the export. Revert the specific schema/validator/ADR files to restore the human-only path.
No existing canonical record is overwritten by the import pipeline.

## Success criteria

- `exports/views/` contains five deterministic views + index; `--check` is clean.
- Calibration report states measured values and refuses to claim quality below threshold.
- Router activates only when ≥200 decisions across ≥3 domains; otherwise says why.
- Scale benchmark completes at 10^4 with recorded timings; Merkle manifest verifies.
- OpenStax inventory covers all 22 selected books and reports license tier per book.
- Content tranches validate; canonical entities carry source refs, delegation, and ≥2
  passing machine checks; no Tier C prose is copied.
- Coverage report states measured entity counts per domain/subdomain and names gaps.
- `pytest`, `verify_all.py`, docs check, state-tree, and startup receipt all pass.
- Pending PRs merged, branches cleaned, and `origin/main` merged before any push.
