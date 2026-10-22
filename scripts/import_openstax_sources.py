#!/usr/bin/env python3
"""Create canonical source records from the OpenStax inventory.

The source record states what was consulted and under which license. It does not
claim that OpenStax prose was copied; Tier C books are reference/verification
material only (ADR-0062).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
INVENTORY = ROOT / "state" / "content-inventory.json"
SOURCES = ROOT / "sources"
WRITER = "process:openstax-importer.v1"


def source_id(slug: str) -> str:
    return f"stemma:src.openstax-{slug}"


def build(book: dict) -> dict:
    authors = book.get("authors") or ["OpenStax"]
    year = book.get("year") or ""
    title = book.get("title") or book["slug"]
    license_name = (book.get("license") or {}).get("name") or "unknown"
    license_url = (book.get("license") or {}).get("url") or ""
    tier = (book.get("license") or {}).get("tier") or "D"
    citation = f"{', '.join(authors)} ({year}). {title}. OpenStax. {book.get('url', '')}"
    return {
        "id": source_id(book["slug"]),
        "type": "textbook",
        "citation": citation.strip(),
        "title": title,
        "authors": authors,
        "year": year,
        "publisher": "OpenStax",
        "isbn": book.get("isbn"),
        "url": book.get("url"),
        "language": "en",
        "source_role": "secondary",
        "accessed_at": book.get("retrieved_at") or "2026-10-20",
        "retrieved_at": book.get("retrieved_at") or "2026-10-20",
        "writer": WRITER,
        "license": f"{license_name} {book.get('license', {}).get('version', '')}".strip(),
        "locator_authority": "OpenStax",
        "rights": {
            "license": f"{license_name} ({license_url})".strip(),
            "attribution": (
                f"OpenStax, {title}. Used as a Tier {tier} reference for term discovery "
                "and factual verification; canonical definitions are independently phrased."
            ),
        },
    }


def main() -> int:
    if not INVENTORY.exists():
        print(f"error: missing {INVENTORY}", file=sys.stderr)
        return 2
    data = json.loads(INVENTORY.read_text(encoding="utf-8"))
    written = 0
    for book in data.get("books") or []:
        if not book.get("terms"):
            continue
        record = build(book)
        path = SOURCES / f"{record['id'].split(':', 1)[1]}.yaml"
        path.write_text(
            yaml.safe_dump(record, sort_keys=False, allow_unicode=True, width=100),
            encoding="utf-8",
        )
        written += 1
        print(f"OK: {path.relative_to(ROOT)}")
    print(f"OK: {written} source records")
    return 0


if __name__ == "__main__":
    sys.exit(main())
