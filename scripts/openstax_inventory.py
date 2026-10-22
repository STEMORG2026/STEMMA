#!/usr/bin/env python3
"""OpenStax term inventory — coverage discovery, never canonical prose.

Fetches the public OpenStax book metadata, TOC, and key-terms pages, then writes
a deterministic term inventory with source/license metadata. The inventory is a
planning and verification artifact: definitions here are *reference excerpts*
and must not be copied into canonical definitions (ADR-0062).

Usage:
    python3 scripts/openstax_inventory.py
    python3 scripts/openstax_inventory.py --books university-physics-volume-1
    python3 scripts/openstax_inventory.py --check
"""
from __future__ import annotations

import argparse
import concurrent.futures
import html
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "state" / "content-inventory.json"
API = "https://openstax.org/apps/cms/api/v2/pages/?type=books.Book&fields=*&slug={slug}"
SITE = "https://openstax.org/books/{slug}/pages/{page}"
UA = "STEMMA-content-inventory/1.0 (+https://github.com/sajan/STEMMA)"
RETRIEVED_AT = "2026-10-20"

# The catalogue is deliberately explicit: a domain/subdomain mapping is a
# curation decision, not something to infer from a title.
BOOKS: list[dict[str, str]] = [
    {"slug": "university-physics-volume-1", "domain": "physics", "subdomain": "general", "level": "intermediate"},
    {"slug": "university-physics-volume-2", "domain": "physics", "subdomain": "general", "level": "intermediate"},
    {"slug": "university-physics-volume-3", "domain": "physics", "subdomain": "general", "level": "intermediate"},
    {"slug": "college-physics-2e", "domain": "physics", "subdomain": "general", "level": "foundational"},
    {"slug": "chemistry-2e", "domain": "chemistry", "subdomain": "general", "level": "intermediate"},
    {"slug": "organic-chemistry", "domain": "chemistry", "subdomain": "organic-chemistry", "level": "intermediate"},
    {"slug": "biology-2e", "domain": "biology", "subdomain": "general", "level": "intermediate"},
    {"slug": "microbiology", "domain": "biology", "subdomain": "microbiology", "level": "intermediate"},
    {"slug": "anatomy-and-physiology-2e", "domain": "biology", "subdomain": "physiology", "level": "intermediate"},
    {"slug": "astronomy-2e", "domain": "earth-space", "subdomain": "astronomy", "level": "intermediate"},
    {"slug": "calculus-volume-1", "domain": "mathematics", "subdomain": "calculus", "level": "intermediate"},
    {"slug": "calculus-volume-2", "domain": "mathematics", "subdomain": "calculus", "level": "intermediate"},
    {"slug": "calculus-volume-3", "domain": "mathematics", "subdomain": "calculus", "level": "intermediate"},
    {"slug": "algebra-and-trigonometry-2e", "domain": "mathematics", "subdomain": "algebra", "level": "foundational"},
    {"slug": "college-algebra-2e", "domain": "mathematics", "subdomain": "algebra", "level": "foundational"},
    {"slug": "precalculus-2e", "domain": "mathematics", "subdomain": "precalculus", "level": "foundational"},
    {"slug": "introductory-statistics-2e", "domain": "mathematics", "subdomain": "statistics-probability", "level": "intermediate"},
    {"slug": "introduction-computer-science", "domain": "engineering", "subdomain": "computer", "level": "foundational"},
    {"slug": "introduction-python-programming", "domain": "engineering", "subdomain": "software-engineering", "level": "foundational"},
    {"slug": "principles-data-science", "domain": "engineering", "subdomain": "data-engineering", "level": "intermediate"},
    {"slug": "additive-manufacturing-essentials", "domain": "engineering", "subdomain": "mechanical", "level": "intermediate"},
    {"slug": "physics", "domain": "physics", "subdomain": "general", "level": "foundational"},
]


def fetch(url: str, retries: int = 3) -> str:
    last: Exception | None = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=45) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except (urllib.error.URLError, TimeoutError) as exc:  # pragma: no cover - network
            last = exc
            time.sleep(0.75 * (attempt + 1))
    raise RuntimeError(f"fetch failed: {url}: {last}")


