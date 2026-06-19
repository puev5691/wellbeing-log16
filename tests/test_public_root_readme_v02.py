import unittest
from pathlib import Path

class TestPublicRootReadmeV02(unittest.TestCase):
    def test_v02_universal_text_field_framing(self):
        path = Path("docs/public/github-root-readme-draft-v02.md")
        self.assertTrue(path.exists())
        text = path.read_text(encoding="utf-8")

        self.assertIn("большими массивами текстовой информации", text)
        self.assertIn("БЛАГОПОЛУЧИЕ выступает первым живым полигоном", text)
        self.assertIn("любому большому текстовому массиву", text)
        self.assertIn("рабочую систему знания", text)
        self.assertIn("не является готовым публичным продуктом", text)

    def test_v02_reading_note_exists(self):
        path = Path("docs/public/github-root-readme-draft-v02-reading-note.md")
        self.assertTrue(path.exists())
        text = path.read_text(encoding="utf-8")
        self.assertIn("универсальной задаче", text)
        self.assertIn("первый реальный полигон", text)

if __name__ == "__main__":
    unittest.main()
