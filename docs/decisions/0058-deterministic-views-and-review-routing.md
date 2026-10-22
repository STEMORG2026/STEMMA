# ADR-0058: Deterministic Views and Data-Gated Review Routing

Status: Decided — 2026-10-21
Date: 2026-10-21
Decided by: Sajan (sole owner), through the R7 work order
Relates to: ADR-0022 (determinism), ADR-0054 (consumer surface), ADR-0060
(delegated canonicalization)

## Context

Consumers need stable derived views without reading the full export, and reviewers need
queue ordering that is explainable. Two failure modes are unacceptable:

1. A view becomes a second source of truth. It must carry the export's `content_hash` and
   regenerate byte-identically.
2. A routing heuristic is mistaken for a trained model. The corpus does not yet have enough
   labelled decisions to justify prediction.

## Decision

1. `scripts/export_views.py` writes five deterministic views under `exports/views/`:
   prerequisites, misconceptions, formulations, centrality, and changelog, plus an index.
   Every view declares the source `content_hash`; no wall-clock timestamps. `--check`
   verifies freshness.
2. `scripts/review_router.py` emits a deterministic worksheet order with explicit features
   (`mechanism: heuristic-worksheet-ordering`, `predictive: false`).
3. Routing activation requires **at least 200 measured review decisions across at least 3
   domains**. `reports/calibration.{json,md}` computes the measured counts; below the
   threshold the routing block stays `activated: false` and states why.
4. Calibration never fabricates decisions. It counts real `review_history[]` entries and
   campaign worksheet rows.

## Consequences

- Views can be regenerated from `exports/knowledge.json` and checked in CI.
- Reviewers get a stable order without a model making quality claims.
- Once the threshold is met, a later ADR may add a predictive model; that is explicitly out
  of scope here.
