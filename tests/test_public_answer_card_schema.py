import json
import unittest
from pathlib import Path

class TestPublicAnswerCardSchema(unittest.TestCase):
    def test_example_has_required_fields(self):
        schema = json.loads(Path("schemas/public-answer-card-v01.schema.json").read_text(encoding="utf-8"))
        example = json.loads(Path("examples/public-answer-card-example.json").read_text(encoding="utf-8"))

        for key in schema["required"]:
            self.assertIn(key, example)

        self.assertEqual(example["schema_version"], "public-answer-card-v01")
        self.assertIn(example["status"], schema["status_values"])
        self.assertIn(example["source_status"], schema["source_status_values"])
        self.assertIn(example["review_level"], schema["review_level_values"])

if __name__ == "__main__":
    unittest.main()
