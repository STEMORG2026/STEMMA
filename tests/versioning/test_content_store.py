"""Content-addressed manifest invariants (R8)."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import content_store  # noqa: E402


def test_merkle_root_is_order_sensitive_and_deterministic():
    a = content_store.leaf_hash("a.md", b"alpha")
    b = content_store.leaf_hash("b.md", b"beta")
    assert content_store.merkle_root([a, b]) == content_store.merkle_root([a, b])
    assert content_store.merkle_root([a, b]) != content_store.merkle_root([b, a])
    assert content_store.merkle_root([]) == content_store.sha256_bytes(b"")


def test_manifest_matches_tree_without_mutation():
    current = content_store.build()
    manifest = json.loads((ROOT / "exports" / "content-manifest.json").read_text(encoding="utf-8"))
    assert current["root"] == manifest["root"]
    assert current["file_count"] == manifest["file_count"]


def test_check_detects_a_changed_file():
    manifest = json.loads((ROOT / "exports" / "content-manifest.json").read_text(encoding="utf-8"))
    changed = json.loads(json.dumps(manifest))
    changed["files"][0]["sha256"] = "0" * 64
    problems = content_store.check(changed)
    assert any("hash mismatch" in problem for problem in problems)
