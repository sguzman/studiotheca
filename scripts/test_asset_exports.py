"""CI tests: source protection, deterministic formats, and avatar-size boundary."""
import tempfile
import unittest
from pathlib import Path

from PIL import Image
from export_dusk_raven import build, checksum


class DuskAssetExports(unittest.TestCase):
    def test_source_guard_and_repeatability(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            src = root / "synthetic.png"
            Image.new("RGB", (1254, 1254), (82, 48, 107)).save(src)
            with self.assertRaisesRegex(ValueError, "Wrong source SHA-256"):
                build(src, root / "blocked")
            out = root / "outputs"
            first = build(src, out, verify=False)
            self.assertEqual(7, len(first["exports"]))
            self.assertEqual([512, 512], first["exports"][0]["dimensions"])
            self.assertLess((out / "avatar-full-512.png").stat().st_size, 1_000_000)
            initial_hashes = {e["file"]: e["sha256"] for e in first["exports"]}
            second = build(src, out, verify=False)
            self.assertEqual(initial_hashes, {e["file"]: e["sha256"] for e in second["exports"]})
            self.assertEqual(first["source_sha256"], checksum(src))
            self.assertFalse((out / "raven_beneath_the_violet_moon.png").exists())


if __name__ == "__main__":
    unittest.main()
