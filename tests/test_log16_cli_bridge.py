import unittest

from log16.cli.main import build_parser

class TestLog16CliBridge(unittest.TestCase):
    def test_parse_pult_bridge(self):
        parser = build_parser()
        args = parser.parse_args(["pult", "status", "--cleanup"])
        self.assertEqual(args.command, "pult")
        self.assertEqual(args.args, ["status", "--cleanup"])

    def test_parse_answer_bridge(self):
        parser = build_parser()
        args = parser.parse_args(["answer", "test question"])
        self.assertEqual(args.command, "answer")
        self.assertEqual(args.text, "test question")

    def test_parse_dashboard_bridge(self):
        parser = build_parser()
        args = parser.parse_args(["dashboard"])
        self.assertEqual(args.command, "dashboard")

if __name__ == "__main__":
    unittest.main()
