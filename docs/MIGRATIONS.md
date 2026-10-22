# MIGRATIONS (BEGINNING, NO LEGACY)

**Status:** Beginning, no legacy. Old migrations archived to archive/old-design/.

## Standing rule — a schema change is not done until entities adopt it

A schema bump is only half the change. The schemas describe the *current* shape of a
canonical record, so when a new field is added or promoted, existing entities must be
updated to use it where it applies. Leaving the corpus validating as "old shape with new
fields unused" is treated as an unfinished migration, not a passing one.

Follow this sequence on every `schema_version` bump:

1. **ADR + version bump.** Record the change (ADR) and bump `schema_version` in
   `schema/VERSION.yaml`; update the export version only if the consumer shape changes.
2. **Validator before content.** Update the validators so the new field is checked, then
   run `python3 scripts/validate.py`.
3. **Measure adoption.** Run `python3 scripts/schema_field_coverage.py`; it reports how
   many entities carry each tracked field, per domain. The adoption delta is the
   migration's real progress.
4. **Sync the entities.** Enrich the existing canonical entities with the new fields
   where they apply (`scripts/enrich_schema_fields.py` for the descriptive 1.4.0 fields;
   add dimensional/`datasets` fields by hand or with a dedicated pass). Do it in
   resumable batches with a cache, never fabricate values, and keep the machine-checked
   delegation provenance from ADR-0060.
5. **Re-verify.** `validate.py` → `export_jsonld.py` → `export_consumers.py --all` →
   `review_manifest.py` → `status_truth.py --write` → `content_store.py --write` →
   `pytest` → `verify_all.py`, and re-run `schema_field_coverage.py`.
6. **Watch for drift.** `scripts/schema_watch.py --loop --interval 1800` checks the
   schema and inventory every 30 minutes and records changes; a detected change is the
   trigger to run steps 2–5 again.

Optional fields with no applicable value stay absent; adoption is measured, not
mandated per entity. What is mandated is that the corpus is re-examined after every
bump instead of silently staying on the previous shape.

### Canonical vs consumer fields — not every schema field goes in canonical

A new schema field must be classified before it is adopted. Some describe the
knowledge itself (`level`, `formal`, `applications`, `limitations`,
`same_dimensional_quantities`, `datasets`) and belong in canonical entities.
Others describe how a *consumer* uses the knowledge and must stay out of canonical
content. The standing example is `learning_objectives`, added by schema 1.4.0 but
forbidden in canonical entities by ADR-0041 (minimal entity profile) and ADR-0047,
and mechanically enforced by `tests/curation/test_generality.py`
(`test_no_curriculum_grade_country_metadata_fields`). It is consumer/curriculum
metadata, so `scripts/enrich_schema_fields.py` deliberately does not write it and
`scripts/schema_field_coverage.py` reports it as consumer-only rather than as a
migration gap. When a future schema bump adds a field, state which side of this
line it falls on; if it is consumer-facing, exclude it from canonical adoption and
record the reason here.

## 2026-09-26 — version baseline for the consumer versioning policy

- **What:** records the versions in force when the policy in
  `docs/VERSIONING.md` ("Consumer versioning and release policy", ADR-0054
  Amendment 1) was written. From here on, every change to one of these gets
  its own entry in this file.
- **Baseline:** release version `3.0.0` (`./VERSION`, first tag
  `v3.0.0-rc1`); `export_version` 2.2.0 (ADR-0050); `schema_version` 1.3.0
  (H1, entry below); `relation_registry_version` 1.0.0 (reserved duplicates
  removed; `equivalent_to` / `misconception_of` per ADR-0048).
- **Consumers:** nothing to do.

## 2026-10-21 — schema 1.4.0: multidomain fields + delegated provenance (additive)

- **What:** `schema_version` 1.4.0 adds multidomain entity types, `level`,
  `learning_objectives`, `applications`, `limitations`, `formal`, `datasets`, and the
  `owner_delegated` provenance block (`review_mode`, `verification`, `delegation`).
- **Validator:** delegated records need a registered human SOLE_OWNER delegator, a
  registered process/LLM verifier, and at least two passing checks. Human-only promotion is
  unchanged and remains the default when `review_mode` is absent.
- **Licensing:** OpenStax content is Tier C (CC BY-NC-SA 4.0, except `physics` CC BY 4.0);
  only term inventory and factual verification are used, never prose (ADR-0062).
- **Migration path:** fields are optional, so no record is invalid; the corpus is synced
  anyway (see the standing rule above). `level` is now present on 100% of entities,
  `applications` on 100% of canonical entities, `limitations` where they apply, measured by
  `scripts/schema_field_coverage.py`. `learning_objectives` is intentionally NOT adopted in
  canonical content (ADR-0041/0047 + generality guard) and is reported as consumer-only.
- **Export version:** stays 2.2.0 (entity fields are additive; old readers ignore them).
- **Consumers:** re-export consumer bundles; schema_version is checked by the release gate.

## 2026-09-26 — release asset rename: `knowledge.canonical.json` → `connections.canonical.json`

