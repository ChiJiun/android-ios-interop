import importlib.util
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "wifi_audit", Path(__file__).parents[1] / "tools" / "duchamp_wifi_source_audit.py"
)
wifi_audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wifi_audit)


class DriverSourceAuditTests(unittest.TestCase):
    def test_empty_tree_reports_missing_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = wifi_audit.analyze(Path(tmp))
            self.assertEqual(report["source_completeness"], "incomplete")
            self.assertEqual(len(report["missing"]), 3)
            self.assertFalse(report["rf_tx_rx_verified"])

    def test_full_paths_still_do_not_claim_rf_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            chip = root / "chips" / "soc7_0"
            chip.mkdir(parents=True)
            (chip / "soc7_0.c").write_text("/* synthetic fixture */")
            headers = root / "include" / "chips" / "coda" / "soc7_0"
            headers.mkdir(parents=True)
            (headers / "header.h").write_text("/* synthetic fixture */")
            (root / "Makefile").write_text("SOC7_0 := y\n")
            report = wifi_audit.analyze(root)
            self.assertEqual(report["source_completeness"], "candidate_complete")
            self.assertFalse(report["rf_tx_rx_verified"])
            self.assertFalse(report["awdl_interoperability_verified"])

    def test_comment_only_makefile_is_not_wiring(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            chip = root / "chips" / "soc7_0"
            chip.mkdir(parents=True)
            (chip / "soc7_0.c").write_text("/* fixture */")
            headers = root / "include" / "chips" / "coda" / "soc7_0"
            headers.mkdir(parents=True)
            (headers / "header.h").write_text("/* fixture */")
            (root / "Makefile").write_text("# SOC7_0 is not wired yet\n")
            report = wifi_audit.analyze(root)
            self.assertFalse(report["checks"]["makefile_soc7_0_wiring"])
            self.assertEqual(report["source_completeness"], "incomplete")

    def test_empty_chip_directory_is_not_complete(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "chips" / "soc7_0").mkdir(parents=True)
            (root / "Makefile").write_text("SOC7_0 := y\n")
            self.assertEqual(wifi_audit.analyze(root)["source_completeness"], "incomplete")

    def test_missing_directory_safe_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                wifi_audit.analyze(Path(tmp) / "not_there")


if __name__ == "__main__":
    unittest.main()
