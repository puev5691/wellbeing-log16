import tempfile
import unittest
from pathlib import Path

from log16.storage.cards import list_json_cards, move_card, read_json, write_json
from log16.storage.layout import RuntimeLayout
from log16.review.decisions import apply_review_decision

class TestCards(unittest.TestCase):
    def test_read_write_move_card(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            src = root / "a.json"
            write_json(src, {"x": 1})
            self.assertEqual(read_json(src)["x"], 1)

            dst = move_card(src, root / "done", {"status": "done"})
            self.assertFalse(src.exists())
            self.assertTrue(dst.exists())
            self.assertEqual(read_json(dst)["status"], "done")
            self.assertEqual(len(list_json_cards(root / "done")), 1)

    def test_apply_review_decision(self):
        with tempfile.TemporaryDirectory() as td:
            layout = RuntimeLayout(Path(td))
            layout.ensure()
            card = layout.responses_needs_review / "response-test.json"
            write_json(card, {
                "response_id": "response-test",
                "response_text": "hello",
            })

            result = apply_review_decision(
                card,
                layout,
                decision="approve_with_edit",
                operator_text="edited hello",
                operator_note="ok",
            )
            self.assertTrue(result.response_target_path.exists())
            self.assertTrue(result.review_json_path.exists())
            self.assertTrue(result.review_md_path.exists())
            self.assertTrue(result.reviewed_doc_path.exists())
            self.assertEqual(read_json(result.response_target_path)["review_status"], "approve_with_edit")

if __name__ == "__main__":
    unittest.main()
