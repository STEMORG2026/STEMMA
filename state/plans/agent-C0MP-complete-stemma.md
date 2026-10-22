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

## Resume point — paused 2026-10-22T11:16Z

**Where we stopped.** PR #92 (R6–R8 + 260-entity corpus) squash-merged as `0df9032`; PR
#93 (30 biology entities) squash-merged as `a0edd12`; both branches deleted and `main`
is clean. Corpus: **298 entities (290 reviewed, 8 physics drafts)**, 2 connections, 20
sources; biology is 75 of 5,548 inventory terms (**1.35%**). The generated gate block was
last measured at 2026-10-22T10:59Z on `0df9032` (6/6 green); PR #93 merged after that
measurement, so regenerate it on resume.

**First actions on resume (in order).**
1. `git checkout main && git pull --ff-only`; create `feat/coverage-batch-3`.
2. Add the squash SHA of the docs/pause-point PR that carries this handoff to the session
   log's commit enumeration (`git log --oneline --grep 'pause point'`). `macp_sync_gate.py`
   refuses a push when a non-tip commit since `Base commit 50566bf` is unlisted; the tip
   is exempt. `0df9032`, `a0edd12`, and `e6a0baf` are already listed.
3. Refresh STEP 8 if a new gate block is generated: `python3 scripts/startup_receipt.py`,
   then `python3 scripts/gate_status.py` (all six gates, ~5+ min).
4. Run one content tranche end to end (below), then the regeneration chain, tests, docs,
   explorer, `gate_status.py`, commit, push, PR.

**Planned tranche order.**
1. **Chemistry 30** (`--domain chemistry --limit 30`): bond energy, lone pair, resonance,
   intermolecular force, oxidation number, electrolysis, activation energy (Ea), addition
   reaction, adhesive force, alcohol, aldehyde, alkali metal, alkaline battery, alkaline
   earth metal, alkane, alkene, alkyl group, alkyne, allotropes, alloy, + the next 10.
2. **Mathematics 30**: parametric equations, standard deviation, normal and binomial
   distributions, conditional probability, expected value, alternating series, …
3. **Earth-space 30**: planetary nebula, parallax, apparent solar time, asteroid, …
4. **Engineering 30**: tree, heapsort, binary search, hash table, linked list, array list,
   recursion, memory, …
5. **Physics:** promote the 8 remaining drafts (`length`, `mass`, `second`, `time`,
   `kilogram`, `force`, `newton's-second-law`, `conservation-energy`), then the next 22
   priority terms (acceleration due to gravity, average acceleration, …).
6. **Zero-term books (parser work, not generation):** `additive-manufacturing-essentials`,
   `college-physics-2e`, `introduction-python-programming`, `microbiology`,
   `organic-chemistry` yield no inventory terms. Debug `scripts/openstax_inventory.py`
   for those slugs; microbiology and organic chemistry are the largest blocked subdomains.
7. **Remaining schema field:** `datasets` is 0/298; it needs real dataset sources, not
   fabricated links.
8. **Engineering breadth:** civil/electrical/chemical/mechanical sources beyond OpenStax
   (DOE/NASA/NIST/USACE) under the ADR-0062 license gate.

**Operational notes (learned in this batch).**
- Generation uses Ollama `qwen3.5:9b`; `state/cache/llm-definitions.json` has 302 entries.
  Run `generate_openstax_content.py --domain X --limit N`, then
  `promote_delegated.py --domain X --limit N`. Expect failures: the biology batch needed
  14 of 30 definitions rewritten for length, formulaic wording, or 8-word verbatim overlap;
  `nucleus` initially described the atomic nucleus and was corrected to the cell organelle.
- **Never run `verify_all.py` and `pytest` concurrently.** `verify_all.py` regenerates
  `review_manifest.json` in write mode and pytest's mutation tests temporarily edit
  `content/physics/mechanics/force.md` / `metre.md`; the overlap produced a stale manifest
  hash (895b… vs 871e…). Re-running `review_manifest.py` after pytest fixes it.
- After any content edit, run in order: `validate.py`, `export_jsonld.py`,
  `export_consumers.py --all`, `review_manifest.py`, `status_truth.py --write`,
  `curation_status.py`, `integrity_anomalies.py`, `coverage_report.py`,
  `schema_field_coverage.py`, `content_store.py --write`.
- `review_manifest.py --check` must pass before commit (291 reviewed records after this
  batch).
- Baselines: 379 pytest passed; adapters 77 passed / 24 skipped; explorer
  typecheck/build/verify/grounded-chat pass; docs check pass; `gate_status.py` 6/6 green.
- The schema watcher is not running; restart with
  `python3 scripts/schema_watch.py --loop --interval 1800` (its runtime files are ignored).
- Accepted branch prefixes: `feat|fix|docs|chore|ci|task|refactor|test|dependabot|arena`.
- Main history is squash merges; delete merged branches and prune after each merge.
