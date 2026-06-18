import tempfile
import unittest
from pathlib import Path

from log16.storage.cards import safe_read_json, write_json

class TestSafeReadJson(unittest.TestCase):
    def test_safe_read_json_valid(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "ok.json"
            write_json(p, {"ok": True})
            self.assertEqual(safe_read_json(p), {"ok": True})

    def test_safe_read_json_invalid(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "bad.json"
            p.write_text("{bad", encoding="utf-8")
            self.assertIsNone(safe_read_json(p))

    def test_safe_read_json_missing(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "missing.json"
            self.assertIsNone(safe_read_json(p))

if __name__ == "__main__":
    unittest.main()
