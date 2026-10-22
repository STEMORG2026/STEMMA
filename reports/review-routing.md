# Review-Queue Routing — R7

- Source export: `sha256:df7943c4e08e53620f6169cce4b58f99b6371f362d1833b355d32fd5656944f9` (v2.2.0)
- Mechanism: **heuristic-worksheet-ordering** · predictive model: **False** · content effect: **order-only**
- Threshold: 200 decisions / 3 domains · observed 6 / 1 · activated: **False**

> The heuristic only orders work. It cannot accept, reject, or canonicalize anything.

## Pending entities (8)

| Rank | Entity | Domain | Score | Reasons |
|---|---|---|---|---|
| 1 | `stemma:phys.force` | physics | 0.843334 | centrality 0.016667; graph degree 1; 2 source ref(s) |
| 2 | `stemma:phys.newtons-second-law` | physics | 0.833334 | centrality 0.016667; 2 source ref(s) |
| 3 | `stemma:phys.mass` | physics | 0.621666 | centrality 0.030833; graph degree 1; 1 source ref(s) |
| 4 | `stemma:phys.conservation-energy` | physics | 0.583334 | centrality 0.016667; 1 source ref(s) |
| 5 | `stemma:phys.kilogram` | physics | 0.583334 | centrality 0.016667; 1 source ref(s) |
| 6 | `stemma:phys.length` | physics | 0.583334 | centrality 0.016667; 1 source ref(s) |
| 7 | `stemma:phys.second` | physics | 0.583334 | centrality 0.016667; 1 source ref(s) |
| 8 | `stemma:phys.time` | physics | 0.583334 | centrality 0.016667; 1 source ref(s) |

## Pending connections (1)

| Rank | Connection | Relation | Evidence | Score |
|---|---|---|---|---|
| 1 | `stemma:conn.000157` | mathematically_requires | 2 | 0.520000 |

## Invariants

- canonical remains per-object and human-only (L2)
- routing changes order only, never content
- no predictive model is activated below the threshold
