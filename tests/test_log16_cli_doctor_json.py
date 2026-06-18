import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from log16.cli.main import main
from log16.storage.layout import RuntimeLayout

class TestLog16CliDoctorJson(unittest.TestCase):
    def test_doctor_json_skip_external_checks(self):
        with tempfile.TemporaryDirectory() as td:
            layout = RuntimeLayout(Path(td))
            layout.ensure()

            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = main([
                    "doctor",
                    "--repo", ".",
                    "--runtime", td,
                    "--skip-ollama",
                    "--skip-prepublish",
                    "--skip-bins",
                    "--json",
                ])

            self.assertEqual(rc, 0)
            data = json.loads(buf.getvalue())
            self.assertTrue(data["ok"])
            self.assertEqual(data["failures"], 0)
            self.assertIn(data["status"], {"OK", "WARN"})

if __name__ == "__main__":
    unittest.main()
