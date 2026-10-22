#!/usr/bin/env python3
"""Adopt new schema fields on existing entities (schema-change follow-through).

Schema 1.4.0 added optional but recommended fields. When the schema moves, the
corpus must move with it: this script enriches existing canonical entities with
`applications` and `limitations` using the local model, so the corpus carries the
current shape instead of validating as old data. `learning_objectives` is
deliberately excluded: it is consumer/curriculum metadata, not canonical
(ADR-0041/0047).

Usage:
    python3 scripts/enrich_schema_fields.py --domain physics --limit 10 --dry-run
    python3 scripts/enrich_schema_fields.py --domain physics
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
CACHE = ROOT / "state" / "cache" / "llm-enrichment.json"
OLLAMA = "http://localhost:11434/api/generate"
MODEL = "qwen3.5:9b"
CACHE_VERSION = "enrich-v2"
# Deliberately excludes `learning_objectives`: it is a consumer/curriculum field,
# forbidden in canonical content by ADR-0041/0047 and the generality guard
# (tests/curation/test_generality.py). Schema 1.4.0 offers it; canonical STEMMA
# does not adopt it. See docs/MIGRATIONS.md "canonical vs consumer fields".
FIELDS = ["applications", "limitations"]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def save_cache(cache: dict) -> None:
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(cache, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def frontmatter(text: str) -> tuple[str, str, str]:
    front, sep, body = text.partition("\n---\n")
    return front, sep, body


def keys_of(front: str) -> set[str]:
    return set(re.findall(r"^([a-z_]+):", front, flags=re.M))


def definition_of(front: str) -> str:
    m = re.search(r"(?ms)^definition:\s*(.*?)(?=\n[a-z_]+:)", front + "\n__end__:")
    raw = (m.group(1) if m else "").strip()
    if raw[:2] in {">-", "|", ">-", "|-"}:
        raw = raw[2:].strip()
    return " ".join(line.strip() for line in raw.splitlines()).strip()


def cache_key(entity_id: str, definition: str) -> str:
    return hashlib.sha256(f"{CACHE_VERSION}\n{entity_id}\n{definition}".encode("utf-8")).hexdigest()


def select(domain: str | None, offset: int, limit: int) -> list[dict]:
    rows = []
    for path in sorted(CONTENT.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        front, sep, body = frontmatter(text)
        if not sep:
            continue
        if re.search(r"^status:\s*draft\s*$", front, flags=re.M):
            continue
        d = re.search(r"^domain:\s*(\S+)", front, flags=re.M)
        did = re.search(r"^id:\s*(\S+)", front, flags=re.M)
        name = re.search(r"^name:\s*(.+)$", front, flags=re.M)
        if domain and (not d or d.group(1) != domain):
            continue
        present = keys_of(front)
        if all(f in present for f in FIELDS):
            continue
        rows.append({
            "path": path,
            "id": did.group(1) if did else path.stem,
            "term": (name.group(1).strip().strip('"') if name else path.stem),
            "domain": d.group(1) if d else "",
            "definition": definition_of(front),
            "present": present,
            "front": front,
            "sep": sep,
            "body": body,
        })
    return rows[offset: offset + limit]


def llm_batch(items: list[dict], cache: dict) -> None:
    pending = [it for it in items if cache_key(it["id"], it["definition"]) not in cache]
    if not pending:
        return
    lines = [f"{i}. {it['term']} ({it['domain']}): {it['definition']}" for i, it in enumerate(pending, 1)]
    prompt = (
        "You are enriching a canonical undergraduate STEM knowledge base. For each numbered term, "
        "return short accurate metadata. applications: 1-3 representative real-world or cross-domain "
        "uses. limitations: 1-3 scope conditions, approximations, or validity limits (empty array if "
        "none). Each string must be under 20 words. Use your own wording and do not invent citations. "
        "Return ONLY valid JSON: "
        '{"items":[{"term":"...","applications":["..."],"limitations":["..."]}]}.\n\n'
        "Terms:\n" + "\n".join(lines)
    )
    payload = json.dumps({
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "think": False,
        "format": "json",
        "options": {"temperature": 0.1, "num_predict": 3000, "num_ctx": 8192},
    }).encode("utf-8")
    req = urllib.request.Request(OLLAMA, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    raw = (body.get("response") or "").strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
    parsed = json.loads(raw)
    by_term = {str(x.get("term", "")).strip().lower(): x for x in parsed.get("items", []) if isinstance(x, dict)}
    for it in pending:
        row = by_term.get(it["term"].strip().lower())
        if row is None:
            row = next((v for k, v in by_term.items() if k in it["term"].strip().lower() or it["term"].strip().lower() in k), None)
        if row is None:
            continue
        def clean(value) -> list[str]:
            if isinstance(value, str):
                value = [value]
            if not isinstance(value, list):
                return []
            return [str(v).strip() for v in value if str(v).strip()][:3]
        cache[cache_key(it["id"], it["definition"])] = {
            "applications": clean(row.get("applications")),
            "limitations": clean(row.get("limitations")),
        }


def render(block: list[str], key: str) -> str:
    return key + ":\n" + "".join(f"- {yaml.safe_dump(x, default_style=chr(34)).strip()}\n" for x in block)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--domain")
    ap.add_argument("--offset", type=int, default=0)
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--batch-size", type=int, default=10)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    rows = select(args.domain, args.offset, args.limit)
    if not rows:
        print("OK: no entities need enrichment")
        return 0
    cache = load_json(CACHE)
    written = 0
    for start in range(0, len(rows), args.batch_size):
        batch = rows[start:start + args.batch_size]
        llm_batch(batch, cache)
    for it in rows:
        values = cache.get(cache_key(it["id"], it["definition"]))
        if not values:
            print(f"SKIP: {it['id']} (no model output)")
            continue
        additions = []
        for field in FIELDS:
            if field in it["present"] or not values.get(field):
                continue
            additions.append(render(values[field], field))
        if not additions:
            continue
        if args.dry_run:
            print(f"DRY: {it['id']} would add {[a.split(':')[0] for a in additions]}")
            written += 1
            continue
        front = it["front"].rstrip("\n") + "\n" + "\n".join(additions)
        it["path"].write_text(front + it["sep"] + it["body"], encoding="utf-8")
        written += 1
        print(f"OK: {it['path'].relative_to(ROOT)} (+{', '.join(a.split(':')[0] for a in additions)})")
    if not args.dry_run:
        save_cache(cache)
    print(f"OK: {written} entit{'y' if written == 1 else 'ies'} enriched")
    return 0


if __name__ == "__main__":
    sys.exit(main())