def clean_html(value: str) -> str:
    """Strip markup while preserving math alt text and readable structure."""
    value = re.sub(
        r"<math\b[^>]*\balttext=\"([^\"]*)\"[^>]*>.*?</math>",
        lambda m: f" {html.unescape(m.group(1))} ",
        value,
        flags=re.S | re.I,
    )
    value = re.sub(r"<br\s*/?>", "; ", value, flags=re.I)
    value = re.sub(r"</(p|li|dt|dd|div|h[1-6])>", "; ", value, flags=re.I)
    value = re.sub(r"<[^>]+>", "", value)
    value = html.unescape(value)
    value = re.sub(r"\s+", " ", value).strip(" ;")
    return value


def title_text(value: str) -> str:
    return clean_html(value)


def walk_toc(node: Any, out: list[dict[str, Any]]) -> None:
    if isinstance(node, dict):
        if node.get("slug") and "key-terms" in str(node.get("slug", "")):
            out.append(node)
        for child in node.values():
            walk_toc(child, out)
    elif isinstance(node, list):
        for child in node:
            walk_toc(child, out)


def extract_tree(page_html: str) -> dict[str, Any] | None:
    marker = '"tree":'
    idx = page_html.find(marker)
    if idx < 0:
        return None
    try:
        obj, _ = json.JSONDecoder().raw_decode(page_html[idx + len(marker):])
        return obj if isinstance(obj, dict) else None
    except json.JSONDecodeError:
        return None


def parse_glossary(page_html: str) -> list[dict[str, str]]:
    terms: list[dict[str, str]] = []
    for block in re.findall(r"<dl\b[^>]*>(.*?)</dl>", page_html, flags=re.S | re.I):
        dt = re.search(r"<dt\b[^>]*>(.*?)</dt>", block, flags=re.S | re.I)
        dd = re.search(r"<dd\b[^>]*>(.*?)</dd>", block, flags=re.S | re.I)
        if not dt or not dd:
            continue
        term = clean_html(dt.group(1))
        definition = clean_html(dd.group(1))
        if term and definition:
            terms.append({"term": term, "reference_definition": definition})
    return terms


def slugify(value: str) -> str:
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return re.sub(r"-+", "-", value).strip("-")[:80]


def license_tier(name: str) -> str:
    low = (name or "").lower()
    if "noncommercial" in low or "sharealike" in low or "non-commercial" in low:
        return "C"
    if "attribution" in low:
        return "B"
    if "cc0" in low or "public domain" in low:
        return "A"
    return "D"


def book_url(slug: str) -> str:
    return f"https://openstax.org/books/{slug}"


def collect_book(spec: dict[str, str], limit_pages: int | None = None) -> dict[str, Any]:
    slug = spec["slug"]
    meta_raw = fetch(API.format(slug=slug))
    meta = (json.loads(meta_raw).get("items") or [{}])[0]
    # `webview_link` points at cnx.org for several books and has no `"tree":`
    # block; `webview_rex_link` is the OpenStax reader entry point.
    webview = meta.get("webview_rex_link") or meta.get("webview_link") or ""
    if "openstax.org/books/" not in str(webview):
        webview = f"https://openstax.org/books/{slug}/pages/1-introduction"
    page_html = fetch(webview)
    tree = extract_tree(page_html)
    if not tree:
        raise RuntimeError(f"{slug}: TOC tree not found")
    key_pages: list[dict[str, Any]] = []
    walk_toc(tree, key_pages)
    if limit_pages is not None:
        key_pages = key_pages[:limit_pages]

    terms: list[dict[str, str]] = []
    for node in key_pages:
        page_slug = str(node.get("slug"))
        url = SITE.format(slug=slug, page=page_slug)
        try:
            body = fetch(url)
        except RuntimeError as exc:
            terms.append({"term": "__FETCH_ERROR__", "reference_definition": str(exc), "page": page_slug})
            continue
        chapter = title_text(str(node.get("title", "")))
        for term in parse_glossary(body):
            terms.append({**term, "page": page_slug, "chapter": chapter, "url": url})

    authors = []
    for entry in meta.get("authors") or []:
        value = entry.get("value") if isinstance(entry, dict) else None
        if isinstance(value, dict) and value.get("name"):
            authors.append(value["name"])
    categories = []
    for entry in meta.get("book_categories") or []:
        if isinstance(entry, dict) and entry.get("subject_category"):
            categories.append(entry["subject_category"])

    license_name = str(meta.get("license_name") or "")
    return {
        "slug": slug,
        "title": meta.get("title") or slug,
        "authors": authors,
        "publisher": "OpenStax",
        "year": str(meta.get("publish_date") or "")[:4],
        "isbn": meta.get("digital_isbn_13") or meta.get("print_isbn_13"),
        "url": book_url(slug),
        "webview": webview,
        "categories": categories,
        "license": {
            "name": license_name,
            "version": str(meta.get("license_version") or ""),
            "url": meta.get("license_url") or "",
            "tier": license_tier(license_name),
        },
        "domain": spec["domain"],
        "subdomain": spec["subdomain"],
        "level": spec["level"],
        "key_terms_pages": len(key_pages),
        "terms": terms,
    }


