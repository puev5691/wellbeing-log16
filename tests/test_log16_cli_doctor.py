import unittest

from log16.cli.main import build_parser

class TestLog16CliDoctor(unittest.TestCase):
    def test_parse_doctor(self):
        parser = build_parser()
        args = parser.parse_args(["doctor"])
        self.assertEqual(args.command, "doctor")

    def test_parse_doctor_overrides(self):
        parser = build_parser()
        args = parser.parse_args([
            "doctor",
            "--repo", "/tmp/repo",
            "--runtime", "/tmp/runtime",
            "--ollama-url", "http://127.0.0.1:11434",
            "--model", "qwen3:8b",
        ])
        self.assertEqual(args.command, "doctor")
        self.assertEqual(args.repo, "/tmp/repo")
        self.assertEqual(args.runtime, "/tmp/runtime")
        self.assertEqual(args.model, "qwen3:8b")

if __name__ == "__main__":
    unittest.main()
