#!/usr/bin/env python3
"""R7 — review-queue routing (heuristic worksheet ordering only).

What this is:
  A deterministic ordering of pending review work. It reads centrality, evidence
  coverage and structural neighbourhood, sorts the queue, and writes a worksheet.
  It NEVER edits a record, changes a review status, or decides acceptance.

What this is not:
  A predictive model. The architecture permits one only after >=200 labeled
  decisions across >=3 domains (ADR-0058). The activation block reports the
  measured counts and stays `activated: false` below that threshold.

Invariants (ADR-0058):
  - canonical remains per-object and human-only (L2);
  - routing changes order only, never content;
  - the order is reproducible from the derived export alone.

Usage:
  python3 scripts/review_router.py
  python3 scripts/review_router.py --check
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from atomic_write import write_text_atomic  # noqa: E402
import review_data  # noqa: E402

EXPORT_PATH = ROOT / "exports" / "knowledge.json"
EXTENDED_PATH = ROOT / "exports" / "knowledge.extended.json"
JSON_PATH = ROOT / "reports" / "review-routing.json"
MD_PATH = ROOT / "reports" / "review-routing.md"

WEIGHTS = {
    "pagerank": 2.0,
    "degree": 0.01,
    "source_refs": 0.25,
    "governed_by": 0.1,
    "definition": 0.1,
}


class RouterError(RuntimeError):
    pass


def _load(path: pathlib.Path) -> dict[str, Any]:
    if not path.exists():
        raise RouterError(f"missing {path.relative_to(ROOT)} — run the export chain first")
    return json.loads(path.read_text(encoding="utf-8"))


def _features(entity: dict[str, Any], score: dict[str, Any],
              states: dict[str, str]) -> dict[str, Any]:
    source_refs = len(entity.get("source_refs") or [])
    governed_by = len(entity.get("governed_by") or [])
    definition = entity.get("definition") or ""
    return {
        "pagerank": score.get("pagerank", 0.0),
        "degree": score.get("degree", 0),
        "source_refs": source_refs,
        "governed_by": governed_by,
        "definition_chars": len(definition),
        "has_definition": bool(definition.strip()),
        "review_status": states.get(entity["id"], entity.get("status")),
    }


def _priority(features: dict[str, Any]) -> float:
    return round(
        WEIGHTS["pagerank"] * features["pagerank"]
        + WEIGHTS["degree"] * features["degree"]
        + WEIGHTS["source_refs"] * features["source_refs"]
        + WEIGHTS["governed_by"] * features["governed_by"]
        + WEIGHTS["definition"] * (1.0 if features["has_definition"] else 0.0),
        6,
    )


def _reasons(features: dict[str, Any]) -> list[str]:
    out = []
    if features["pagerank"]:
        out.append(f"centrality {features['pagerank']:.6f}")
    if features["degree"]:
        out.append(f"graph degree {features['degree']}")
    if features["source_refs"]:
        out.append(f"{features['source_refs']} source ref(s)")
    if not features["has_definition"]:
        out.append("missing definition")
    return out or ["deterministic id order"]


def build() -> dict[str, Any]:
    export = _load(EXPORT_PATH)
    extended = _load(EXTENDED_PATH)
    if extended.get("content_hash") != export.get("content_hash"):
        raise RouterError("exports/knowledge.extended.json is stale relative to exports/knowledge.json")
    scores = (extended.get("derived") or {}).get("centrality", {}).get("all", {})
    states = {
        e["id"]: e.get("status") for e in export.get("entities", [])
    }

    pending_entities = [
        e for e in export.get("entities", [])
        if e.get("status") not in review_data.REVIEWED_STATUSES
    ]
    entity_queue = []
    for entity in pending_entities:
        features = _features(entity, scores.get(entity["id"], {}), states)
        entity_queue.append({
            "id": entity["id"],
            "name": entity.get("name"),
            "domain": entity.get("domain"),
            "type": entity.get("type"),
            "status": entity.get("status"),
            "score": _priority(features),
            "features": features,
            "reasons": _reasons(features),
        })
    entity_queue.sort(key=lambda row: (-row["score"], row["id"]))
    for rank, row in enumerate(entity_queue, start=1):
        row["rank"] = rank

    pending_connections = [
        c for c in export.get("connections", [])
        if ((c.get("assertion") or {}).get("review") or {}).get("status")
        not in review_data.REVIEWED_TARGETS
    ]
    connection_queue = []
    for conn in pending_connections:
        endpoint_degree = sum(
            (scores.get(conn.get("source"), {}) or {}).get("degree", 0)
            + (scores.get(conn.get("target"), {}) or {}).get("degree", 0)
            for _ in (0,)
        )
        connection_queue.append({
            "id": conn["id"],
            "relation": conn.get("relation"),
            "source": conn.get("source"),
            "target": conn.get("target"),
            "evidence_count": len(conn.get("evidence") or []),
            "endpoint_degree": endpoint_degree,
            "score": round(0.01 * endpoint_degree + 0.25 * len(conn.get("evidence") or []), 6),
        })
    connection_queue.sort(key=lambda row: (-row["score"], row["id"]))
    for rank, row in enumerate(connection_queue, start=1):
        row["rank"] = rank

    stats = review_data.decision_stats()
    return {
        "report_version": "1.0.0",
        "source_content_hash": export["content_hash"],
        "export_version": export["export_version"],
        "mechanism": "heuristic-worksheet-ordering",
        "predictive_model": False,
        "heuristic_active": True,
        "content_effect": "order-only",
        "weights": WEIGHTS,
        "activation": stats["threshold"],
        "observed": {
            "decisions": stats["decisions_total"],
            "domains": stats["domains_with_decisions"],
            "domain_list": stats["domains"],
        },
        "entity_queue": entity_queue,
        "connection_queue": connection_queue,
        "invariants": [
            "canonical remains per-object and human-only (L2)",
            "routing changes order only, never content",
            "no predictive model is activated below the threshold",
        ],
    }


def render_md(report: dict[str, Any]) -> str:
    activation = report["activation"]
    lines = [
        "# Review-Queue Routing — R7",
        "",
        f"- Source export: `{report['source_content_hash']}` (v{report['export_version']})",
        f"- Mechanism: **{report['mechanism']}** · predictive model: **{report['predictive_model']}** · content effect: **{report['content_effect']}**",
        f"- Threshold: {activation['decisions_required']} decisions / {activation['domains_required']} domains · "
        f"observed {report['observed']['decisions']} / {report['observed']['domains']} · activated: **{activation['met']}**",
        "",
        "> The heuristic only orders work. It cannot accept, reject, or canonicalize anything.",
        "",
        f"## Pending entities ({len(report['entity_queue'])})",
        "",
        "| Rank | Entity | Domain | Score | Reasons |",
        "|---|---|---|---|---|",
    ]
    for row in report["entity_queue"]:
        lines.append(f"| {row['rank']} | `{row['id']}` | {row['domain']} | {row['score']:.6f} | {'; '.join(row['reasons'])} |")
    if not report["entity_queue"]:
        lines.append("| — | none | — | — | — |")
    lines += [
        "",
        f"## Pending connections ({len(report['connection_queue'])})",
        "",
        "| Rank | Connection | Relation | Evidence | Score |",
        "|---|---|---|---|---|",
    ]
    for row in report["connection_queue"]:
        lines.append(f"| {row['rank']} | `{row['id']}` | {row['relation']} | {row['evidence_count']} | {row['score']:.6f} |")
    if not report["connection_queue"]:
        lines.append("| — | none | — | — | — |")
    lines += [
        "",
        "## Invariants",
        "",
    ]
    lines += [f"- {item}" for item in report["invariants"]]
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="R7 heuristic review-queue routing (order only)")
    parser.add_argument("--check", action="store_true", help="verify committed report is fresh")
    args = parser.parse_args(argv)
    report = build()
    json_text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    md_text = render_md(report)
    if args.check:
        stale = []
        for path, text in ((JSON_PATH, json_text), (MD_PATH, md_text)):
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                stale.append(str(path.relative_to(ROOT)))
        if stale:
            print("FAIL: review routing is stale — run python3 scripts/review_router.py", file=sys.stderr)
            for rel in stale:
                print(f"  - {rel}", file=sys.stderr)
            return 1
        print("OK: review routing fresh")
        return 0
    write_text_atomic(JSON_PATH, json_text)
    write_text_atomic(MD_PATH, md_text)
    print(f"OK: review routing — {len(report['entity_queue'])} pending entities, "
          f"{len(report['connection_queue'])} pending connections; predictive model "
          f"activated: {report['activation']['met']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
