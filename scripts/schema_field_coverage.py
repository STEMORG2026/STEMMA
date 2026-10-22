#!/usr/bin/env python3
"""Report how much the corpus has adopted the current schema's optional fields.

A schema bump is not finished when the schemas change: existing entities must
adopt the new fields where they apply. This report is the measured adoption
check so a future session can see what is still on the old shape.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
JSON_OUT = ROOT / "reports" / "schema-field-coverage.json"
MD_OUT = ROOT / "reports" / "schema-field-coverage.md"

# Fields introduced or promoted by schema 1.4.0 (ADR-0061). Adoption of these is
# tracked; `datasets` applies mainly to data/engineering entities.
TRACKED = ["level", "formal", "examples", "applications",
           "limitations", "datasets", "same_dimensional_quantities"]

# Schema 1.4.0 also offers `learning_objectives`, but canonical STEMMA does not
# adopt it: it is curriculum/consumer metadata, forbidden in canonical content by
# ADR-0041/0047 and enforced by tests/curation/test_generality.py. It is listed
# separately so its absence is read as policy, not as a migration gap.
CONSUMER_ONLY = ["learning_objectives"]


def frontmatter_keys(text: str) -> set[str]:
    if not text.startswith("---\n"):
        return set()
    try:
        end = text.index("\n---\n", 4)
    except ValueError:
        return set()
    return set(re.findall(r"^([a-z_]+):", text[4:end], flags=re.M))


def main() -> int:
    per_domain: dict[str, Counter] = defaultdict(Counter)
    per_domain_total: Counter = Counter()
    field_counts: Counter = Counter()
    total = 0
    for path in sorted(CONTENT.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        m = re.search(r"^domain:\s*(\S+)", text, flags=re.M)
        domain = m.group(1) if m else "unknown"
        keys = frontmatter_keys(text)
        total += 1
        per_domain_total[domain] += 1
        for field in TRACKED:
            if field in keys:
                field_counts[field] += 1
                per_domain[domain][field] += 1

    data = {
        "schema_version_source": "schema/VERSION.yaml",
        "entity_files": total,
        "tracked_fields": TRACKED,
        "adoption": {f: {"count": field_counts.get(f, 0), "percent": round(100 * field_counts.get(f, 0) / total, 1)} for f in TRACKED},
        "consumer_only": {f: {"count": field_counts.get(f, 0), "policy": "not canonical (ADR-0041/0047)"} for f in CONSUMER_ONLY},
        "by_domain": {
            d: {"entities": per_domain_total[d], **{f: per_domain[d].get(f, 0) for f in TRACKED}}
            for d in sorted(per_domain_total)
        },
    }
    JSON_OUT.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# SCHEMA FIELD COVERAGE",
        "",
        f"Measured across **{total}** entity files. Optional 1.4.0 fields are adopted",
        "incrementally; this report exists so a schema bump is not considered finished",
        "while entities still carry only the old shape.",
        "",
        "| Field | Adopted | Percent |",
        "|---|---:|---:|",
    ]
    for f in TRACKED:
        row = data["adoption"][f]
        lines.append(f"| `{f}` | {row['count']} | {row['percent']}% |")
    lines += ["", "## Consumer-only schema fields (intentionally not canonical)", ""]
    for f in CONSUMER_ONLY:
        lines.append(f"- `{f}` — present in {data['consumer_only'][f]['count']} files; {data['consumer_only'][f]['policy']}")
    lines += ["", "## By domain", ""]
    header = "| Domain | Entities | " + " | ".join(f"`{f}`" for f in TRACKED) + " |"
    lines += [header, "|---" * (len(TRACKED) + 2) + "|"]
    for d, row in data["by_domain"].items():
        lines.append("| " + d + " | " + str(row["entities"]) + " | " + " | ".join(str(row[f]) for f in TRACKED) + " |")
    lines.append("")
    MD_OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"OK: wrote {JSON_OUT.relative_to(ROOT)} and {MD_OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
