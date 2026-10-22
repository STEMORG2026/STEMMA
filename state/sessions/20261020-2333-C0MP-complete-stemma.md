# SESSION: 20261020-2333-C0MP-complete-stemma

**Agent:** `C0MP`
**Model:** `opencode/deepseek-v4.1-flash-free`
**Protocol:** `v1.2`
**Session ID:** `20261020-2333-C0MP-complete-stemma`
**Started:** 2026-10-20T23:33Z
**Status:** IN-PROGRESS
**Branch:** feat/bachelor-multidomain (based on `origin/main` f197bdc)
**Base commit:** 50566bf
**Task:** Complete STEMMA infrastructure (R6/R7/R8) and build verified bachelor-level canonical STEM content under the owner-delegated path in ADR-0060, licensed per ADR-0062 and schema 1.4.0.
**Files owned:** `scripts/*`, `tests/**`, `docs/*.md`, `docs/decisions/*.md`, `docs/docs-contract.yaml`, `exports/**`, `reports/*`, `state/**`, `PROGRESS.md`, `README.md`, `AGENTS.md`, `Makefile`, `.gitignore`, `explorer/**`, `schema/**`, `spec/**`, `content/**`, `connections/**`, `sources/**`, `.workbuddy-ai/**`

> Append-only event log. Registration metadata completed from reconnaissance in phase B.

---

## [START] — 2026-10-20T23:33Z

Owner instruction: "Complete STEMMA completely." This is interpreted as completing the
remaining **engineering** roadmap and making the repository internally consistent, not as
performing human-only review of canonical content (Tier 2, `spec/`, `content/`,
`connections/`, `sources/`). The agent will not approve, review, or canonicalize content on
the owner's behalf.

### Reconnaissance (phase B)

- Branch: `main`, clean except two state registrations left by an abandoned review session
  (`R6A1`, IN-PROGRESS, no phase B, no receipt, no work) and that session's file.
- HEAD: `50566bf`.
- Open PRs: #89 and #91 (dependabot, explorer dev dependencies).
- `python3 scripts/verify_all.py`: PASS (0 FAIL).
- `python3 tests/repo/test_state_tree.py`: **FAIL 19/22**, entirely caused by the orphaned
  `R6A1` registration (missing Branch/Base commit, no receipt). This is a state-record
  defect, not a repository defect.
- `release/` contains the R6 bundle machinery; `publication_gate.py` is OPEN
  (`stemma-urn-only`, `human:curator.001`).

### Planned work

1. Reconcile the orphaned `R6A1` registration (append-only closure note; no work existed).
2. R6 close-out: verify the projection/bundle chain is complete and record it.
3. R7: implement deterministic `exports/views/*`, the calibration report, and the
   review-queue routing heuristic gated at the owner-approved 200-decision / 3-domain
   threshold (routing remains disabled until the threshold is met).
4. R8: implement a reproducible 10^4-entity scale benchmark, a Merkle-root content-store
   design/prototype, and the migration decision record.
5. Documentation truth: bring `IMPLEMENTATION-STATUS.md`, `ROADMAP.md`, `README.md`,
   `PROGRESS.md`, and `state/` in line with reality.
6. Run the full verification chain and test suite; record every claim with its command.

> `.workbuddy-ai/**` is claimed only to satisfy the ownership footprint guard: it is a pre-existing untracked tool directory, not authored or modified by this session.


---

## [SCOPE AMENDMENT] — 2026-10-21

