#!/usr/bin/env python3
"""Watch schema and inventory files for drift.

The owner asked for a 30-minute schema check. This watcher records a digest of
every schema/vocabulary file plus the content inventory, and appends an event
when something changes. It never edits or upgrades a schema by itself.

Usage:
    python3 scripts/schema_watch.py --once
    python3 scripts/schema_watch.py --loop --interval 1800
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "state" / "schema-watch.json"
LOG = ROOT / "state" / "schema-watch-log.jsonl"
REPORT = ROOT / "state" / "SCHEMA-WATCH.md"
WATCH = [
    "schema/concept.schema.json",
    "schema/source.schema.json",
    "schema/connection.schema.json",
    "schema/VERSION.yaml",
    "schema/agent-registry.yaml",
    "schema/vocabularies/subdomains.yaml",
    "state/content-inventory.json",
]


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def snapshot() -> dict[str, str]:
    out: dict[str, str] = {}
    for rel in WATCH:
        path = ROOT / rel
        if path.exists():
            out[rel] = digest(path)
    for path in sorted((ROOT / "schema").rglob("*")):
        if path.is_file() and path.suffix in {".yaml", ".json", ".ttl"}:
            rel = path.relative_to(ROOT).as_posix()
            out.setdefault(rel, digest(path))
    return dict(sorted(out.items()))


def combined(files: dict[str, str]) -> str:
    h = hashlib.sha256()
    for rel, value in files.items():
        h.update(f"{rel}\0{value}\n".encode("utf-8"))
    return h.hexdigest()


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {}


def write_report(event: dict, files: dict[str, str]) -> None:
    lines = [
        "# SCHEMA WATCH",
        "",
        f"- Digest: `{event['digest']}`",
        f"- Event: **{event['event']}**",
        f"- Files watched: {len(files)}",
        "",
    ]
    changed = event.get("changed") or []
    if changed:
        lines += ["## Changed", ""] + [f"- `{p}`" for p in changed] + [""]
    else:
        lines += ["No schema or inventory changes since the previous check.", ""]
    lines += [
        "This watcher reports drift only. Schema upgrades remain deliberate changes",
        "with an ADR and a migration entry.",
        "",
    ]
    text = "\n".join(lines)
    if not REPORT.exists() or REPORT.read_text(encoding="utf-8") != text:
        REPORT.write_text(text, encoding="utf-8")


def check() -> dict:
    files = snapshot()
    state = load_state()
    previous = state.get("files") or {}
    changed = sorted(p for p in set(previous) | set(files) if previous.get(p) != files.get(p))
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    event = {
        "at": now,
        "event": "change" if changed else "no-change",
        "digest": combined(files),
        "changed": changed,
        "file_count": len(files),
    }
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, sort_keys=True) + "\n")
    STATE.write_text(json.dumps({"updated_at": now, "digest": event["digest"], "files": files}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_report(event, files)
    print(f"{event['event'].upper()}: {event['digest'][:16]} ({len(files)} files)")
    if changed:
        for path in changed:
            print(f"  changed: {path}")
    return event


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Watch schema/inventory drift")
    parser.add_argument("--once", action="store_true", help="check once (default)")
    parser.add_argument("--loop", action="store_true", help="check forever")
    parser.add_argument("--interval", type=int, default=1800, help="seconds between checks")
    args = parser.parse_args(argv)
    if args.interval < 60:
        print("error: interval must be at least 60 seconds", file=sys.stderr)
        return 2
    if not args.loop:
        check()
        return 0
    print(f"schema watcher: every {args.interval}s; log {LOG.relative_to(ROOT)}")
    while True:
        try:
            check()
        except Exception as exc:  # keep the watcher alive; log the failure
            print(f"FAIL: {exc}", file=sys.stderr)
        time.sleep(args.interval)


if __name__ == "__main__":
    sys.exit(main())
