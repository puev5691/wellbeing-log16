import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from log16.cli.main import main
from log16.storage.cards import write_json
from log16.storage.layout import RuntimeLayout

class TestLog16Cli(unittest.TestCase):
    def test_status_json(self):
        with tempfile.TemporaryDirectory() as td:
            layout = RuntimeLayout(Path(td))
            layout.ensure()
            write_json(layout.responses_needs_review / "response.json", {"x": 1})

            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = main(["status", "--root", td, "--json"])

            self.assertEqual(rc, 0)
            data = json.loads(buf.getvalue())
            self.assertEqual(data["responses_review"], 1)

    def test_paths(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = main(["paths"])
        self.assertEqual(rc, 0)
        data = json.loads(buf.getvalue())
        self.assertIn("runtime_root", data)

if __name__ == "__main__":
    unittest.main()