def build(books: list[dict[str, str]], limit_pages: int | None) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(collect_book, spec, limit_pages): spec for spec in books}
        for future in concurrent.futures.as_completed(futures):
            spec = futures[future]
            try:
                results.append(future.result())
                print(f"OK: {spec['slug']}", file=sys.stderr)
            except Exception as exc:  # pragma: no cover - network
                print(f"FAIL: {spec['slug']}: {exc}", file=sys.stderr)
                results.append({**spec, "error": str(exc), "terms": [], "key_terms_pages": 0})
    results.sort(key=lambda b: b["slug"])

    by_domain: dict[str, int] = {}
    by_tier: dict[str, int] = {}
    seen: set[str] = set()
    unique = 0
    collisions = 0
    for book in results:
        domain = book.get("domain", "")
        by_domain[domain] = by_domain.get(domain, 0) + len(book.get("terms") or [])
        tier = (book.get("license") or {}).get("tier", "D")
        by_tier[tier] = by_tier.get(tier, 0) + 1
        for term in book.get("terms") or []:
            key = f"{domain}:{term.get('term', '').casefold()}"
            if key in seen:
                collisions += 1
            else:
                seen.add(key)
                unique += 1

    return {
        "version": "1.0.0",
        "retrieved_at": RETRIEVED_AT,
        "purpose": "coverage inventory and verification reference; reference_definition is OpenStax prose and MUST NOT be copied into canonical content (ADR-0062)",
        "books": results,
        "counts": {
            "books": len([b for b in results if not b.get("error")]),
            "failed_books": len([b for b in results if b.get("error")]),
            "key_terms_pages": sum(int(b.get("key_terms_pages") or 0) for b in results),
            "term_rows": sum(len(b.get("terms") or []) for b in results),
            "unique_terms_by_domain": unique,
            "duplicate_rows": collisions,
            "rows_by_domain": by_domain,
            "books_by_license_tier": by_tier,
        },
    }


def check(path: Path) -> int:
    if not path.exists():
        print(f"FAIL: missing {path}", file=sys.stderr)
        return 1
    data = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    if not data.get("books"):
        errors.append("no books")
    for book in data.get("books") or []:
        if not book.get("slug"):
            errors.append("book missing slug")
        if not book.get("license"):
            errors.append(f"{book.get('slug')}: missing license")
        for term in book.get("terms") or []:
            if not term.get("term") or not term.get("reference_definition"):
                errors.append(f"{book.get('slug')}: malformed term row")
    if errors:
        for error in errors[:20]:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"OK: inventory {data['counts']['term_rows']} rows, {data['counts']['unique_terms_by_domain']} unique terms")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="OpenStax coverage inventory (ADR-0062)")
    parser.add_argument("--books", help="comma-separated slugs (default: all)")
    parser.add_argument("--limit-pages", type=int, default=None, help="smoke-test only")
    parser.add_argument("--output", type=Path, default=OUT)
    parser.add_argument("--check", action="store_true", help="validate an existing inventory")
    args = parser.parse_args(argv)

    if args.check:
        return check(args.output)

    selected = BOOKS
    if args.books:
        wanted = {s.strip() for s in args.books.split(",") if s.strip()}
        selected = [b for b in BOOKS if b["slug"] in wanted]
        if not selected:
            print("error: no known book slugs selected", file=sys.stderr)
            return 2

    data = build(selected, args.limit_pages)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    c = data["counts"]
    print(
        f"OK: {c['books']} books, {c['key_terms_pages']} key-terms pages, "
        f"{c['term_rows']} rows, {c['unique_terms_by_domain']} unique terms -> {args.output}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
