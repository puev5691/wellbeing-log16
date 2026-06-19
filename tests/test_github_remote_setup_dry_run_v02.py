import unittest
from pathlib import Path

class TestGitHubRemoteSetupDryRunV02(unittest.TestCase):
    def test_script_and_docs_exist(self):
        required = [
            "scripts/github-remote-setup-dry-run-v02.sh",
            "docs/productization/log16-github-remote-setup-dry-run-v02.md",
            "docs/productization/log16-github-publish-parameters-v01.md",
        ]
        for path in required:
            with self.subTest(path=path):
                self.assertTrue(Path(path).exists())

    def test_parameters_recorded(self):
        text = Path("docs/productization/log16-github-publish-parameters-v01.md").read_text(encoding="utf-8")
        self.assertIn("GitHub", text)
        self.assertIn("public", text)
        self.assertIn("wellbeing-log16", text)
        self.assertIn("git@github.com:puev5691/wellbeing-log16.git", text)
        self.assertIn("master + tags", text)

    def test_script_is_dry_run_only(self):
        text = Path("scripts/github-remote-setup-dry-run-v02.sh").read_text(encoding="utf-8")
        self.assertIn("git push --dry-run origin", text)
        self.assertIn("No real push performed", text)
        self.assertNotIn("git push origin master", text)

if __name__ == "__main__":
    unittest.main()
