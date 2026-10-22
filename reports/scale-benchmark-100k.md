# SCALE BENCHMARK

Dataset: **scale-100000** (100000 synthetic entities, 2 repeats for interactive checks).

## Timings

| Operation | Seconds |
|---|---:|
| `write_files` | 3.8959 |
| `git_add` | 3.6075 |
| `git_commit` | 0.3677 |
| `git_status_median` | 0.1336 |
| `edit_sample` | 0.0274 |
| `git_diff_stat_median` | 0.1032 |
| `validation_shaped_read_median` | 2.3032 |

## Derived

- Write throughput: **25667.8 files/s**
- Status throughput: **748671.7 files/s**
- Content size: **45750005 bytes** (457.5 bytes/entity)
- Records read in validation-shaped pass: **100000**

## Limits

- single local filesystem and git version; timings vary by machine
- synthetic entities are smaller than fully sourced records
- no export, JSON-LD, SHACL, or ZIP bundle step is measured

This benchmark is local and synthetic. It measures file/git mechanics, not
scientific quality or network-bound ingestion.
