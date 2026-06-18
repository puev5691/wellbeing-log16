import unittest
import tempfile
from pathlib import Path

from log16.storage.cards import write_json
from log16.storage.layout import RuntimeLayout
from log16.storage.status import status_counts

class TestStatusCounts(unittest.TestCase):
    def test_status_counts_live_layout_names(self):
        with tempfile.TemporaryDirectory() as td:
            layout = RuntimeLayout(Path(td))
            layout.ensure()

            write_json(layout.themes_captured / "theme.json", {"x": 1})
            write_json(layout.tasks_proposed / "task.json", {"x": 1})
            write_json(layout.requests_pending / "request.json", {"x": 1})
            write_json(layout.responses_needs_review / "response.json", {"x": 1})
            write_json(layout.responses_approved / "approved.json", {"x": 1})
            (layout.root / "runner-reports" / "run-1").mkdir(parents=True)

            counts = status_counts(layout)

            self.assertEqual(counts["themes"], 1)
            self.assertEqual(counts["tasks_proposed"], 1)
            self.assertEqual(counts["requests_pending"], 1)
            self.assertEqual(counts["responses_review"], 1)
            self.assertEqual(counts["responses_approved"], 1)
            self.assertEqual(counts["runner_reports"], 1)

if __name__ == "__main__":
    unittest.main()
