"""Regression tests for the OpenStax generation/promotion pipeline."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import generate_openstax_content as gen  # noqa: E402
import promote_delegated as promote  # noqa: E402


def test_priority_terms_are_selected_before_alphabetical_fill():
    rows = gen.select_terms("chemistry", None, 5)
    assert rows
    names = [gen.normalize(row["term"]) for row in rows]
    priority = [gen.normalize(term) for term in gen.PRIORITY["chemistry"]]
    assert names[0] in priority
    assert names == sorted(names, key=lambda n: priority.index(n) if n in priority else 10_000)


def test_physics_route_assigns_a_registered_law_for_thermal_terms():
    route = gen.physics_route("entropy")
    assert route is not None
    subdomain, laws = route
    assert subdomain == "thermal-physics"
    assert any(law.endswith("second-law-thermodynamics") for law in laws)


def test_physics_route_rejects_quantum_terms_without_a_registered_law():
    assert gen.physics_route("quantum number") is None


def test_no_verbatim_detects_eight_word_copy():
    reference = "A solute is a solution component present in a concentration less than that of the solvent."
    copied = promote.has_verbatim(
        "A solute is a solution component present in a concentration less than the bulk.", reference
    )
    assert copied


def test_no_verbatim_allows_independent_phrasing():
    reference = "A solute is a solution component present in a concentration less than that of the solvent."
    assert promote.has_verbatim(
        "A dissolved substance, usually the minor component, is dispersed throughout a solvent.", reference
    ) is None
