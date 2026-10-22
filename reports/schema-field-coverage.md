# SCHEMA FIELD COVERAGE

Measured across **268** entity files. Optional 1.4.0 fields are adopted
incrementally; this report exists so a schema bump is not considered finished
while entities still carry only the old shape.

| Field | Adopted | Percent |
|---|---:|---:|
| `level` | 268 | 100.0% |
| `formal` | 46 | 17.2% |
| `examples` | 137 | 51.1% |
| `applications` | 260 | 97.0% |
| `limitations` | 72 | 26.9% |
| `datasets` | 0 | 0.0% |
| `same_dimensional_quantities` | 268 | 100.0% |

## Consumer-only schema fields (intentionally not canonical)

- `learning_objectives` — present in 0 files; not canonical (ADR-0041/0047)

## By domain

| Domain | Entities | `level` | `formal` | `examples` | `applications` | `limitations` | `datasets` | `same_dimensional_quantities` |
|---|---|---|---|---|---|---|---|---|
| biology | 45 | 45 | 2 | 28 | 45 | 0 | 0 | 45 |
| chemistry | 42 | 42 | 9 | 20 | 42 | 10 | 0 | 42 |
| earth-space | 45 | 45 | 1 | 21 | 45 | 35 | 0 | 45 |
| engineering | 44 | 44 | 0 | 24 | 44 | 13 | 0 | 44 |
| mathematics | 45 | 45 | 17 | 25 | 45 | 0 | 0 | 45 |
| physics | 47 | 47 | 17 | 19 | 39 | 14 | 0 | 47 |
