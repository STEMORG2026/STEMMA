#!/usr/bin/env python3
"""Shared measurement of real review activity (R7 calibration + routing).

A "labeled decision" here is a recorded review-state transition (`from != to`) in
a connection's `provenance.review_history`, or a reviewed/canonical entity with a
recorded `provenance.reviewed_at`. No-op transitions (`reviewed -> reviewed`) are
excluded: they record an edit, not a decision.

This module never edits review state. It only reads canonical files so that the
calibration report and the router agree on one definition.
"""
from __future__ import annotations

import pathlib
import re
from typing import Any

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
CONNECTIONS = ROOT / "connections"
PILOT_REPORT = ROOT / "reports" / "curation-pilot.md"

REVIEWED_STATUSES = {"human_reviewed", "canonical"}
REVIEWED_TARGETS = REVIEWED_STATUSES | {"reviewed"}
THRESHOLD_DECISIONS = 200
THRESHOLD_DOMAINS = 3


def _frontmatter(path: pathlib.Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        return {}
    data = yaml.safe_load(raw.split("---", 2)[1])
    return data if isinstance(data, dict) else {}


def load_entities() -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for path in sorted(CONTENT.rglob("*.md")):
        data = _frontmatter(path)
        if data.get("id"):
            data["_file"] = str(path.relative_to(ROOT))
            out[data["id"]] = data
    return out


def load_connections() -> list[dict[str, Any]]:
    rows = []
    for path in sorted(CONNECTIONS.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(data, dict) and data.get("id"):
            data["_file"] = str(path.relative_to(ROOT))
            rows.append(data)
    return rows


def review_events() -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for conn in load_connections():
        domain = (conn.get("context") or {}).get("domain") or "unknown"
        for item in (conn.get("provenance") or {}).get("review_history") or []:
            before, after = item.get("from"), item.get("to")
            if not before or not after or before == after:
                continue
            events.append({
                "object": conn["id"],
                "kind": "connection",
                "domain": domain,
                "from": before,
                "to": after,
                "reviewer": item.get("reviewer"),
                "at": item.get("at"),
                "correction_class": item.get("correction_class"),
            })
    for eid, entity in load_entities().items():
        if entity.get("status") not in REVIEWED_STATUSES:
            continue
        reviewed_at = (entity.get("provenance") or {}).get("reviewed_at")
        if not reviewed_at:
            continue
        events.append({
            "object": eid,
            "kind": "entity",
            "domain": entity.get("domain") or "unknown",
            "from": "unreviewed",
            "to": "reviewed" if entity.get("status") == "human_reviewed" else "canonical",
            "reviewer": (entity.get("provenance") or {}).get("reviewer"),
            "at": reviewed_at,
            "correction_class": None,
        })
    return sorted(events, key=lambda e: (e.get("at") or "", e["object"], e["to"]))


def decision_stats() -> dict[str, Any]:
    events = review_events()
    by_domain: dict[str, dict[str, int]] = {}
    for event in events:
        bucket = by_domain.setdefault(event["domain"], {"decisions": 0, "accepted": 0, "rejected": 0, "demoted": 0})
        bucket["decisions"] += 1
        if event["to"] in REVIEWED_TARGETS:
            bucket["accepted"] += 1
        elif event["to"] == "rejected":
            bucket["rejected"] += 1
        elif event["from"] in REVIEWED_TARGETS and event["to"] not in REVIEWED_TARGETS:
            bucket["demoted"] += 1
    accepted = sum(1 for e in events if e["to"] in REVIEWED_TARGETS)
    rejected = sum(1 for e in events if e["to"] == "rejected")
    demoted = sum(1 for e in events
                  if e["from"] in REVIEWED_TARGETS and e["to"] not in REVIEWED_TARGETS)
    domains = sorted(by_domain)
    return {
        "decisions_total": len(events),
        "distinct_objects": len({e["object"] for e in events}),
        "accepted": accepted,
        "rejected": rejected,
        "demoted": demoted,
        "corrections_labeled": sum(1 for e in events if e.get("correction_class")),
        "domains_with_decisions": len(domains),
        "domains": domains,
        "by_domain": by_domain,
        "threshold": {
            "decisions_required": THRESHOLD_DECISIONS,
            "domains_required": THRESHOLD_DOMAINS,
            "decisions_met": len(events) >= THRESHOLD_DECISIONS,
            "domains_met": len(domains) >= THRESHOLD_DOMAINS,
            "met": len(events) >= THRESHOLD_DECISIONS and len(domains) >= THRESHOLD_DOMAINS,
        },
        "events": events,
    }


def historical_pilot() -> dict[str, Any]:
    """The archived 36->12 pilot, kept separate from current-corpus measurements."""
    if not PILOT_REPORT.exists():
        return {"available": False}
    text = PILOT_REPORT.read_text(encoding="utf-8")
    m = re.search(r"(\d+)\s+proposals,\s+(\d+)\s+curated accepted", text)
    if not m:
        return {"available": False}
    proposals, accepted = int(m.group(1)), int(m.group(2))
    return {
        "available": True,
        "source": str(PILOT_REPORT.relative_to(ROOT)),
        "corpus": "archived pilot corpus (not the current repository corpus)",
        "proposals": proposals,
        "accepted": accepted,
        "acceptance_rate": round(accepted / proposals, 4) if proposals else None,
        "auto_canonicalized": 0,
    }