- **What:** in GitHub Release bundles only, the review-aware *canonical
  connections* view is now published as `connections.canonical.json`
  (`manifest.files[*].kind: connections-view`). It has no entities and never
  loaded with `stemma_adapter validate`; the old name suggested a full export.
- **Rule:** in a release bundle, `knowledge.*.json` is reserved for loadable
  exports (`kind: export`) plus the `knowledge.hash.json` pointer;
  `build_release_bundle.py` refuses anything else.
- **Consumers:** want canonical entities? Use `knowledge.learninghub.json`-style
  consumer exports or filter `knowledge.json` by `status`. `v3.0.0-rc1` keeps
  the old name (tags are immutable); the rename applies from the next tag.
- **Unchanged:** `exports/knowledge.canonical.json` in the repo, `export_version`,
  `schema_version`.

## 2026-09-26 — schema 1.3.0: provenance.drafted_by (H1, additive)

- **What:** `concept.schema.json` provenance gains optional `drafted_by`
  (`llm:*` / `process:*`). Model: a machine may draft, a human must write and
  approve, and both stay visible — `writer: human:*` (responsible author),
  `drafted_by: llm:…|process:…` (origin), `ai_drafted`, `reviewer: human:*`.
- **Validator:** `validate.py` now resolves entity `writer`/`reviewer`/`drafted_by`
  in `schema/agent-registry.yaml` (they were free strings); reviewer must be
  human, drafted_by a machine agent.
- **Migration path:** none required — the field is optional and all existing
  entities validate unchanged. Existing direct-authored entities keep
  `writer: llm:coding-agent.001` + `reviewer: human:curator.001` (ADR-0043); they
  are not rewritten.
- **Exports:** `schema_version` 1.3.0; `export_version` stays 2.2.0 (entity
  provenance is an open object in `export.schema.json`; old readers ignore the
  new member). Subset exports now carry `content_hash` instead of a wall-clock
  `generated_at`, and are regenerated by `verify_all.py` (they had gone stale).

## 2026-09-21 — Beginning: physics-core v2 minimal with dual verification + governing laws

- **Tag:** ADR-0040/0041/0042/0043 · **Kind:** breaking? No, beginning, no old data
- **Changed:** New minimal design: every entity has governed_by, source_refs, writer, link, retrieved_at, source_kind, source; every connection evidence>=1; governing registry 23 laws; deterministic placement without LLM
- **Old data:** None — this is beginning, 0 entities before, 17 now
- **Consumer impact:** None — new beginning


## 2026-09-21 — Reset to Beginning Clean, PDF Primary with HITL, Evolvable Templates, model selector like DeepSeek harness (local + frontier models)

- **Changed:** Archived 74 entities + 150 connections to archive/beginning-74-entities/, reset content/physics/ to 1 entity (metre) via PDF primary ingestion with HITL
- **Added:** PDF primary ingestion with HITL before canonical — PDF (SI Brochure 9th ed., HRW 12th ed., custom) → ingest.py deterministic → AI draft to markdown preview → human explicitly edits markdown → stage → validate (including hitl_check.py) → review_entity accept/canonicalize
- **Added:** Deterministic scales — uses schema/template-registry.yaml with regex rules + exact SI constants c,h,ΔνCs,e,k,N_A,K_cd, no LLM, no cost, scales to any domain (physics, chemistry, biology, math), evolvable without code change via `python3 scripts/evolvable_template.py --evolve`
- **Added:** LLM fallback only when PDF missing exact SI — frontier models DeepSeek R1/V3 free, Claude 3.5 Sonnet/Opus, GPT-4o/o1, Gemini 2.5 Pro/2.0 Flash free, Llama 3.3 70B free, Qwen, Nemotron via OpenRouter/NVIDIA NIM, selector like DeepSeek harness (search, categories Frontier/Reasoning/Free/Custom, 25 models, custom model input), even LLM requires HITL
- **Added:** scripts/hitl_check.py (enforces human edited markdown before canonical), scripts/pdf_ingest_primary.py (primary feeder), scripts/evolvable_template.py (deterministic extraction + evolvable), schema/template-registry.yaml (evolvable, domain-agnostic)
- **Updated:** webapp/ with model selector like DeepSeek harness (local + frontier models) with search, categories, frontier models, custom input), deterministic draft (no LLM, scales) + AI draft with frontier buttons, markdown preview textarea + checklist + Save human edit HITL
- **Updated:** All docs (ARCHITECTURE, CONSUMERS, DOMAIN-MODEL, GOVERNANCE, VISION, README, CURATION-PROTOCOL, SCHEMA-SPECIFICATION, METADATA-SPECIFICATION, STANDARDS, TESTING, VERSIONING, IMPLEMENTATION-STATUS, ROADMAP, PIPELINES, AGENT, INGESTION-PRIMARY) to reflect 1 entity via HITL, deterministic scales, evolvable templates, frontier selector
- **Verification:** validate.py OK 1, physics_core_profile_check OK 0, physics_governing_check OK 0, hitl_check OK HITL satisfied, verify_all OK — beginning clean, HITL enforced, PDF primary deterministic scales, evolvable, frontier
