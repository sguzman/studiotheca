#!/usr/bin/env python3
"""Regression tests for referenced symbols and image provenance."""
import json
import tempfile
import unittest
from pathlib import Path
from validate_identity import validate


class StudioIdentityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "studio").mkdir()
        for f in ("assets.json", "decisions.md", "quality.md"):
            (self.root / "studio" / f).write_text("fixture", encoding="utf-8")
        self.model = {
            "schema": "studiotheca.studio-identity.v1",
            "id": "sample",
            "name": "Sample Studio",
            "entities": [{"id": "raven"}],
            "relations": [{"subject": "raven", "predicate": "perched_on", "object": "raven"}],
            "canonical_composition": {"required": ["raven"]},
            "palette": {"colors": [{"hex": "#123456"}]},
            "forms": [{"id": "avatar"}],
            "asset_manifest": "studio/assets.json",
            "decisions": "studio/decisions.md",
            "quality": "studio/quality.md",
        }

    def result(self):
        (self.root / "studio" / "identity.json").write_text(json.dumps(self.model), encoding="utf-8")
        return validate(self.root, "studio/identity.json", "sample")

    def test_valid(self):
        self.assertEqual([], self.result())

    def test_invalid_relation(self):
        self.model["relations"][0]["object"] = "nonexistent"
        self.assertTrue(any("unknown endpoint" in s for s in self.result()))

    def test_duplicate_symbol(self):
        self.model["entities"].append({"id": "raven"})
        self.assertTrue(any("duplicate symbol" in s for s in self.result()))

    def test_missing_source_manifest(self):
        self.model["asset_manifest"] = "studio/absent.json"
        self.assertTrue(any("asset_manifest" in s for s in self.result()))


if __name__ == "__main__":
    unittest.main()
