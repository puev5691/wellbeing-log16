import unittest
from pathlib import Path

class TestPublicRootReadmeDraft(unittest.TestCase):
    def test_root_readme_draft_mentions_status_and_boundaries(self):
        path = Path("docs/public/github-root-readme-draft-v01.md")
        self.assertTrue(path.exists())
        text = path.read_text(encoding="utf-8")

        self.assertIn("v0.3.0-lab", text)
        self.assertIn("not ready", text)
        self.assertIn("docs/public/publication-boundary.md", text)
        self.assertIn("log16 doctor --json", text)
        self.assertIn("docs/public/navigation.md", text)

    def test_activation_note_exists(self):
        path = Path("docs/public/github-root-readme-activation-note-v01.md")
        self.assertTrue(path.exists())
        text = path.read_text(encoding="utf-8")
        self.assertIn("не перезаписывать README.md без просмотра", text)

if __name__ == "__main__":
    unittest.main()
