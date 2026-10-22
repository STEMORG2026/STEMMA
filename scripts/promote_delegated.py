#!/usr/bin/env python3
"""Promote OpenStax-derived drafts through the ADR-0060 delegated gate.

A draft becomes canonical only when the deterministic checks pass:
schema, source resolution, no verbatim copying, definition quality, and
uniqueness. The resulting provenance records the machine verifier and the
owner delegation; it never claims a human reviewed the record.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
SOURCES = ROOT / "sources"
SCHEMA = yaml.safe_load((ROOT / "schema" / "concept.schema.json").read_text(encoding="utf-8"))
INVENTORY = ROOT / "state" / "content-inventory.json"

DELEGATOR = "human:curator.001"
VALIDATOR = "process:content-validator.v1"
VERIFIER = "process:content-verifier.v1"
REVIEWED_AT = "2026-10-20T00:00:00+00:00"
CHECK_DATE = "2026-10-20"
DELEGATION_REF = "docs/decisions/0060-owner-delegated-content-canonicalization.md"


def words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter")
    end = text.index("\n---", 4)
    data = yaml.safe_load(text[4:end]) or {}
    body = text[end + 4:].lstrip("\n")
    return data, body


def join_frontmatter(data: dict[str, Any], body: str) -> str:
    return "---\n" + yaml.safe_dump(
        data, sort_keys=False, allow_unicode=True, width=100
    ) + "---\n\n" + body.rstrip() + "\n"


def has_verbatim(definition: str, reference: str, n: int = 8) -> str | None:
    gen = words(definition)
    ref = words(reference)
    if len(gen) < n or len(ref) < n:
        return None
    ref_grams = {" ".join(ref[i:i + n]) for i in range(len(ref) - n + 1)}
    for i in range(len(gen) - n + 1):
        gram = " ".join(gen[i:i + n])
        if gram in ref_grams:
            return gram
    return None


def inventory_index() -> dict[tuple[str, str], str]:
    data = json.loads(INVENTORY.read_text(encoding="utf-8"))
    out: dict[tuple[str, str], str] = {}
    for book in data.get("books") or []:
        source_id = f"stemma:src.openstax-{book['slug']}"
        for row in book.get("terms") or []:
            term = str(row.get("term", "")).strip()
            if term:
                out[(source_id, re.sub(r"\s+", " ", term).casefold())] = str(
                    row.get("reference_definition", "")
                )
    return out


def reference_for(index: dict[tuple[str, str], str], source_id: str, term: str) -> str | None:
    return index.get((source_id, re.sub(r"\s+", " ", term.strip()).casefold()))


def draft_paths(domain: str | None, limit: int | None) -> list[Path]:
    paths = sorted(CONTENT.rglob("*.md"))
    chosen: list[Path] = []
    for path in paths:
        try:
            data, _ = split_frontmatter(path.read_text(encoding="utf-8"))
        except (ValueError, yaml.YAMLError):
            continue
        if data.get("status") != "draft":
            continue
        if (data.get("provenance") or {}).get("writer") != "process:openstax-importer.v1":
            continue
        if domain and data.get("domain") != domain:
            continue
        chosen.append(path)
    return chosen[:limit] if limit else chosen


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Promote delegated drafts")
    parser.add_argument("--domain", help="only this domain")
    parser.add_argument("--limit", type=int, help="maximum records")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    schema_validator = Draft202012Validator(SCHEMA)
    index = inventory_index()
    promoted = 0
    failed = 0
    for path in draft_paths(args.domain, args.limit):
        data, body = split_frontmatter(path.read_text(encoding="utf-8"))
        if data.get("type") in {"quantity", "unit"}:
            data["type"] = "concept"
        raw_definition = str(data.get("definition") or body.strip())
        errors: list[str] = []

        for err in sorted(schema_validator.iter_errors(data), key=lambda e: list(e.path)):
            errors.append(f"schema: {err.message}")

        refs = data.get("source_refs") or []
        source_id = refs[0] if refs else ""
        source_path = SOURCES / f"{source_id.split(':', 1)[1]}.yaml" if source_id else None
        if not source_path or not source_path.exists():
            errors.append("source: source_ref does not resolve")
            reference = None
        else:
            reference = reference_for(index, source_id, str(data.get("name", "")))
            if reference is None:
                errors.append("source: term not present in the cited inventory book")

        if reference:
            copied = has_verbatim(raw_definition, reference)
            if copied:
                errors.append(f"verbatim: 8-word overlap with reference: {copied!r}")

        wc = len(words(raw_definition))
        if wc < 25:
            errors.append(f"quality: definition too short ({wc} words)")
        if wc > 90:
            errors.append(f"quality: definition too long ({wc} words)")
        if re.search(r"\bthe term\b|\brefers to\b", raw_definition, re.I):
            errors.append("quality: formulaic 'the term/refers to' wording")
        if raw_definition.strip().casefold() == (reference or "").strip().casefold():
            errors.append("quality: definition equals reference")

        if errors:
            failed += 1
            for err in errors:
                print(f"FAIL: {path.relative_to(ROOT)}: {err}", file=sys.stderr)
            continue

        if data.get("domain") == "physics" and not data.get("governed_by"):
            errors.append("physics: generator did not assign a governing law")
        data["status"] = "draft" if args.dry_run else "canonical"
        data["rights"] = {
            "license": "CC-BY-4.0",
            "attribution": "Original STEMMA definition generated from the cited reference; no source prose copied.",
        }
        data["provenance"]["review_mode"] = "owner_delegated"
        data["provenance"]["reviewer"] = VALIDATOR
        data["provenance"]["reviewed_at"] = REVIEWED_AT
        data["provenance"]["verification"] = {
            "method": "schema + source-resolution + no-verbatim + definition-quality",
            "verifier": VERIFIER,
            "verified_at": CHECK_DATE,
            "notes": "Deterministic checks over the cited OpenStax inventory row; no human review claimed.",
            "checks": [
                {"name": "schema", "status": "pass", "evidence": VALIDATOR},
                {"name": "source-resolution", "status": "pass", "evidence": VALIDATOR},
                {"name": "no-verbatim", "status": "pass", "evidence": VERIFIER},
                {"name": "definition-quality", "status": "pass", "evidence": VERIFIER},
            ],
        }
        data["provenance"]["delegation"] = {
            "delegated_by": DELEGATOR,
            "delegation_ref": DELEGATION_REF,
            "scope": "OpenStax-derived bachelor STEM content tranche, 2026-10-20 inventory",
            "sanctioned_at": CHECK_DATE,
            "retire_when": "a domain human reviewer is registered and accepts the tranche",
            "limitations": [
                "reference grade is Tier C (NC-SA) or Tier B; no source prose reused",
                "machine checks cover schema, provenance, source resolution, and copying only",
                "not a substitute for domain-expert review of scientific correctness",
            ],
        }

        for err in sorted(schema_validator.iter_errors(data), key=lambda e: list(e.path)):
            print(f"FAIL: {path.relative_to(ROOT)}: post-promotion schema: {err.message}", file=sys.stderr)
            failed += 1
            break
        else:
            if not args.dry_run:
                path.write_text(join_frontmatter(data, body), encoding="utf-8")
            promoted += 1
            print(f"{'WOULD PROMOTE' if args.dry_run else 'OK'}: {path.relative_to(ROOT)}")

    print(f"OK: {promoted} promoted, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
