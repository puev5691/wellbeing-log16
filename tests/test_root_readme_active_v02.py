import unittest
from pathlib import Path

class TestRootReadmeActiveV02(unittest.TestCase):
    def test_root_readme_matches_v02_draft(self):
        root = Path("README.md")
        draft = Path("docs/public/github-root-readme-draft-v02.md")
        self.assertTrue(root.exists())
        self.assertTrue(draft.exists())
        self.assertEqual(root.read_text(encoding="utf-8"), draft.read_text(encoding="utf-8"))

    def test_root_readme_contains_universal_framing(self):
        text = Path("README.md").read_text(encoding="utf-8")
        self.assertIn("большими массивами текстовой информации", text)
        self.assertIn("БЛАГОПОЛУЧИЕ выступает первым живым полигоном", text)
        self.assertIn("любому большому текстовому массиву", text)
        self.assertIn("рабочую систему знания", text)
        self.assertIn("не является готовым публичным продуктом", text)

if __name__ == "__main__":
    unittest.main()
