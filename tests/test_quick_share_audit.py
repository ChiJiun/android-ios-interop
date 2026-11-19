import importlib.util
import subprocess
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "quick_share_audit", Path(__file__).parents[1] / "tools" / "quick_share_audit.py"
)
audit_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit_module)


class AuditTests(unittest.TestCase):
    @staticmethod
    def mock_runner(commands):
        seen = []

        def run(args, **kwargs):
            seen.append(args)
            action = tuple(args[1:])
            value = commands.get(action, "")
            return subprocess.CompletedProcess(args, 0, value, "")

        return run, seen

    def test_presence_is_not_compatibility(self):
        runner, seen = self.mock_runner({
            ("devices",): "List of devices attached\nSECRET\tdevice\n",
            ("-s", "SECRET", "shell", "getprop", "ro.product.device"): "duchamp\n",
            ("-s", "SECRET", "shell", "pm", "path", "com.google.android.gms"): "package:/system/priv-app/gms.apk\n",
        })
        report = audit_module.audit("adb", None, runner)
        self.assertFalse(report["direct_airdrop_verified"])
        self.assertEqual(report["status"], "unknown_requires_real_apple_device_test")
        self.assertEqual(report["candidate_packages"]["com.google.android.gms"], "detected")
        self.assertNotIn("SECRET", str(report))
        self.assertTrue(all("pm" not in cmd or "path" in cmd for cmd in seen))
        self.assertFalse(any("reboot" in cmd or "fastboot" in cmd for cmd in seen))

    def test_unrecognized_packages_are_unknown_or_missing(self):
        runner, _ = self.mock_runner({"devices": "unsupported"})
        with self.assertRaises(audit_module.AuditError):
            audit_module.audit("adb", None, runner)

    def test_multiple_devices_are_explicitly_selected(self):
        runner, _ = self.mock_runner({
            ("devices",): "List of devices attached\nA\tdevice\nB\tdevice\n",
        })
        with self.assertRaises(audit_module.AuditError):
            audit_module.audit("adb", None, runner)
        report = audit_module.audit("adb", "B", runner)
        self.assertNotIn('"B"', str(report))

    def test_unexpected_identifiers_are_redacted(self):
        self.assertEqual(audit_module.sanitize_property("alice@example.com"), "[REDACTED]")
        self.assertEqual(audit_module.sanitize_property("aa:bb:cc:dd:ee:ff"), "[REDACTED]")
        self.assertEqual(audit_module.sanitize_property("a\nb"), "unknown")
        self.assertEqual(audit_module.sanitize_property("duchamp"), "duchamp")

    def test_error_output_does_not_expose_serial(self):
        def run(args, **kwargs):
            return subprocess.CompletedProcess(args, 1, "", "user serial SECRET")
        with self.assertRaises(audit_module.AuditError) as exc:
            audit_module.audit("adb", None, run)
        self.assertNotIn("SECRET", str(exc.exception))


if __name__ == "__main__":
    unittest.main()
