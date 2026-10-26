"""Guards for missing and modified media previews."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from validate_artwork import problems


class MediaTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "assets").mkdir()
        self.preview = self.root / "assets/thumbnail.jpg"
        self.preview.write_bytes(b"\xff\xd8\xffsynthetic-image")
        self.record = {
            "schema": "studiotheca.media-import.v1",
            "items": [{
                "id": "sample", "sha256": "a" * 64,
                "bytes": 123, "status": "verified-original; binary-not-committed",
                "intended_repository_path": "assets/original.png",
                "derivative_previews": [{
                    "file": "assets/thumbnail.jpg",
                    "sha256": hashlib.sha256(self.preview.read_bytes()).hexdigest(),
                    "bytes": self.preview.stat().st_size, "format": "image/jpeg"
                }]
            }]
        }

    def check(self):
        (self.root / "assets/import.json").write_text(json.dumps(self.record), encoding="utf-8")
        return problems(self.root, "assets/import.json")

    def test_valid_preview(self):
        self.assertEqual([], self.check())

    def test_tampered_preview(self):
        self.preview.write_bytes(b"\xff\xd8\xffaltered")
        self.assertTrue(any("SHA-256 mismatch" in x for x in self.check()))

    def test_missing_preview(self):
        self.preview.unlink()
        self.assertTrue(any("preview file missing" in x for x in self.check()))

    def test_original_wrongly_marked_absent(self):
        (self.root / "assets/original.png").write_bytes(b"unsafe data")
        self.assertTrue(any("original exists but still marked absent" in x for x in self.check()))


if __name__ == "__main__":
    unittest.main()
