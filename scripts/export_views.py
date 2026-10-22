#!/usr/bin/env python3
"""R7 — deterministic consumer views (ADR-0058).

Writes `exports/views/` from the derived export, never from canonical files:

  prerequisites.json  dependency subgraph + strongly-connected cycle sets
  misconceptions.json per-subject misconception records
  formulations.json   per-law modern + historical formulations
  centrality.json     degree / PageRank per entity (from knowledge.extended.json)
  changelog.json      added/removed/changed objects vs the `v3.0.0` release tag
  index.json          view inventory with payload hashes + source content hash

Rules:
- Every view carries `source_content_hash`; a view that disagrees with
  `exports/knowledge.json` is stale by definition.
- No wall clock, no environment-dependent ordering. `--check` byte-compares.
- Views are DERIVED (L6): consumers may rebuild them, the canonical layer never
  depends on them.

Usage:
  python3 scripts/export_views.py            # write all views + index
  python3 scripts/export_views.py --check    # CI: fail if committed views are stale
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import subprocess
import sys
from typing import Any

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from atomic_write import write_text_atomic  # noqa: E402

EXPORT_PATH = ROOT / "exports" / "knowledge.json"
EXTENDED_PATH = ROOT / "exports" / "knowledge.extended.json"
RELATION_PATH = ROOT / "schema" / "relation-registry.yaml"
OUT_DIR = ROOT / "exports" / "views"
VIEW_VERSION = "1.0.0"
BASELINE_TAG = "v3.0.0"

VIEW_NAMES = (
    "prerequisites",
    "misconceptions",
    "formulations",
    "centrality",
    "changelog",
)


class ViewError(RuntimeError):
    pass


def load_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.exists():
        raise ViewError(f"missing {path.relative_to(ROOT)} — run the export chain first")
    return json.loads(path.read_text(encoding="utf-8"))


def load_registry() -> tuple[dict[str, Any], str]:
    data = yaml.safe_load(RELATION_PATH.read_text(encoding="utf-8")) or {}
    relations = data.get("relations") or {}
    if not relations:
        raise ViewError("schema/relation-registry.yaml defines no relations")
    return relations, str(data.get("version") or "unknown")


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def payload_sha256(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _header(view: str, export: dict[str, Any]) -> dict[str, Any]:
    return {
        "view": view,
        "view_version": VIEW_VERSION,
        "export_version": export["export_version"],
        "schema_version": export["schema_version"],
        "source_content_hash": export["content_hash"],
        "license": "CC-BY-4.0",
    }


def _dependency_relations(relations: dict[str, Any]) -> list[str]:
    return sorted(
        name
        for name, rel in relations.items()
        if rel.get("family") == "dependency" and rel.get("status") == "adopted"
    )


def _sccs(nodes: set[str], edges: dict[str, set[str]]) -> list[list[str]]:
    """Tarjan SCCs, iterative and deterministic, returned only for real cycles."""
    index: dict[str, int] = {}
    low: dict[str, int] = {}
    on_stack: set[str] = set()
    stack: list[str] = []
    out: list[list[str]] = []
    counter = 0

    for root in sorted(nodes):
        if root in index:
            continue
        work: list[tuple[str, int]] = [(root, 0)]
        while work:
            node, i = work.pop()
            if i == 0:
                index[node] = low[node] = counter
                counter += 1
                stack.append(node)
                on_stack.add(node)
            succ = sorted(edges.get(node, ()))
            if i < len(succ):
                work.append((node, i + 1))
                nxt = succ[i]
                if nxt not in index:
                    work.append((nxt, 0))
                elif nxt in on_stack:
                    low[node] = min(low[node], index[nxt])
                continue
            if low[node] == index[node]:
                comp: list[str] = []
                while True:
                    item = stack.pop()
                    on_stack.discard(item)
                    comp.append(item)
                    if item == node:
                        break
                comp.sort()
                if len(comp) > 1 or node in edges.get(node, set()):
                    out.append(comp)
            if work:
                parent = work[-1][0]
                low[parent] = min(low[parent], low[node])
    return sorted(out)


def build_prerequisites(export: dict[str, Any], relations: dict[str, Any],
                        registry_version: str) -> dict[str, Any]:
    adopted = set(_dependency_relations(relations))
    names = {e["id"]: e for e in export.get("entities", [])}
    prereq: dict[str, set[str]] = {}
    dependents: dict[str, set[str]] = {}
    edges: list[dict[str, Any]] = []
    for conn in sorted(export.get("connections", []), key=lambda c: c["id"]):
        rel = conn.get("relation")
        target = conn.get("target")
        if rel not in adopted or not target:
            continue
        source = conn["source"]
        if source not in names or target not in names:
            continue
        prereq.setdefault(source, set()).add(target)
        dependents.setdefault(target, set()).add(source)
        edges.append({
            "connection": conn["id"], "source": source, "relation": rel, "target": target,
            "review_status": ((conn.get("assertion") or {}).get("review") or {}).get("status"),
        })
    nodes = sorted(set(prereq) | set(dependents))
    view = _header("prerequisites", export)
    view.update({
        "relations_considered": sorted(adopted),
        "relation_registry_version": registry_version,
        "edge_count": len(edges),
        "edges": edges,
        "nodes": {
            node: {
                "name": (names.get(node) or {}).get("name"),
                "domain": (names.get(node) or {}).get("domain"),
                "status": (names.get(node) or {}).get("status"),
                "prerequisites": sorted(prereq.get(node, ())),
                "dependents": sorted(dependents.get(node, ())),
            }
            for node in nodes
        },
        # SCCs are reported as cycle *sets*, not enumerated simple cycles: the
        # number of simple cycles can explode, and a consumer needs only to know
        # that a group cannot be linearly ordered.
        "cycles": [{"members": comp, "kind": "strongly-connected"} for comp in _sccs(set(nodes), prereq)],
        "note": "Edge source requires target; target is therefore a prerequisite of source.",
    })
    return view


def build_misconceptions(export: dict[str, Any], relations: dict[str, Any],
                         registry_version: str) -> dict[str, Any]:
    adopted = "misconception_of" in relations and relations["misconception_of"].get("status") == "adopted"
    names = {e["id"]: e for e in export.get("entities", [])}
    groups: dict[str, list[dict[str, Any]]] = {}
    records: list[dict[str, Any]] = []
    if adopted:
        for conn in sorted(export.get("connections", []), key=lambda c: c["id"]):
            if conn.get("relation") != "misconception_of" or not conn.get("target"):
                continue
            subject = conn["target"]
            record = {
                "id": conn["source"],
                "name": (names.get(conn["source"]) or {}).get("name"),
                "subject": subject,
                "subject_name": (names.get(subject) or {}).get("name"),
                "connection": conn["id"],
                "review_status": ((conn.get("assertion") or {}).get("review") or {}).get("status"),
                "evidence_count": len(conn.get("evidence") or []),
            }
            records.append(record)
            groups.setdefault(subject, []).append(record)
    view = _header("misconceptions", export)
    view.update({
        "relation": "misconception_of",
        "relation_status": "adopted" if adopted else "not-adopted",
        "relation_registry_version": registry_version,
        "record_count": len(records),
        "records": sorted(records, key=lambda r: r["id"]),
        "by_subject": {k: sorted(v, key=lambda r: r["id"]) for k, v in sorted(groups.items())},
    })
    if not adopted:
        view["note"] = "misconception_of is not adopted in the relation registry."
    return view


def build_formulations(export: dict[str, Any]) -> dict[str, Any]:
    laws = []
    for entity in sorted(export.get("entities", []), key=lambda e: e["id"]):
        if entity.get("type") != "law":
            continue
        formulations: list[dict[str, Any]] = [{
            "kind": "modern",
            "statement": entity.get("definition"),
            "symbol": entity.get("symbol"),
            "source_refs": entity.get("source_refs") or [],
        }]
        for item in sorted(
            (entity.get("historical") or {}).get("timeline") or [],
            key=lambda h: (h.get("year", 0), h.get("by") or "", h.get("event") or ""),
        ):
            formulations.append({
                "kind": "historical",
                "year": item.get("year"),
                "by": item.get("by"),
                "event": item.get("event"),
            })
        laws.append({
            "id": entity["id"],
            "name": entity.get("name"),
            "domain": entity.get("domain"),
            "status": entity.get("status"),
            "formulations": formulations,
        })
    view = _header("formulations", export)
    view.update({"law_count": len(laws), "laws": laws})
    return view


def build_centrality(export: dict[str, Any], extended: dict[str, Any]) -> dict[str, Any]:
    derived = (extended.get("derived") or {}).get("centrality") or {}
    scores = derived.get("all") or {}
    entities = {e["id"]: e for e in export.get("entities", [])}
    rows = []
    for eid in sorted(scores):
        score = scores[eid] or {}
        entity = entities.get(eid) or {}
        rows.append({
            "id": eid,
            "name": entity.get("name"),
            "domain": entity.get("domain"),
            "status": entity.get("status"),
            "degree": score.get("degree", 0),
            "in_degree": score.get("in_degree", 0),
            "out_degree": score.get("out_degree", 0),
            "pagerank": score.get("pagerank", 0.0),
        })
    rows.sort(key=lambda r: (-r["pagerank"], r["id"]))
    view = _header("centrality", export)
    view.update({
        "input": "exports/knowledge.extended.json derived.centrality.all",
        "algorithm": "PageRank over explicit+inverse edges (graph_analysis.py)",
        "entity_count": len(rows),
        "rows": rows,
    })
    return view


def _git_show(ref: str, path: str) -> str | None:
    proc = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        cwd=ROOT, capture_output=True, text=True,
    )
    return proc.stdout if proc.returncode == 0 else None


def build_changelog(export: dict[str, Any]) -> dict[str, Any]:
    view = _header("changelog", export)
    raw = _git_show(BASELINE_TAG, "exports/knowledge.json")
    if raw is None:
        view.update({
            "basis": None,
            "added_entities": [], "removed_entities": [], "changed_entities": [],
            "added_connections": [], "removed_connections": [], "changed_connections": [],
            "note": f"baseline {BASELINE_TAG} is unavailable in this checkout; no diff computed",
        })
        return view

    baseline = json.loads(raw)
    before_e = {e["id"]: e for e in baseline.get("entities", [])}
    after_e = {e["id"]: e for e in export.get("entities", [])}
    before_c = {c["id"]: c for c in baseline.get("connections", [])}
    after_c = {c["id"]: c for c in export.get("connections", [])}

    def changed(before: dict[str, Any], after: dict[str, Any]) -> list[dict[str, Any]]:
        out = []
        for oid in sorted(set(before) & set(after)):
            fields = sorted(k for k in set(before[oid]) | set(after[oid])
                            if canonical_json(before[oid].get(k)) != canonical_json(after[oid].get(k)))
            if fields:
                out.append({"id": oid, "changed_fields": fields})
        return out

    view.update({
        "basis": {
            "kind": "git-tag", "ref": BASELINE_TAG,
            "content_hash": baseline.get("content_hash"),
            "entity_count": baseline.get("entity_count"),
            "connection_count": baseline.get("connection_count"),
        },
        "current": {
            "content_hash": export.get("content_hash"),
            "entity_count": export.get("entity_count"),
            "connection_count": export.get("connection_count"),
        },
        "added_entities": sorted(set(after_e) - set(before_e)),
        "removed_entities": sorted(set(before_e) - set(after_e)),
        "changed_entities": changed(before_e, after_e),
        "added_connections": sorted(set(after_c) - set(before_c)),
        "removed_connections": sorted(set(before_c) - set(after_c)),
        "changed_connections": changed(before_c, after_c),
        "unchanged": baseline.get("content_hash") == export.get("content_hash"),
    })
    return view


def build_all() -> dict[str, dict[str, Any]]:
    export = load_json(EXPORT_PATH)
    extended = load_json(EXTENDED_PATH)
    relations, registry_version = load_registry()
    if extended.get("content_hash") != export.get("content_hash"):
        raise ViewError("exports/knowledge.extended.json is stale relative to exports/knowledge.json")
    views = {
        "prerequisites": build_prerequisites(export, relations, registry_version),
        "misconceptions": build_misconceptions(export, relations, registry_version),
        "formulations": build_formulations(export),
        "centrality": build_centrality(export, extended),
        "changelog": build_changelog(export),
    }
    index = {
        "view": "index",
        "view_version": VIEW_VERSION,
        "export_version": export["export_version"],
        "schema_version": export["schema_version"],
        "source_content_hash": export["content_hash"],
        "license": "CC-BY-4.0",
        "views": [
            {
                "name": name,
                "path": f"exports/views/{name}.json",
                "sha256": payload_sha256(views[name]),
            }
            for name in VIEW_NAMES
        ],
    }
    views["index"] = index
    return views


def render(view: dict[str, Any]) -> str:
    return json.dumps(view, indent=2, ensure_ascii=False, sort_keys=False) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Deterministic consumer views (R7, ADR-0058)")
    parser.add_argument("--check", action="store_true", help="verify committed views are fresh; write nothing")
    args = parser.parse_args(argv)
    try:
        views = build_all()
        stale: list[str] = []
        for name in VIEW_NAMES + ("index",):
            path = OUT_DIR / f"{name}.json"
            rel = path.relative_to(ROOT)
            text = render(views[name])
            if args.check:
                if not path.exists() or path.read_text(encoding="utf-8") != text:
                    stale.append(str(rel))
                continue
            OUT_DIR.mkdir(parents=True, exist_ok=True)
            write_text_atomic(path, text)
            print(f"OK: {rel} — {payload_sha256(views[name])[:19]}…")
        if stale:
            print("FAIL: consumer views are stale or missing — run python3 scripts/export_views.py", file=sys.stderr)
            for rel in stale:
                print(f"  - {rel}", file=sys.stderr)
            return 1
        if args.check:
            print(f"OK: {len(VIEW_NAMES)} consumer views fresh (source {views['index']['source_content_hash'][:19]}…)")
        return 0
    except ViewError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
