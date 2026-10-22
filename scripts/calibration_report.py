#!/usr/bin/env python3
"""R7 — calibration report from real review data (ADR-0058).

Writes `reports/calibration.{json,md}` from measured review activity only:

- current corpus: review-state transitions recorded in canonical connection
  histories + reviewed/canonical entities with `provenance.reviewed_at`;
- archived pilot: the historical 36 -> 12 result, labelled as historical.

It never estimates a quality score, never extrapolates, and never writes a
timestamp. Below the ADR-0058 threshold it states that the sample is not
representative instead of presenting a rate as a calibration.

Usage:
  python3 scripts/calibration_report.py
  python3 scripts/calibration_report.py --check
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from atomic_write import write_text_atomic  # noqa: E402
import review_data  # noqa: E402

EXPORT_PATH = ROOT / "exports" / "knowledge.json"
JSON_PATH = ROOT / "reports" / "calibration.json"
MD_PATH = ROOT / "reports" / "calibration.md"


def build() -> dict:
    export = json.loads(EXPORT_PATH.read_text(encoding="utf-8"))
    stats = review_data.decision_stats()
    pilot = review_data.historical_pilot()
    accepted_rate = (round(stats["accepted"] / stats["decisions_total"], 4)
                     if stats["decisions_total"] else None)
    return {
        "report_version": "1.0.0",
        "source_content_hash": export["content_hash"],
        "export_version": export["export_version"],
        "method": {
            "decision_unit": "review-state transition (from != to) or reviewed entity with provenance.reviewed_at",
            "excluded": "no-op transitions (reviewed -> reviewed) and unlabeled worksheet rows",
            "threshold": stats["threshold"],
        },
        "current_corpus": {
            "decisions_total": stats["decisions_total"],
            "distinct_objects": stats["distinct_objects"],
            "accepted": stats["accepted"],
            "rejected": stats["rejected"],
            "demoted": stats["demoted"],
            "accepted_transition_rate": accepted_rate,
            "corrections_labeled": stats["corrections_labeled"],
            "domains_with_decisions": stats["domains_with_decisions"],
            "domains": stats["domains"],
            "by_domain": stats["by_domain"],
        },
        "historical_pilot": pilot,
        "verdict": (
            "representative sample" if stats["threshold"]["met"]
            else "INSUFFICIENT — below the ADR-0058 activation threshold; "
                 "accepted_transition_rate is descriptive, not a calibration"
        ),
        "limitations": [
            "Accepted transitions include reviewed and canonical stages; they are not independent samples.",
            "The archived pilot belongs to a retired corpus and is shown as history, not current quality.",
            "No rejected-with-correction decision exists in the current corpus, so correction calibration is not measurable.",
        ],
    }


def render_md(report: dict) -> str:
    current = report["current_corpus"]
    threshold = report["method"]["threshold"]
    lines = [
        "# Calibration Report — R7",
        "",
        f"- Source export: `{report['source_content_hash']}` (v{report['export_version']})",
        f"- Decision unit: {report['method']['decision_unit']}",
        f"- Excluded: {report['method']['excluded']}",
        "",
        "## Current corpus (measured)",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Labeled decisions | **{current['decisions_total']}** |",
        f"| Distinct reviewed objects | {current['distinct_objects']} |",
        f"| Accepted transitions | {current['accepted']} |",
        f"| Rejected transitions | {current['rejected']} |",
        f"| Demotions | {current['demoted']} |",
        f"| Accepted-transition rate (descriptive) | {current['accepted_transition_rate'] if current['accepted_transition_rate'] is not None else 'n/a'} |",
        f"| Corrected with `correction_class` | {current['corrections_labeled']} |",
        f"| Domains with decisions | **{current['domains_with_decisions']}** ({', '.join(current['domains']) or 'none'}) |",
        "",
        "### By domain",
        "",
        "| Domain | Decisions | Accepted | Rejected | Demoted |",
        "|---|---|---|---|---|",
    ]
    for domain, row in sorted(current["by_domain"].items()):
        lines.append(f"| {domain} | {row['decisions']} | {row['accepted']} | {row['rejected']} | {row['demoted']} |")
    if not current["by_domain"]:
        lines.append("| — | 0 | 0 | 0 | 0 |")
    lines += [
        "",
        "## Threshold (ADR-0058)",
        "",
        f"- Required: **{threshold['decisions_required']}** labeled decisions across **{threshold['domains_required']}** domains",
        f"- Observed: {current['decisions_total']} decisions across {current['domains_with_decisions']} domain(s)",
        f"- Decisions met: **{threshold['decisions_met']}** · Domains met: **{threshold['domains_met']}** · Activated: **{threshold['met']}**",
        "",
        f"**Verdict:** {report['verdict']}",
        "",
        "## Historical pilot (archived corpus)",
        "",
    ]
    pilot = report["historical_pilot"]
    if pilot.get("available"):
        lines += [
            f"Source: `{pilot['source']}` — {pilot['corpus']}.",
            "",
            "| Metric | Value |",
            "|---|---|",
            f"| Proposals | {pilot['proposals']} |",
            f"| Curated accepted | {pilot['accepted']} |",
            f"| Acceptance rate | {pilot['acceptance_rate']} |",
            f"| Auto-canonicalized | {pilot['auto_canonicalized']} |",
        ]
    else:
        lines.append("No archived pilot report found.")
    lines += ["", "## Limitations", ""]
    lines += [f"- {item}" for item in report["limitations"]]
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="R7 calibration report from measured review data")
    parser.add_argument("--check", action="store_true", help="verify committed report is fresh")
    args = parser.parse_args(argv)
    report = build()
    json_text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    md_text = render_md(report)
    if args.check:
        stale = []
        for path, text in ((JSON_PATH, json_text), (MD_PATH, md_text)):
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                stale.append(str(path.relative_to(ROOT)))
        if stale:
            print("FAIL: calibration report is stale — run python3 scripts/calibration_report.py", file=sys.stderr)
            for rel in stale:
                print(f"  - {rel}", file=sys.stderr)
            return 1
        print("OK: calibration report fresh")
        return 0
    write_text_atomic(JSON_PATH, json_text)
    write_text_atomic(MD_PATH, md_text)
    current = report["current_corpus"]
    print(f"OK: calibration — {current['decisions_total']} decisions across "
          f"{current['domains_with_decisions']} domain(s); threshold met: "
          f"{report['method']['threshold']['met']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
