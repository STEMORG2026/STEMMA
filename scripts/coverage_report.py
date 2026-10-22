#!/usr/bin/env python3
"""Measured content coverage against the OpenStax term inventory.

Reports counts by domain and subdomain, plus source gaps. It never estimates
unmeasured coverage and never copies reference prose.
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
INVENTORY = ROOT / "state" / "content-inventory.json"
CONTENT = ROOT / "content"
JSON_OUT = ROOT / "reports" / "content-coverage.json"
MD_OUT = ROOT / "reports" / "content-coverage.md"


def entities() -> list[dict]:
    out = []
    for path in sorted(CONTENT.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        try:
            end = text.index("\n---", 4)
            data = yaml.safe_load(text[4:end]) or {}
        except (ValueError, yaml.YAMLError):
            continue
        if isinstance(data, dict):
            data["_path"] = path.relative_to(ROOT).as_posix()
            out.append(data)
    return out


def main() -> int:
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    counts: dict[str, dict] = {}
    subcounts: dict[tuple[str, str], dict] = defaultdict(lambda: {"inventory_terms": 0, "books": set()})
    for book in inventory.get("books") or []:
        domain = book["domain"]
        domain_row = counts.setdefault(domain, {"inventory_terms": 0, "books": 0, "entities": 0, "canonical": 0, "draft": 0})
        domain_row["books"] += 1
        domain_row["inventory_terms"] += len(book.get("terms") or [])
        sub = subcounts[(domain, book["subdomain"])]
        sub["inventory_terms"] += len(book.get("terms") or [])
        sub["books"].add(book["slug"])

    for entity in entities():
        domain = entity.get("domain")
        if domain not in counts:
            continue
        counts[domain]["entities"] += 1
        if entity.get("status") == "canonical":
            counts[domain]["canonical"] += 1
        elif entity.get("status") == "draft":
            counts[domain]["draft"] += 1
        subkey = (str(domain), str(entity.get("subdomain") or "unassigned"))
        subcounts[subkey]["entities"] = subcounts[subkey].get("entities", 0) + 1

    reported = {}
    for domain, row in sorted(counts.items()):
        inv = row["inventory_terms"]
        row["coverage_percent"] = round(100 * row["entities"] / inv, 2) if inv else 0.0
        reported[domain] = row

    subs = []
    for (domain, sub), row in sorted(subcounts.items()):
        inv = row["inventory_terms"]
        subs.append({
            "domain": domain,
            "subdomain": sub,
            "books": sorted(row["books"]),
            "inventory_terms": inv,
            "entities": row.get("entities", 0),
            "coverage_percent": round(100 * row.get("entities", 0) / inv, 2) if inv else 0.0,
        })

    zero_books = [b["slug"] for b in inventory.get("books") or [] if not b.get("terms")]
    data = {
        "inventory_books": len(inventory.get("books") or []),
        "inventory_unique_terms": (inventory.get("counts") or {}).get("unique_terms_by_domain"),
        "domains": reported,
        "subdomains": subs,
        "source_gaps": {
            "books_with_no_parsed_terms": zero_books,
            "engineering_breadth": "OpenStax covers computer, software, data, and additive manufacturing; civil/electrical/chemical/mechanical breadth still needs public-domain DOE/NASA/NIST/USACE sources.",
        },
    }
    JSON_OUT.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# CONTENT COVERAGE",
        "",
        f"Inventory: **{data['inventory_books']} books**, **{data['inventory_unique_terms']} unique terms**.",
        "Coverage means canonical/draft entity files in `content/`, not generated or planned records.",
        "",
        "| Domain | Inventory terms | Entities | Canonical | Draft | Coverage |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for domain, row in reported.items():
        lines.append(f"| {domain} | {row['inventory_terms']} | {row['entities']} | {row['canonical']} | {row['draft']} | {row['coverage_percent']}% |")
    lines += ["", "## Source gaps", ""]
    lines += [f"- `{slug}` yields no parsed terms" for slug in zero_books]
    lines += [
        "- Engineering breadth: OpenStax covers computer, software, data, and additive manufacturing;",
        "  civil/electrical/chemical/mechanical breadth still needs public-domain DOE/NASA/NIST/USACE sources.",
        "",
        "## Limits",
        "",
        "- OpenStax is Tier C (NC-SA) reference material: term inventory and fact checks only.",
        "- The inventory is not a list of canonical claims; each entity is independently phrased",
        "  and passed schema, source, no-verbatim, and quality checks.",
        "",
    ]
    MD_OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"OK: wrote {JSON_OUT.relative_to(ROOT)} and {MD_OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
