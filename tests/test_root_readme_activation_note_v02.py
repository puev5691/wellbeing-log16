import unittest
from pathlib import Path

class TestRootReadmeActivationNoteV02(unittest.TestCase):
    def test_activation_note_mentions_correct_paths_and_fix(self):
        path = Path("docs/productization/log16-root-readme-activation-v02.md")
        self.assertTrue(path.exists())
        text = path.read_text(encoding="utf-8")
        self.assertIn("docs/public/github-root-readme-draft-v02.md", text)
        self.assertIn("README.md", text)
        self.assertIn("unquoted heredoc", text)
        self.assertIn("Permission denied", text)
        self.assertIn("command not found", text)
        self.assertIn("СТАТУС: fixed", text)

if __name__ == "__main__":
    unittest.main()
