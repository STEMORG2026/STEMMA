# Calibration Report — R7

- Source export: `sha256:df7943c4e08e53620f6169cce4b58f99b6371f362d1833b355d32fd5656944f9` (v2.2.0)
- Decision unit: review-state transition (from != to) or reviewed entity with provenance.reviewed_at
- Excluded: no-op transitions (reviewed -> reviewed) and unlabeled worksheet rows

## Current corpus (measured)

| Metric | Value |
|---|---|
| Labeled decisions | **6** |
| Distinct reviewed objects | 3 |
| Accepted transitions | 5 |
| Rejected transitions | 0 |
| Demotions | 1 |
| Accepted-transition rate (descriptive) | 0.8333 |
| Corrected with `correction_class` | 0 |
| Domains with decisions | **1** (physics) |

### By domain

| Domain | Decisions | Accepted | Rejected | Demoted |
|---|---|---|---|---|
| physics | 6 | 5 | 0 | 1 |

## Threshold (ADR-0058)

- Required: **200** labeled decisions across **3** domains
- Observed: 6 decisions across 1 domain(s)
- Decisions met: **False** · Domains met: **False** · Activated: **False**

**Verdict:** INSUFFICIENT — below the ADR-0058 activation threshold; accepted_transition_rate is descriptive, not a calibration

## Historical pilot (archived corpus)

Source: `reports/curation-pilot.md` — archived pilot corpus (not the current repository corpus).

| Metric | Value |
|---|---|
| Proposals | 36 |
| Curated accepted | 12 |
| Acceptance rate | 0.3333 |
| Auto-canonicalized | 0 |

## Limitations

- Accepted transitions include reviewed and canonical stages; they are not independent samples.
- The archived pilot belongs to a retired corpus and is shown as history, not current quality.
- No rejected-with-correction decision exists in the current corpus, so correction calibration is not measurable.
