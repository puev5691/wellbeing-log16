import json
import unittest
from pathlib import Path

class TestPublicAnswerCardLinks(unittest.TestCase):
    def test_cards_have_existing_related_docs(self):
        cards = sorted(Path("docs/public/knowledge-base/answers").glob("*.json"))
        self.assertGreaterEqual(len(cards), 7)

        for path in cards:
            with self.subTest(path=str(path)):
                data = json.loads(path.read_text(encoding="utf-8"))

                related_docs = data.get("related_docs", [])
                self.assertTrue(related_docs)

                for doc in related_docs:
                    self.assertTrue(Path(doc).exists(), doc)

                next_docs = data.get("routing", {}).get("next_docs", [])
                self.assertTrue(next_docs)

                for doc in next_docs:
                    self.assertTrue(Path(doc).exists(), doc)

if __name__ == "__main__":
    unittest.main()
