import unittest
from pathlib import Path

class TestGitHubPublicationPrep(unittest.TestCase):
    def test_publication_prep_files_exist(self):
        required = [
            "scripts/check-github-publication-prep.sh",
            "docs/productization/log16-github-publication-prep-v01.md",
            "docs/productization/log16-publication-decision-checklist-v01.md",
        ]
        for path in required:
            with self.subTest(path=path):
                self.assertTrue(Path(path).exists())

    def test_publication_prep_warns_no_push(self):
        text = Path("docs/productization/log16-github-publication-prep-v01.md").read_text(encoding="utf-8")
        self.assertIn("Это НЕ push", text)
        self.assertIn("не выполнять git push автоматически", text)
        self.assertIn("v0.3.3-lab", text)

    def test_decision_checklist_requires_operator_decision(self):
        text = Path("docs/productization/log16-publication-decision-checklist-v01.md").read_text(encoding="utf-8")
        self.assertIn("человеческое решение", text)
        self.assertIn("scripts/check-github-publication-prep.sh", text)
        self.assertIn("private credentials", text)

if __name__ == "__main__":
    unittest.main()