Owner directives since start: (1) the deliverable must be real bachelor-level content, not a
seed or a coverage map; (2) the agent may autonomously verify and canonicalize; (3) schema
upgrades are allowed when the content needs them ("might need to upgrade schema along the way
to include all the data sets"); (4) keep checking every 30 minutes for schema updates; (5) use
branch/PR workflow, pull before push, merge pending PRs first, fix pre-existing failures, and
clean merged branches.

The original "no Tier-2 content review" constraint is superseded by ADR-0060
(`owner_delegated` canonicalization), which forbids fabricating a human reviewer and requires
registered machine verification instead. Files owned now include content, connections,
sources, schema, and spec. Git workflow is recorded in `docs/GIT-WORKFLOW.md` and `AGENTS.md`.

### Work completed under the amendment

- ADR-0060 (delegated canonicalization), ADR-0061 (schema 1.4.0), ADR-0062 (OpenStax
  licensing/Tier C reference use).
- Schema 1.4.0, expanded subdomain vocabulary, registered `llm:qwen3.5-9b` and process agents,
  `ENF-STEMMA-HITL-005`.
- OpenStax inventory: 22 books, 323 key-terms pages, 11,443 rows, 9,492 unique terms; 17
  source records created from books with terms.
- First delegated tranche: 5 original physics definitions promoted through schema, source,
  no-verbatim, and quality checks. Validation now sees 14 entities.
- Merged PRs #91 and #89; branch fast-forwarded to `origin/main` f197bdc.

### Still open

- Bulk generation/promotion, schema watcher at 30-minute cadence, quantity/unit enrichment
  (currently falls back to concept), R8, docs truth pass, branch cleanup.


---

## [AMENDMENT UPDATE] — 2026-10-21

- R6, R7, R8 closed in `docs/ROADMAP.md` and `docs/IMPLEMENTATION-STATUS.md`.
- ADR-0058 (deterministic views + data-gated routing), ADR-0059 (sharded files + Merkle
  manifest through 10^5), and `docs/SCALE-READINESS.md` written and indexed.
- `scripts/content_store.py` manifest (148 files) wired into `verify_all.py`; tamper and
  determinism tests added.
- Three curated OpenStax tranches promoted through ADR-0060 checks (200 canonical entities,
  23 formal blocks); `reports/content-coverage.md` records measured coverage and names the five
  zero-term books plus engineering source gaps.
- Schema watcher running (PID 443761, 1800 s); no schema changes observed.
- Full pytest and `verify_all.py` green.
- Schema-change follow-through (DEC-016): `docs/MIGRATIONS.md` + `AGENTS.md` standing rule,
  `scripts/schema_field_coverage.py` adoption report, and `scripts/enrich_schema_fields.py`
  enrichment pass; schema 1.4.0 fields adopted on the corpus, `learning_objectives` excluded
  from canonical by ADR-0041/0047.

### Still open

- Continue resumable content tranches beyond the current curated core; source coverage for
  civil/electrical/chemical/mechanical engineering and the five zero-term books.
- Commit/push and branch cleanup await owner instruction.

---

## [PRODUCTION-AUDIT] — 2026-10-22

### Fixed

- `docs/README.md`: added the missing `GIT-WORKFLOW.md` and `SCALE-READINESS.md` index rows.
  `scripts/docs.py check` failed before this; CI's `verify-docs` job would have failed at
  `git diff --exit-code` after `docs.py sync`.
- `Makefile` `security` target: the condition ended in `| head -n 5`, which always exits 0,
  so the target always printed `FAIL: secret` and exited 1. Replaced with the same
  `grep -q .` check CI uses (and excluded `provenance`, matching CI).
- `content/physics/mechanics/instantaneous-velocity.md`: dropped `wd: Q11465`, which it
  shared with `velocity.md`. The adapter rejects ambiguous external ids; `test_real_export`
  failed. Added the entity to `NO_FAITHFUL_WIKIDATA_ITEM` in
  `tests/provenance/test_agents_external_ids.py` with the reason (no separate QID exists).
- `state/REGISTRY.md`: added `Makefile` to the session's `files_owned` and repaired the
  malformed `explorer/**` glob that broke the state-tree coverage check.

### Evidence (all green)

- `npm audit` (explorer): 0 vulnerabilities; no secrets found by pattern scan; `.env` absent,
  `.env.example` documented.
- Explorer: `npm ci` + typecheck + build + verify pass; bundle 1.44 MB / 387 kB gzip (warning
  only, code-splitting suggested).
- `make webapp-test`, `make security`, `make docs`, `make deterministic`, `make no-wall-clock`
  pass; MACP startup gate passes.
- `pytest tests/ -q`: 379 passed; `pytest adapters/python/tests`: 77 passed, 24 skipped.
- `verify_all.py`: exit 0, no artifact drift during the run; `gate_status.py` wrote a fresh
  all-green 6-gate block; `gate_status.py --check` passes.
- Regenerated after the content edit: JSON-LD, consumer exports, review manifest, status
  block, curation status, anomaly report, coverage reports, content manifest
  (`sha256:8f4b67f9ccb6…`, 268 files).

### Residual production risks

- **178 files uncommitted** (68 modified, 110 untracked); `HEAD == origin/main`, so none of
  the R6–R8 infrastructure or 260-entity corpus has run through CI or been reviewable.
  `macp_sync_gate.py` refuses a push until the state changes are committed.
- Python deps are range-pinned (`pyyaml>=6.0.3,<7.0`, `jsonschema>=4.26.0,<5.0`) with no
  lock file; explorer carries both `package-lock.json` and `pnpm-lock.yaml`.
- GitHub Actions use mutable tags (`actions/checkout@v7`, etc.), not SHA pins. Commit
  `e07a845` deliberately reverted the earlier SHA pinning ("merged without permission"), so
  this needs an owner decision, not an agent override.
- `release/R6-bundle-*` staging is 36 MB locally and correctly git-ignored; releases belong
  on GitHub Releases.

### Still open

- Commit/push the workstream and open a PR (awaiting explicit owner instruction).
- Continue content tranches and source selection for the five zero-term books and
  engineering breadth.

---

## [RECORD] — 2026-10-22T06:54Z — workstream committed

Commits since base `50566bf`: `898c13b`, `2e51790`, `e07a845`, `f197bdc`, `8a5be45`
(the workstream commit). The state commit that records this list is the branch tip and
is exempt from the commit enumeration by `macp_sync_gate.py`.

Changed paths (414) — complete enumeration required by `macp_sync_gate.py`:

```text
.gitignore
AGENTS.md
Makefile
PROGRESS.md
README.md
content/biology/general/3-utr.md
content/biology/general/5-cap.md
content/biology/general/5-utr.md
content/biology/general/7-methylguanosine-cap.md
content/biology/general/a-horizon.md
content/biology/general/abduction.md
content/biology/general/abiotic.md
content/biology/general/allele.md
content/biology/general/cell.md
content/biology/general/chromosome.md
content/biology/general/cytoplasm.md
content/biology/general/ecosystem.md
content/biology/general/enzyme.md
content/biology/general/evolution.md
content/biology/general/food-chain.md
content/biology/general/gene.md
content/biology/general/genotype.md
content/biology/general/homeostasis.md
content/biology/general/hormone.md
content/biology/general/meiosis.md
content/biology/general/metabolism.md
content/biology/general/mitosis.md
content/biology/general/mutation.md
content/biology/general/natural-selection.md
content/biology/general/neuron.md
content/biology/general/organelle.md
content/biology/general/phenotype.md
content/biology/general/population.md
content/biology/general/protein.md
content/biology/general/ribosome.md
content/biology/general/species.md
content/biology/general/transcription.md
content/biology/general/translation.md
content/biology/physiology/abdominal-aorta.md
content/biology/physiology/abdominopelvic-cavity.md
content/biology/physiology/abducens-nerve.md
content/biology/physiology/abduct.md
content/biology/physiology/abductor-digiti-minimi.md
content/biology/physiology/abductor-pollicis-brevis.md
content/biology/physiology/abductor-pollicis-longus.md
content/biology/physiology/abductor.md
content/biology/physiology/cell-membrane.md
content/biology/physiology/cellular-respiration.md
content/biology/physiology/immune-system.md
content/biology/physiology/mitochondrion.md
content/chemistry/general/accuracy.md
content/chemistry/general/acid-anhydride.md
content/chemistry/general/acid-base-indicator.md
content/chemistry/general/acid-base-reaction.md
content/chemistry/general/acid-ionization-constant-ka.md
content/chemistry/general/acid-ionization.md
content/chemistry/general/acid.md
content/chemistry/general/acidic.md
content/chemistry/general/actinide-series.md
content/chemistry/general/actinide.md
content/chemistry/general/activated-complex.md
content/chemistry/general/active-electrode.md
content/chemistry/general/actual-yield.md
content/chemistry/general/atom.md
content/chemistry/general/base.md
content/chemistry/general/buffer.md
content/chemistry/general/calorimetry.md
content/chemistry/general/catalyst.md
content/chemistry/general/chemical-equation.md
content/chemistry/general/covalent-bond.md
content/chemistry/general/electron.md
content/chemistry/general/electronegativity.md
content/chemistry/general/empirical-formula.md
content/chemistry/general/equilibrium.md
content/chemistry/general/ion.md
content/chemistry/general/ionic-bond.md
content/chemistry/general/limiting-reactant.md
content/chemistry/general/molar-mass.md
content/chemistry/general/mole.md
content/chemistry/general/molecular-formula.md
content/chemistry/general/molecule.md
content/chemistry/general/neutron.md
content/chemistry/general/organic-compound.md
content/chemistry/general/oxidation.md
content/chemistry/general/percent-yield.md
content/chemistry/general/periodic-table.md
content/chemistry/general/precipitate.md
content/chemistry/general/proton.md
content/chemistry/general/reduction.md
content/chemistry/general/solute.md
content/chemistry/general/solvent.md
content/chemistry/general/stoichiometry.md
content/earth-space/astronomy/absorption-spectrum.md
content/earth-space/astronomy/accelerate.md
content/earth-space/astronomy/accretion-disk.md
content/earth-space/astronomy/accretion.md
content/earth-space/astronomy/active-galactic-nuclei-agn.md
content/earth-space/astronomy/active-galaxies.md
content/earth-space/astronomy/active-region.md
content/earth-space/astronomy/adaptive-optics.md
content/earth-space/astronomy/amino-acids.md
content/earth-space/astronomy/angular-momentum.md
content/earth-space/astronomy/anthropic-principle.md
content/earth-space/astronomy/aperture.md
content/earth-space/astronomy/aphelion.md
content/earth-space/astronomy/apogee.md
content/earth-space/astronomy/apparent-brightness.md
content/earth-space/astronomy/apparent-magnitude.md
content/earth-space/astronomy/aurora.md
content/earth-space/astronomy/big-bang.md
content/earth-space/astronomy/black-hole.md
content/earth-space/astronomy/comet.md
content/earth-space/astronomy/cosmological-principle.md
content/earth-space/astronomy/dark-energy.md
content/earth-space/astronomy/dark-matter.md
content/earth-space/astronomy/doppler-effect.md
content/earth-space/astronomy/event-horizon.md
content/earth-space/astronomy/exoplanet.md
content/earth-space/astronomy/kuiper-belt.md
content/earth-space/astronomy/local-group.md
content/earth-space/astronomy/luminosity.md
content/earth-space/astronomy/main-sequence.md
content/earth-space/astronomy/meteor.md
content/earth-space/astronomy/nebula.md
content/earth-space/astronomy/neutron-star.md
content/earth-space/astronomy/oort-cloud.md
content/earth-space/astronomy/orbit.md
content/earth-space/astronomy/parsec.md
content/earth-space/astronomy/planet.md
content/earth-space/astronomy/pulsar.md
content/earth-space/astronomy/quasar.md
content/earth-space/astronomy/redshift.md
content/earth-space/astronomy/solar-flare.md
content/earth-space/astronomy/sunspot.md
content/earth-space/astronomy/telescope.md
content/earth-space/astronomy/terrestrial-planet.md
content/earth-space/astronomy/white-dwarf.md
content/engineering/computer/3-d-printing.md
content/engineering/computer/4-d-printing.md
content/engineering/computer/abstract-data-type-adt.md
content/engineering/computer/abstract-method.md
content/engineering/computer/abstract-model.md
content/engineering/computer/abstract-representation.md
content/engineering/computer/abstraction.md
content/engineering/computer/acceptance-testing.md
content/engineering/computer/access-control-list-acl.md
content/engineering/computer/access-control.md
content/engineering/computer/access-enforcement.md
content/engineering/computer/access-modifier.md
content/engineering/computer/accessibility-testing.md
content/engineering/computer/accessibility.md
content/engineering/computer/algorithm.md
content/engineering/computer/authentication.md
content/engineering/computer/authorization.md
content/engineering/computer/code-review.md
content/engineering/computer/compiler.md
content/engineering/computer/complexity.md
content/engineering/computer/concurrency.md
content/engineering/computer/continuous-integration.md
content/engineering/computer/data-structure.md
content/engineering/computer/debugging.md
content/engineering/computer/deployment.md
content/engineering/computer/design-pattern.md
content/engineering/computer/encapsulation.md
content/engineering/computer/encryption.md
content/engineering/computer/index.md
content/engineering/computer/inheritance.md
content/engineering/computer/interface.md
content/engineering/computer/machine-learning.md
content/engineering/computer/network.md
content/engineering/computer/neural-network.md
content/engineering/computer/operating-system.md
content/engineering/computer/polymorphism.md
content/engineering/computer/refactoring.md
content/engineering/computer/software-architecture.md
content/engineering/computer/stack.md
content/engineering/computer/transaction.md
content/engineering/computer/unit-testing.md
content/engineering/computer/version-control.md
content/engineering/data-engineering/3d-visualization.md
content/engineering/data-engineering/normalization.md
content/math/algebra/algebraic-expression.md
content/math/algebra/polynomial.md
content/math/calculus/absolute-convergence.md
content/math/calculus/absolute-error.md
content/math/calculus/absolute-extremum.md
content/math/calculus/absolute-maximum.md
content/math/calculus/absolute-minimum.md
content/math/calculus/absolute-value-function.md
content/math/calculus/acceleration-vector.md
content/math/calculus/acceleration.md
content/math/calculus/algebraic-function.md
content/math/calculus/arithmetic-sequence.md
content/math/calculus/conic-section.md
content/math/calculus/derivative.md
content/math/calculus/differential-equation.md
content/math/calculus/domain.md
content/math/calculus/exponential-growth.md
content/math/calculus/function.md
content/math/calculus/geometric-sequence.md
content/math/calculus/limit.md
content/math/calculus/logarithmic-function.md
content/math/calculus/range.md
content/math/calculus/rational-function.md
content/math/calculus/sequence.md
content/math/calculus/vector.md
content/math/precalculus/absolute-value-equation.md
content/math/precalculus/absolute-value-inequality.md
content/math/precalculus/addition-method.md
content/math/precalculus/addition-principle.md
content/math/precalculus/adjacent-side.md
content/math/precalculus/binomial-theorem.md
content/math/precalculus/combination.md
content/math/precalculus/complex-number.md
content/math/precalculus/ellipse.md
content/math/precalculus/hyperbola.md
content/math/precalculus/logarithm.md
content/math/precalculus/matrix.md
content/math/precalculus/parabola.md
content/math/precalculus/permutation.md
content/math/precalculus/polar-coordinates.md
content/math/precalculus/probability.md
content/math/precalculus/relation.md
content/math/precalculus/series.md
content/math/statistics-probability/mean.md
content/math/statistics-probability/variance.md
content/physics/electricity-magnetism/ac-current.md
content/physics/electricity-magnetism/ac-voltage.md
content/physics/electricity-magnetism/alternating-current-ac.md
content/physics/electricity-magnetism/alternating-current.md
content/physics/electricity-magnetism/electric-charge.md
content/physics/electricity-magnetism/electric-current.md
content/physics/electricity-magnetism/electric-field.md
content/physics/electricity-magnetism/electric-potential.md
content/physics/electricity-magnetism/electric-power.md
content/physics/electricity-magnetism/magnetic-field.md
content/physics/electricity-magnetism/voltage.md
content/physics/measurement-units/kilogram.md
content/physics/measurement-units/length.md
content/physics/measurement-units/mass.md
content/physics/measurement-units/metre.md
content/physics/measurement-units/second.md
content/physics/measurement-units/time.md
content/physics/mechanics/action-at-a-distance-force.md
content/physics/mechanics/angle-of-rotation.md
content/physics/mechanics/angular-acceleration.md
content/physics/mechanics/angular-velocity.md
content/physics/mechanics/center-of-mass.md
content/physics/mechanics/conservation-energy.md
content/physics/mechanics/elastic-collision.md
content/physics/mechanics/energy.md
content/physics/mechanics/force.md
content/physics/mechanics/friction.md
content/physics/mechanics/inelastic-collision.md
content/physics/mechanics/instantaneous-velocity.md
content/physics/mechanics/kinetic-energy.md
content/physics/mechanics/momentum.md
content/physics/mechanics/newtons-second-law.md
content/physics/mechanics/potential-energy.md
content/physics/mechanics/simple-harmonic-motion.md
content/physics/mechanics/torque.md
content/physics/mechanics/velocity.md
content/physics/mechanics/work.md
content/physics/thermal-physics/absolute-pressure.md
content/physics/thermal-physics/absolute-temperature-scale.md
content/physics/thermal-physics/absolute-zero.md
content/physics/thermal-physics/absorber.md
content/physics/thermal-physics/entropy.md
content/physics/thermal-physics/first-law-thermodynamics.md
content/physics/thermal-physics/heat.md
content/physics/thermal-physics/pressure.md
content/physics/thermal-physics/second-law-thermodynamics.md
content/physics/thermal-physics/temperature.md
docs/GIT-WORKFLOW.md
docs/IMPLEMENTATION-STATUS.md
docs/MIGRATIONS.md
docs/README.md
docs/ROADMAP.md
docs/SCALE-READINESS.md
docs/decisions/0058-deterministic-views-and-review-routing.md
docs/decisions/0059-scale-readiness-sharded-files.md
docs/decisions/0060-owner-delegated-content-canonicalization.md
docs/decisions/0061-schema-1.4-multidomain-coverage.md
docs/decisions/0062-open-content-acquisition-and-licensing.md
docs/decisions/README.md
docs/decisions/r6-identifier-base.md
docs/docs-contract.yaml
explorer/package-lock.json
explorer/package.json
explorer/pnpm-lock.yaml
exports/consumers/general/knowledge.general.json
exports/consumers/learninghub/knowledge.learninghub.json
exports/consumers/professor-j/knowledge.professor-j.json
exports/consumers/stemma-explorer/knowledge.stemma-explorer.json
exports/content-manifest.json
exports/knowledge.ai-rag.json
exports/knowledge.all.json
exports/knowledge.canonical.json
exports/knowledge.connections-only.json
exports/knowledge.domain-biology.json
exports/knowledge.domain-chemistry.json
exports/knowledge.domain-earth-space.json
exports/knowledge.domain-engineering.json
exports/knowledge.domain-mathematics.json
exports/knowledge.domain-physics.json
exports/knowledge.educational.json
exports/knowledge.entities-only.json
exports/knowledge.extended.json
exports/knowledge.json
exports/knowledge.jsonld
exports/knowledge.proposed.json
exports/knowledge.rejected.json
exports/knowledge.reviewed.json
exports/knowledge.status-canonical.json
exports/knowledge.status-draft.json
exports/knowledge.trusted.json
exports/knowledge.type-concept.json
exports/knowledge.type-constant.json
exports/knowledge.type-equation.json
exports/knowledge.type-function.json
exports/knowledge.type-instrument.json
exports/knowledge.type-law.json
exports/knowledge.type-material.json
exports/knowledge.type-model.json
exports/knowledge.type-phenomenon.json
exports/knowledge.type-principle.json
exports/knowledge.type-process.json
exports/knowledge.type-quantity.json
exports/knowledge.type-structure.json
exports/knowledge.type-system.json
exports/knowledge.type-technique.json
exports/knowledge.type-theorem.json
exports/knowledge.type-unit.json
exports/views/centrality.json
exports/views/changelog.json
exports/views/formulations.json
exports/views/index.json
exports/views/misconceptions.json
exports/views/prerequisites.json
reports/calibration.json
reports/calibration.md
reports/content-coverage.json
reports/content-coverage.md
reports/curation-status.json
reports/curation-status.md
reports/dependency-review-campaign/batch-01.md
reports/integrity-anomalies.json
reports/integrity-anomalies.md
reports/review-routing.json
reports/review-routing.md
reports/scale-benchmark-100k.json
reports/scale-benchmark-100k.md
reports/scale-benchmark.json
reports/scale-benchmark.md
reports/schema-field-coverage.json
reports/schema-field-coverage.md
reports/validation-report.json
schema/VERSION.yaml
schema/agent-registry.yaml
schema/concept.schema.json
schema/vocabularies/subdomains.yaml
scripts/calibration_report.py
scripts/content_store.py
scripts/coverage_report.py
scripts/enrich_schema_fields.py
scripts/export_views.py
scripts/generate_openstax_content.py
scripts/hitl_check.py
scripts/import_openstax_sources.py
scripts/openstax_inventory.py
scripts/promote_delegated.py
scripts/review_data.py
scripts/review_router.py
scripts/scale_benchmark.py
scripts/schema_field_coverage.py
scripts/schema_watch.py
scripts/startup_receipt.py
scripts/validate.py
scripts/verify_all.py
scripts/verify_strong.py
sources/src.openstax-algebra-and-trigonometry-2e.yaml
sources/src.openstax-anatomy-and-physiology-2e.yaml
sources/src.openstax-astronomy-2e.yaml
sources/src.openstax-biology-2e.yaml
sources/src.openstax-calculus-volume-1.yaml
sources/src.openstax-calculus-volume-2.yaml
sources/src.openstax-calculus-volume-3.yaml
sources/src.openstax-chemistry-2e.yaml
sources/src.openstax-college-algebra-2e.yaml
sources/src.openstax-introduction-computer-science.yaml
sources/src.openstax-introductory-statistics-2e.yaml
sources/src.openstax-physics.yaml
sources/src.openstax-precalculus-2e.yaml
sources/src.openstax-principles-data-science.yaml
sources/src.openstax-university-physics-volume-1.yaml
sources/src.openstax-university-physics-volume-2.yaml
sources/src.openstax-university-physics-volume-3.yaml
spec/machine-readable/enforcement_rules.yaml
spec/machine-readable/review_manifest.json
state/BLOCKERS.md
state/DASHBOARD.md
state/DECISIONS.md
state/INDEX.md
state/REGISTRY.md
state/SCHEMA-WATCH.md
state/content-inventory.json
state/plans/agent-C0MP-complete-stemma.md
state/sessions/20261002-0534-R6A1-protocol-enforcement-review.md
state/sessions/20261020-2333-C0MP-complete-stemma.md
state/verification.json
tests/content/test_openstax_pipeline.py
tests/provenance/test_agents_external_ids.py
tests/versioning/test_content_store.py
tests/versioning/test_release_bundle.py
```

### [FIX] — push-blocker in the independence guard — 2026-10-22T07:09Z

- `tests/repo/test_independence.py`: narrowed the "dead quick-start target" pattern from
  `(content/physics/mechanics/|docs/)force.md` to `docs/force.md`. The canonical entity
  `content/physics/mechanics/force.md` has existed since `121af07`, so the manifest and this
  session record legitimately name it; the old guard would have blocked every future push.
