import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from log16.cli.main import main
from log16.storage.layout import RuntimeLayout

class TestLog16CliCheck(unittest.TestCase):
    def test_check_json_skip_bins(self):
        with tempfile.TemporaryDirectory() as td:
            layout = RuntimeLayout(Path(td))
            layout.ensure()

            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = main(["check", "--root", td, "--json", "--skip-bins"])

            self.assertEqual(rc, 0)
            data = json.loads(buf.getvalue())
            self.assertTrue(data["ok"])

if __name__ == "__main__":
    unittest.main()
