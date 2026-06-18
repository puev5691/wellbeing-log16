import tempfile
import unittest
from pathlib import Path

from log16.doctor.checks import doctor_to_dict, run_doctor
from log16.storage.layout import RuntimeLayout

class TestLog16DoctorModule(unittest.TestCase):
    def test_run_doctor_without_ollama_or_prepublish(self):
        with tempfile.TemporaryDirectory() as td:
            layout = RuntimeLayout(Path(td))
            layout.ensure()

            result = run_doctor(
                repo=".",
                runtime=td,
                include_ollama=False,
                include_prepublish=False,
                include_bins=False,
            )
            data = doctor_to_dict(result)

            self.assertTrue(data["ok"])
            self.assertIn("checks", data)
            self.assertTrue(any(item["name"] == "health_runtime_root" for item in data["checks"]))

if __name__ == "__main__":
    unittest.main()
