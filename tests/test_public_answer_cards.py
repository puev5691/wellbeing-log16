import json
import unittest
from pathlib import Path

class TestPublicAnswerCards(unittest.TestCase):
    def test_all_cards_match_schema_like_contract(self):
        schema = json.loads(Path("schemas/public-answer-card-v01.schema.json").read_text(encoding="utf-8"))
        required = schema["required"]
        cards = sorted(Path("docs/public/knowledge-base/answers").glob("*.json"))

        self.assertGreaterEqual(len(cards), 7)

        for path in cards:
            with self.subTest(path=str(path)):
                data = json.loads(path.read_text(encoding="utf-8"))
                for key in required:
                    self.assertIn(key, data)
                self.assertEqual(data["schema_version"], "public-answer-card-v01")
                self.assertIn(data["status"], schema["status_values"])
                self.assertIn(data["source_status"], schema["source_status_values"])
                self.assertIn(data["review_level"], schema["review_level_values"])

if __name__ == "__main__":
    unittest.main()
