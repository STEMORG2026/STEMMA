#!/usr/bin/env python3
"""Content-addressed store prototype for canonical source files.

The corpus stays on sharded Markdown files for now. This module computes a
per-file SHA-256 and a deterministic Merkle root over `content/`, so a consumer
can verify a checkout or a bundle without trusting timestamps or directory
order.

Usage:
    python3 scripts/content_store.py --write
    python3 scripts/content_store.py --check
    python3 scripts/content_store.py --root
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
MANIFEST = ROOT / "exports" / "content-manifest.json"
VERSION = "1.0.0"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def leaf_hash(relpath: str, data: bytes) -> str:
    return sha256_bytes(relpath.encode("utf-8") + b"\0" + data)


def merkle_root(hashes: list[str]) -> str:
    if not hashes:
        return sha256_bytes(b"")
    level = list(hashes)
    while len(level) > 1:
        if len(level) % 2:
            level.append(level[-1])
        level = [
            sha256_bytes((level[i] + level[i + 1]).encode("ascii"))
            for i in range(0, len(level), 2)
        ]
    return level[0]


def build() -> dict:
    files = []
    leaves = []
    for path in sorted(CONTENT.rglob("*.md")):
        rel = path.relative_to(ROOT).as_posix()
        data = path.read_bytes()
        file_hash = sha256_bytes(data)
        files.append({"path": rel, "sha256": file_hash, "bytes": len(data)})
        leaves.append(leaf_hash(rel, data))
    return {
        "version": VERSION,
        "algorithm": "sha256-merkle",
        "file_count": len(files),
        "root": f"sha256:{merkle_root(leaves)}",
        "files": files,
    }


def check(manifest: dict) -> list[str]:
    current = build()
    problems: list[str] = []
    if manifest.get("root") != current["root"]:
        problems.append(f"root mismatch: manifest {manifest.get('root')} != tree {current['root']}")
    expected = {f["path"]: f for f in manifest.get("files") or []}
    actual = {f["path"]: f for f in current["files"]}
    for path in sorted(set(expected) - set(actual)):
        problems.append(f"missing from tree: {path}")
    for path in sorted(set(actual) - set(expected)):
        problems.append(f"not in manifest: {path}")
    for path in sorted(set(expected) & set(actual)):
        if expected[path]["sha256"] != actual[path]["sha256"]:
            problems.append(f"hash mismatch: {path}")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Content-addressed manifest")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write", action="store_true", help="write exports/content-manifest.json")
    group.add_argument("--check", action="store_true", help="verify the tree against the manifest")
    group.add_argument("--root", action="store_true", help="print the Merkle root only")
    args = parser.parse_args(argv)

    current = build()
    if args.root:
        print(current["root"])
        return 0
    if args.check:
        if not MANIFEST.exists():
            print(f"FAIL: manifest missing: {MANIFEST.relative_to(ROOT)}", file=sys.stderr)
            return 1
        problems = check(json.loads(MANIFEST.read_text(encoding="utf-8")))
        if problems:
            for problem in problems:
                print(f"FAIL: {problem}", file=sys.stderr)
            return 1
        print(f"OK: content manifest matches — {current['file_count']} files, {current['root'][:19]}…")
        return 0

    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"OK: wrote {MANIFEST.relative_to(ROOT)} — {current['file_count']} files, {current['root'][:19]}…")
    return 0


if __name__ == "__main__":
    sys.exit(main())
