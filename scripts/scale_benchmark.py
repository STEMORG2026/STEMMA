#!/usr/bin/env python3
"""Reproducible scale benchmark for the sharded-file corpus.

Builds a throwaway git repository with N synthetic entity files, measures the
operations that dominate the authoring loop, and records medians. It never
touches the real repository and requires no network.

Usage:
    python3 scripts/scale_benchmark.py
    python3 scripts/scale_benchmark.py --entities 2000 --repeats 2
"""
from __future__ import annotations

import argparse
import json
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAINS = [
    ("physics", "mechanics"), ("physics", "thermal-physics"),
    ("chemistry", "general"), ("chemistry", "organic-chemistry"),
    ("biology", "general"), ("biology", "physiology"),
    ("earth-space", "astronomy"), ("mathematics", "calculus"),
    ("mathematics", "algebra"), ("engineering", "computer"),
    ("engineering", "mechanical"), ("engineering", "data-engineering"),
]


def entity_text(i: int) -> str:
    domain, subdomain = DOMAINS[i % len(DOMAINS)]
    slug = f"synthetic-{i:05d}"
    return (
        "---\n"
        f"id: stemma:bench.{slug}\n"
        "type: concept\n"
        f"name: Synthetic concept {i}\n"
        f"domain: {domain}\n"
        f"subdomain: {subdomain}\n"
        "level: intermediate\n"
        "status: draft\n"
        f"definition: Synthetic benchmark entity {i} used only to measure file and git scaling.\n"
        "same_dimensional_quantities: null\n"
        "source_refs:\n- stemma:src.benchmark-fixture\n"
        "provenance:\n  ai_drafted: true\n  writer: process:scale-benchmark.v1\n"
        "---\n\n"
        f"Synthetic benchmark entity {i}. No scientific claim is made.\n"
    )


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-c", "user.name=stemma-bench", "-c", "user.email=bench@example.invalid", *args],
        cwd=repo, capture_output=True, text=True,
    )


def timed(fn) -> float:
    start = time.perf_counter()
    fn()
    return time.perf_counter() - start


def run(entities: int, repeats: int) -> dict:
    with tempfile.TemporaryDirectory(prefix="stemma-scale-") as tmp:
        repo = Path(tmp) / "repo"
        repo.mkdir()
        git(repo, "init", "-q")

        def write_all() -> None:
            for i in range(entities):
                domain, subdomain = DOMAINS[i % len(DOMAINS)]
                path = repo / "content" / domain / subdomain / f"synthetic-{i:05d}.md"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(entity_text(i), encoding="utf-8")

        write_s = timed(write_all)
        add_s = timed(lambda: git(repo, "add", "-A"))
        commit_s = timed(lambda: git(repo, "commit", "-q", "-m", "benchmark corpus"))

        status_times = [timed(lambda: git(repo, "status", "--porcelain")) for _ in range(repeats)]

        def edit_sample() -> None:
            for i in range(0, entities, 100):
                domain, subdomain = DOMAINS[i % len(DOMAINS)]
                path = repo / "content" / domain / subdomain / f"synthetic-{i:05d}.md"
                with path.open("a", encoding="utf-8") as fh:
                    fh.write("\n<!-- benchmark edit -->\n")

        edit_s = timed(edit_sample)
        diff_times = [timed(lambda: git(repo, "diff", "--stat")) for _ in range(repeats)]

        def read_pass() -> int:
            count = 0
            for path in sorted((repo / "content").rglob("*.md")):
                text = path.read_text(encoding="utf-8")
                if text.startswith("---\n") and "status: draft" in text:
                    count += 1
            return count

        read_times = [timed(read_pass) for _ in range(repeats)]
        parsed = read_pass()
        total_bytes = sum(p.stat().st_size for p in (repo / "content").rglob("*.md"))

        return {
            "dataset": f"scale-{entities}",
            "entities": entities,
            "repeats": repeats,
            "timings_seconds": {
                "write_files": round(write_s, 4),
                "git_add": round(add_s, 4),
                "git_commit": round(commit_s, 4),
                "git_status_median": round(statistics.median(status_times), 4),
                "edit_sample": round(edit_s, 4),
                "git_diff_stat_median": round(statistics.median(diff_times), 4),
                "validation_shaped_read_median": round(statistics.median(read_times), 4),
            },
            "derived": {
                "written_per_second": round(entities / write_s, 1) if write_s else None,
                "status_per_second": round(entities / statistics.median(status_times), 1)
                if statistics.median(status_times) else None,
                "content_bytes": total_bytes,
                "bytes_per_entity": round(total_bytes / entities, 1) if entities else None,
                "records_read": parsed,
            },
            "limits": [
                "single local filesystem and git version; timings vary by machine",
                "synthetic entities are smaller than fully sourced records",
                "no export, JSON-LD, SHACL, or ZIP bundle step is measured",
            ],
        }


def render_markdown(result: dict) -> str:
    t = result["timings_seconds"]
    d = result["derived"]
    lines = [
        "# SCALE BENCHMARK",
        "",
        f"Dataset: **{result['dataset']}** ({result['entities']} synthetic entities, "
        f"{result['repeats']} repeats for interactive checks).",
        "",
        "## Timings",
        "",
        "| Operation | Seconds |",
        "|---|---:|",
    ]
    for key, value in t.items():
        lines.append(f"| `{key}` | {value} |")
    lines += [
        "",
        "## Derived",
        "",
        f"- Write throughput: **{d['written_per_second']} files/s**",
        f"- Status throughput: **{d['status_per_second']} files/s**",
        f"- Content size: **{d['content_bytes']} bytes** ({d['bytes_per_entity']} bytes/entity)",
        f"- Records read in validation-shaped pass: **{d['records_read']}**",
        "",
        "## Limits",
        "",
    ] + [f"- {item}" for item in result["limits"]]
    lines += [
        "",
        "This benchmark is local and synthetic. It measures file/git mechanics, not",
        "scientific quality or network-bound ingestion.",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scale benchmark for sharded files")
    parser.add_argument("--entities", type=int, default=10000)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--json-out", type=Path, default=ROOT / "reports" / "scale-benchmark.json")
    parser.add_argument("--md-out", type=Path, default=ROOT / "reports" / "scale-benchmark.md")
    args = parser.parse_args(argv)
    if args.entities < 1:
        print("error: entities must be positive", file=sys.stderr)
        return 2
    result = run(args.entities, max(1, args.repeats))
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.md_out.write_text(render_markdown(result), encoding="utf-8")
    print(f"OK: {result['dataset']} — write {result['timings_seconds']['write_files']}s, "
          f"status median {result['timings_seconds']['git_status_median']}s, "
          f"read median {result['timings_seconds']['validation_shaped_read_median']}s")
    def show(path: Path) -> str:
        try:
            return str(path.relative_to(ROOT))
        except ValueError:
            return str(path)
    print(f"OK: wrote {show(args.json_out)} and {show(args.md_out)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
