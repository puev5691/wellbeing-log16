import unittest
from pathlib import Path

class TestGitHubPublicTemplates(unittest.TestCase):
    def test_templates_exist(self):
        required = [
            "CONTRIBUTING.md",
            ".github/ISSUE_TEMPLATE/config.yml",
            ".github/ISSUE_TEMPLATE/documentation_feedback.md",
            ".github/ISSUE_TEMPLATE/question_or_gap.md",
            ".github/ISSUE_TEMPLATE/local_diagnostics_report.md",
            ".github/ISSUE_TEMPLATE/task_proposal.md",
            ".github/PULL_REQUEST_TEMPLATE.md",
        ]
        for path in required:
            with self.subTest(path=path):
                self.assertTrue(Path(path).exists())

    def test_templates_contain_safety_boundaries(self):
        text = Path("CONTRIBUTING.md").read_text(encoding="utf-8")
        self.assertIn("private credentials", text)
        self.assertIn("local lab", text)
        pr = Path(".github/PULL_REQUEST_TEMPLATE.md").read_text(encoding="utf-8")
        self.assertIn("private credentials", pr)
        self.assertIn("raw internal queues", pr)

if __name__ == "__main__":
    unittest.main()
