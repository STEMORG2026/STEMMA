#!/usr/bin/env python3
"""Generate original entity drafts from the OpenStax term inventory.

This is a *draft* generator. It never copies OpenStax prose and never sets
canonical status. Definitions are written by a local model from a term plus a
short reference excerpt; the reference is attached only as verification
evidence. Promotion happens in scripts/promote_delegated.py (ADR-0060).

Usage:
    python3 scripts/generate_openstax_content.py --limit 25 --dry-run
    python3 scripts/generate_openstax_content.py --domain physics --limit 50
    python3 scripts/generate_openstax_content.py --domain mathematics --subdomain calculus --limit 40
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
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
INVENTORY = ROOT / "state" / "content-inventory.json"
CACHE = ROOT / "state" / "cache" / "llm-definitions.json"
CONTENT = ROOT / "content"
OLLAMA = "http://localhost:11434/api/generate"
MODEL = "qwen3.5:9b"
CACHE_VERSION = "v2"
WRITER = "process:openstax-importer.v1"
TYPES = {
    "concept", "quantity", "unit", "constant", "law", "principle", "theorem",
    "equation", "operator", "function", "distribution", "misconception",
    "phenomenon", "process", "structure", "system", "material", "reaction",
    "organelle", "model", "experiment", "technique", "instrument", "algorithm",
    "data-structure", "protocol", "standard", "dataset", "mission",
}
LEVELS = {"foundational", "intermediate", "advanced"}
DRAFTER = "llm:qwen3.5-9b"

PREFIX = {
    "physics": "phys",
    "chemistry": "chem",
    "biology": "bio",
    "earth-space": "earth",
    "engineering": "eng",
    "mathematics": "math",
}
DIRECTORY = {
    "physics": "physics",
    "chemistry": "chemistry",
    "biology": "biology",
    "earth-space": "earth-space",
    "engineering": "engineering",
    "mathematics": "math",
}

PRIORITY = {
    "physics": [
        "force", "velocity", "acceleration", "momentum", "energy", "work", "power",
        "newton's second law", "newton's first law", "newton's third law", "gravity",
        "electric charge", "electric current", "voltage", "resistance", "ohm's law",
        "wave", "wavelength", "frequency", "temperature", "heat", "pressure",
        "entropy", "first law of thermodynamics", "second law of thermodynamics",
        "kinetic energy", "potential energy", "conservation of energy", "friction",
        "torque", "angular momentum", "magnetic field", "electric field",
        "electric potential", "capacitance", "resistance", "electric power",
        "power", "impulse", "elastic collision", "inelastic collision", "center of mass",
        "moment of inertia", "simple harmonic motion", "wavelength", "frequency",
        "reflection", "refraction", "diffraction", "interference", "sound", "wave",
        "average speed", "instantaneous velocity", "free fall",
    ],
    "chemistry": [
        "atom", "molecule", "ion", "covalent bond", "ionic bond", "mole", "molarity",
        "stoichiometry", "oxidation", "reduction", "acid", "base", "ph", "equilibrium",
        "enthalpy", "entropy", "gibbs free energy", "reaction rate", "catalyst",
        "solution", "solvent", "solute", "electron", "proton", "neutron",
        "periodic table", "electronegativity", "chemical reaction", "precipitate",
        "buffer", "titration", "organic compound", "molar mass", "molecular formula",
        "empirical formula", "chemical equation", "limiting reactant", "percent yield",
        "specific heat", "calorimetry", "bond energy", "lone pair", "resonance",
        "intermolecular force", "hydrogen bond", "dipole", "oxidation number", "redox",
        "galvanic cell", "electrolysis", "half-life",
    ],
    "biology": [
        "cell", "dna", "rna", "protein", "gene", "chromosome", "mitosis", "meiosis",
        "enzyme", "metabolism", "photosynthesis", "cellular respiration", "evolution",
        "natural selection", "ecosystem", "neuron", "hormone", "homeostasis",
        "organelle", "membrane", "ribosome", "mitochondrion", "allele", "genotype",
        "phenotype", "transcription", "translation", "mutation", "species", "population",
        "food chain", "immune system", "cell membrane", "cytoplasm", "nucleus",
        "chloroplast", "tissue", "organ", "organism", "biodiversity", "carrying capacity",
        "food web", "symbiosis", "adaptation", "speciation", "genetic drift",
        "gene expression", "replication", "nucleotide", "amino acid", "prokaryote",
        "eukaryote", "virus", "bacteria", "fungus",
    ],
    "mathematics": [
        "function", "limit", "derivative", "integral", "sequence", "series", "vector",
        "matrix", "probability", "distribution", "mean", "variance", "theorem",
        "polynomial", "exponential function", "logarithm", "trigonometric function",
        "differential equation", "linear transformation", "eigenvalue", "random variable",
        "hypothesis test", "confidence interval", "regression", "graph", "set",
        "relation", "permutation", "combination", "complex number", "domain", "range",
        "asymptote", "rational function", "exponential growth", "logarithmic function",
        "arithmetic sequence", "geometric sequence", "binomial theorem", "conic section",
        "ellipse", "hyperbola", "parabola", "polar coordinates", "parametric equations",
        "standard deviation", "normal distribution", "binomial distribution",
        "conditional probability", "expected value", "correlation", "linear regression",
    ],
    "earth-space": [
        "star", "galaxy", "planet", "black hole", "redshift", "parsec", "light-year",
        "stellar evolution", "big bang", "dark matter", "dark energy", "solar system",
        "orbit", "telescope", "spectroscopy", "nebula", "supernova", "neutron star",
        "exoplanet", "cosmic microwave background", "main sequence", "absolute magnitude",
        "apparent magnitude", "luminosity", "doppler effect", "comet", "meteor",
        "eclipse", "solar flare", "sunspot", "aurora", "terrestrial planet",
        "gas giant", "dwarf planet", "kuiper belt", "oort cloud", "galaxy cluster",
        "local group", "hubble law", "cosmological principle", "gravitational lensing",
        "event horizon", "accretion disk", "pulsar", "quasar", "white dwarf",
        "planetary nebula", "spectral line", "parallax",
    ],
    "engineering": [
        "algorithm", "data structure", "complexity", "database", "network", "protocol",
        "software development lifecycle", "requirement", "unit testing", "integration testing",
        "abstraction", "encapsulation", "inheritance", "polymorphism", "compiler",
        "operating system", "version control", "api", "serialization", "caching",
        "load balancing", "encryption", "authentication", "authorization", "machine learning",
        "neural network", "data pipeline", "relational database", "query", "index",
        "distributed system", "concurrency", "requirements engineering",
        "software architecture", "design pattern", "debugging", "refactoring",
        "code review", "continuous integration", "deployment", "api", "serialization",
        "caching", "load balancing", "relational database", "query", "schema",
        "normalization", "transaction", "index", "integration testing", "interface",
        "software development lifecycle", "requirement", "test-driven development",
        "dependency", "refactoring", "continuous integration", "deployment",
        "relational database", "query", "distributed system", "load balancing",
        "stack", "tree", "heapsort algorithm", "binary search algorithm", "hash table",
        "linked list", "array list", "recursion", "memory", "graph",
        "depth-first search", "breadth-first search", "merge sort",
        "minimum spanning tree", "Dijkstra’s algorithm", "greedy algorithm",
        "divide and conquer algorithm", "asymptotic analysis", "interpreter",
        "thread", "process", "virtual memory",
    ],
}

BOOK_PRIORITY = [
    "university-physics-volume-1",
    "university-physics-volume-2",
    "university-physics-volume-3",
    "chemistry-2e",
    "organic-chemistry",
    "biology-2e",
    "anatomy-and-physiology-2e",
    "microbiology",
    "astronomy-2e",
    "calculus-volume-1",
    "calculus-volume-2",
    "calculus-volume-3",
    "precalculus-2e",
    "algebra-and-trigonometry-2e",
    "college-algebra-2e",
    "introductory-statistics-2e",
    "introduction-computer-science",
    "introduction-python-programming",
    "principles-data-science",
    "additive-manufacturing-essentials",
    "college-physics-2e",
    "physics",
]
STOP_TERMS = {
    "introduction", "summary", "review", "key terms", "chapter", "section",
    "learning objectives", "answer", "figure", "table", "exercise", "problem",
    "concept check", "check your understanding", "key equations", "key concepts",
}


def normalize(term: str) -> str:
    return re.sub(r"\s+", " ", term).strip().casefold()


def slugify(value: str) -> str:
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return re.sub(r"-+", "-", value).strip("-")[:80]


def existing_names() -> tuple[set[str], set[str]]:
    names: set[str] = set()
    ids: set[str] = set()
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
            if data.get("name"):
                names.add(normalize(str(data["name"])))
            if data.get("id"):
                ids.add(str(data["id"]))
    return names, ids


def infer_type(term: str) -> str:
    t = f" {term.lower()} "
    rules = [
        (" law", "law"), ("law of", "law"), (" theorem", "theorem"),
        (" principle", "principle"), (" constant", "constant"),
        (" equation", "equation"), (" algorithm", "algorithm"),
        (" reaction", "reaction"), (" process", "process"),
        (" model", "model"), (" experiment", "experiment"),
        (" organelle", "organelle"), (" material", "material"),
        (" system", "system"), (" structure", "structure"),
        (" distribution", "distribution"), (" function", "function"),
        (" operator", "operator"), (" protocol", "protocol"),
        (" standard", "standard"), (" instrument", "instrument"),
        (" technique", "technique"), (" method", "technique"),
    ]
    for needle, kind in rules:
        if needle in t:
            return kind
    return "concept"



def physics_route(term: str) -> tuple[str, list[str]] | None:
    """Map a physics term to a subdomain that has a registered governing law.

    The OpenStax physics books are all tagged `general`, which the governing
    check rejects. Terms that do not fit a registered law are skipped rather
    than placed in the wrong subdomain.
    """
    t = f" {term.lower()} "
    if any(k in t for k in (" quantum", " orbital", " atomic", " nuclear", " relativ",
                            " photon", " electron", " particle", " binding energy",
                            " nucleon", " radioactivity", " radioactive", " half-life",
                            " nuclear", " fission", " fusion", " isotope")):
        return None
    if "first law of thermodynamics" in t:
        return "thermal-physics", ["stemma:phys.zeroth-law-thermodynamics", "stemma:phys.ideal-gas-law"]
    if "second law of thermodynamics" in t:
        return "thermal-physics", ["stemma:phys.first-law-thermodynamics", "stemma:phys.zeroth-law-thermodynamics"]
    if "entropy" in t:
        return "thermal-physics", ["stemma:phys.second-law-thermodynamics"]
    if "heat" in t:
        return "thermal-physics", ["stemma:phys.first-law-thermodynamics", "stemma:phys.zeroth-law-thermodynamics"]
    if "pressure" in t or "ideal gas" in t or " gas " in t:
        return "thermal-physics", ["stemma:phys.ideal-gas-law"]
    if any(k in t for k in (" temperature", " thermal", " thermodynamic", " zero")):
        return "thermal-physics", ["stemma:phys.zeroth-law-thermodynamics", "stemma:phys.ideal-gas-law"]
    if any(k in t for k in (" force", " motion", " acceleration", " velocity", " momentum", " energy", " work", " torque", " friction", " gravity", " mass", " collision", " rotation")):
        return "mechanics", ["stemma:phys.newtons-second-law", "stemma:phys.conservation-energy"]
    if any(k in t for k in (" charge", " current", " voltage", " electric", " magnetic", " resistor", " capacitor", " inductor", " circuit", " ohm", " coulomb", " farad")):
        return "electricity-magnetism", ["stemma:phys.coulombs-law", "stemma:phys.faraday-law"]
    return None

def cache_key(term: str, reference: str) -> str:
    return hashlib.sha256(f"{CACHE_VERSION}\n{normalize(term)}\n{reference}".encode("utf-8")).hexdigest()


def load_cache() -> dict[str, dict[str, str]]:
    if CACHE.exists():
        return json.loads(CACHE.read_text(encoding="utf-8"))
    return {}


def save_cache(cache: dict[str, dict[str, str]]) -> None:
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(cache, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def llm_batch(items: list[dict[str, str]], cache: dict[str, dict[str, str]]) -> dict[str, dict[str, str]]:
    pending = [it for it in items if cache_key(it["term"], it["reference_definition"]) not in cache]
    if not pending:
        return cache
    lines = []
    for i, it in enumerate(pending, 1):
        lines.append(f"{i}. {it['term']}: {it['reference_definition']}")
    prompt = (
        "You are writing original definitions for a canonical STEM knowledge base. "
        "For each numbered term, write a definition of 30 to 65 words (usually two sentences). "
        "The first sentence must say what the term is; the second must give its key property, "
        "role, or a necessary distinction. Write at undergraduate level and use your own wording. "
        "Do not copy phrases of more than six words from the reference. Do not invent numbers "
        "or facts that the reference does not support. Also classify the term as exactly one of: "
        "concept, quantity, unit, constant, law, principle, theorem, equation, operator, "
        "function, distribution, misconception, phenomenon, process, structure, system, "
        "material, reaction, organelle, model, experiment, technique, instrument, algorithm, "
        "data-structure, protocol, standard, dataset, mission. "
        "Classify level as foundational, intermediate, or advanced. Return ONLY valid JSON: "
        '{"items":[{"term":"...","definition":"...","type":"...","level":"..."}]} with the same terms.\n\n'
        "Terms:\n" + "\n".join(lines)
    )
    payload = json.dumps({
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "think": False,
        "format": "json",
        "options": {"temperature": 0.1, "num_predict": 2500, "num_ctx": 8192},
    }).encode("utf-8")
    req = urllib.request.Request(OLLAMA, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(f"ollama request failed: {exc}") from exc
    raw = (body.get("response") or "").strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"model returned invalid JSON: {raw[:300]}") from exc
    out = parsed.get("items") if isinstance(parsed, dict) else None
    if not isinstance(out, list):
        raise RuntimeError("model JSON has no items array")
    by_term = {normalize(str(x.get("term", ""))): x for x in out if isinstance(x, dict)}
    for it in pending:
        row = by_term.get(normalize(it["term"]))
        if not row:
            continue
        definition = str(row.get("definition", "")).strip()
        if not definition:
            continue
        kind = str(row.get("type", "")).strip().lower()
        if kind in {"quantity", "unit"}:
            # Dimensional classification needs quantity_kind, tensor_character and a
            # non-empty dimension class. Keep drafts at concept level until that
            # enrichment exists rather than emitting a half-specified quantity.
            kind = "concept"
        level = str(row.get("level", "")).strip().lower()
        cache[cache_key(it["term"], it["reference_definition"])] = {
            "definition": definition,
            "type": kind if kind in TYPES else infer_type(it["term"]),
            "level": level if level in LEVELS else (it["book"].get("level") or "intermediate"),
        }
    return cache


def select_terms(domain: str | None, subdomain: str | None, limit: int | None) -> list[dict[str, Any]]:
    data = json.loads(INVENTORY.read_text(encoding="utf-8"))
    priority = {slug: i for i, slug in enumerate(BOOK_PRIORITY)}
    chosen: dict[tuple[str, str], dict[str, Any]] = {}
    for book in data.get("books") or []:
        if domain and book.get("domain") != domain:
            continue
        if subdomain and book.get("subdomain") != subdomain:
            continue
        rank = priority.get(book["slug"], 999)
        for term in book.get("terms") or []:
            name = str(term.get("term", "")).strip()
            if not name or normalize(name) in STOP_TERMS or len(name) < 3:
                continue
            if book["domain"] == "physics" and physics_route(name) is None:
                continue
            key = (book["domain"], normalize(name))
            candidate = {
                "term": name,
                "reference_definition": term.get("reference_definition", ""),
                "book": book,
                "url": term.get("url", book.get("url", "")),
                "rank": rank,
            }
            if key not in chosen or rank < chosen[key]["rank"]:
                chosen[key] = candidate
    rank = {normalize(t): i for i, t in enumerate(PRIORITY.get(domain or "", []))}
    rows = sorted(
        chosen.values(),
        key=lambda x: (
            0 if normalize(x["term"]) in rank else 1,
            rank.get(normalize(x["term"]), 0),
            x["book"]["domain"],
            normalize(x["term"]),
        ),
    )
    return rows[:limit] if limit else rows


def definition_for(item: dict[str, Any], cache: dict[str, dict[str, str]]) -> dict[str, str] | None:
    return cache.get(cache_key(item["term"], item["reference_definition"]))


def write_entity(item: dict[str, Any], definition: dict[str, str], used_ids: set[str], used_slugs: set[str]) -> Path:
    book = item["book"]
    domain = book["domain"]
    prefix = PREFIX[domain]
    slug = slugify(item["term"]) or "concept"
    base = slug
    n = 2
    while f"{prefix}.{slug}" in used_slugs:
        slug = f"{base}-{n}"
        n += 1
    used_slugs.add(f"{prefix}.{slug}")
    entity_id = f"stemma:{prefix}.{slug}"
    while entity_id in used_ids:
        entity_id = f"stemma:{prefix}.{slug}-{n}"
        n += 1
    used_ids.add(entity_id)

    subdomain = book["subdomain"]
    governed_by = None
    if domain == "physics":
        route = physics_route(item["term"])
        if route is None:
            raise ValueError(f"no physics route for {item['term']}")
        subdomain, governed_by = route
    source_id = f"stemma:src.openstax-{book['slug']}"
    entity = {
        "id": entity_id,
        "type": definition.get("type") if definition.get("type") in TYPES else infer_type(item["term"]),
        "name": item["term"],
        "domain": domain,
        "subdomain": subdomain,
        "level": definition.get("level") if definition.get("level") in LEVELS else (book.get("level") or "intermediate"),
        "status": "draft",
        "definition": definition["definition"].strip(),
        "examples": [],
        "same_dimensional_quantities": None,
        "source_refs": [source_id],
        "provenance": {
            "ai_drafted": True,
            "source_kind": "textbook",
            "source": (
                f"{book['title']} ({book.get('year') or 'n.d.'}), OpenStax. "
                f"Term locator: {item.get('url')}. Used as a reference; definition independently phrased."
            ),
            "writer": WRITER,
            "drafted_by": DRAFTER,
            "original_author": ", ".join(book.get("authors") or ["OpenStax"]),
            "link": item.get("url") or book.get("url"),
            "retrieved_at": book.get("retrieved_at") or "2026-10-20",
        },
    }
    if governed_by:
        entity["governed_by"] = governed_by
    if entity["type"] == "concept":
        entity.pop("examples")
    body = definition["definition"].strip() + "\n"
    text = "---\n" + yaml.safe_dump(entity, sort_keys=False, allow_unicode=True, width=100) + "---\n\n" + body
    path = CONTENT / DIRECTORY[domain] / subdomain / f"{slug}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate OpenStax-derived entity drafts")
    parser.add_argument("--domain", choices=sorted(PREFIX), help="filter by domain")
    parser.add_argument("--subdomain", help="filter by subdomain")
    parser.add_argument("--limit", type=int, default=25)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--batch-size", type=int, default=10)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    rows = select_terms(args.domain, args.subdomain, None)
    names, ids = existing_names()
    rows = [r for r in rows if normalize(r["term"]) not in names]
    rows = rows[args.offset: args.offset + args.limit]
    if not rows:
        print("OK: no new terms selected")
        return 0
    if args.dry_run:
        for r in rows:
            print(f"{r['book']['domain']:12} {r['book']['subdomain']:22} {r['term']}")
        print(f"OK: {len(rows)} terms (dry run)")
        return 0

    cache = load_cache()
    for start in range(0, len(rows), args.batch_size):
        batch = rows[start:start + args.batch_size]
        try:
            cache = llm_batch(batch, cache)
        except RuntimeError as exc:
            print(f"FAIL: batch {start}: {exc}", file=sys.stderr)
            continue
        save_cache(cache)

    written = 0
    used_slugs: set[str] = set()
    for row in rows:
        definition = definition_for(row, cache)
        if not definition:
            print(f"SKIP: no definition for {row['term']}", file=sys.stderr)
            continue
        if len(definition.get("definition", "")) < 70:
            print(f"SKIP: definition too short for {row['term']}", file=sys.stderr)
            continue
        path = write_entity(row, definition, ids, used_slugs)
        written += 1
        print(f"OK: {path.relative_to(ROOT)}")
    print(f"OK: {written} drafts written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
