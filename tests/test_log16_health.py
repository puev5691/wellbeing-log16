import tempfile
import unittest
from pathlib import Path

from log16.health.checks import checks_to_dict, run_checks
from log16.storage.layout import RuntimeLayout

class TestLog16Health(unittest.TestCase):
    def test_health_check_temp_layout_without_bins(self):
        with tempfile.TemporaryDirectory() as td:
            layout = RuntimeLayout(Path(td))
            layout.ensure()

            checks = run_checks(root=td, include_bins=False)
            data = checks_to_dict(checks)

            self.assertTrue(data["ok"])
            self.assertTrue(any(item["name"] == "runtime_root" for item in data["checks"]))

if __name__ == "__main__":
    unittest.main()
