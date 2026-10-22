# SCALE BENCHMARK

Dataset: **scale-10000** (10000 synthetic entities, 3 repeats for interactive checks).

## Timings

| Operation | Seconds |
|---|---:|
| `write_files` | 0.2498 |
| `git_add` | 0.2176 |
| `git_commit` | 0.0844 |
| `git_status_median` | 0.0657 |
| `edit_sample` | 0.0039 |
| `git_diff_stat_median` | 0.011 |
| `validation_shaped_read_median` | 0.122 |

## Derived

- Write throughput: **40036.9 files/s**
- Status throughput: **152260.7 files/s**
- Content size: **4545005 bytes** (454.5 bytes/entity)
- Records read in validation-shaped pass: **10000**

## Limits

- single local filesystem and git version; timings vary by machine
- synthetic entities are smaller than fully sourced records
- no export, JSON-LD, SHACL, or ZIP bundle step is measured

This benchmark is local and synthetic. It measures file/git mechanics, not
scientific quality or network-bound ingestion.
