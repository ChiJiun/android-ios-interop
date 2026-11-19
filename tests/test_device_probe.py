import importlib.util
import subprocess
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "tools" / "device_probe.py"
spec = importlib.util.spec_from_file_location("device_probe", SCRIPT)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


def fake_runner(*, devices="ABC123\tdevice\n", overrides=None):
    overrides = overrides or {}
    calls = []

    def run(args, **kwargs):
        calls.append(args)
        if args[1:] == ["devices"]:
            return subprocess.CompletedProcess(args, 0, "List of devices attached\n" + devices, "")
        if args[-2:] == ["pm", "list"] or args[-3:] == ["pm", "list", "features"]:
            return subprocess.CompletedProcess(
                args, 0,
                "feature:android.hardware.camera.front\nfeature:android.hardware.wifi\n"
                "feature:android.hardware.sensor.accelerometer\n"
                "feature:com.vendor.account.secret\n", ""
            )
        if args[-2:] == ["uname", "-r"]:
            return subprocess.CompletedProcess(args, 0, "5.10.223\n", "")
        if args[-1] == "getenforce":
            return subprocess.CompletedProcess(args, 0, "Enforcing\n", "")
        if "getprop" in args:
            key = args[-1]
            return subprocess.CompletedProcess(args, 0, overrides.get(key, "unknown") + "\n", "")
        return subprocess.CompletedProcess(args, 1, "", "some unexpected stderr with ABC123")

    return run, calls


class CapabilityProbeTests(unittest.TestCase):
    def test_collect_only_allowlisted_commands_and_no_serial(self):
        run, calls = fake_runner(overrides={"ro.product.model": "POCO X6 Pro"})
        report = probe.collect("adb", run=run)
        self.assertEqual(report["properties"]["model"]["value"], "POCO X6 Pro")
        self.assertIn("android.hardware.camera.front", report["features"]["values"])
        self.assertNotIn("com.vendor.account.secret", report["features"]["values"])
        self.assertNotIn("ABC123", str(report))
        self.assertTrue(all("getprop" in cmd or cmd[-1] in ("devices", "-r", "getenforce", "features") for cmd in calls))
        self.assertFalse(any("fastboot" in cmd or "reboot" in cmd for cmd in calls))

    def test_multiple_devices_requires_selection(self):
        run, _ = fake_runner(devices="ABC123\tdevice\nXYZ456\tdevice\n")
        with self.assertRaises(probe.ProbeError):
            probe.collect("adb", run=run)
        report = probe.collect("adb", serial="XYZ456", run=run)
        self.assertNotIn("XYZ456", str(report))

    def test_unauthorized_device_does_not_leak_ids(self):
        run, _ = fake_runner(devices="TOPSECRET\tunauthorized\n")
        with self.assertRaises(probe.ProbeError) as cm:
            probe.collect("adb", run=run)
        self.assertNotIn("TOPSECRET", str(cm.exception))

    def test_missing_property_is_unavailable(self):
        run, _ = fake_runner(overrides={"ro.mi.os.version.name": ""})
        report = probe.collect("adb", run=run)
        self.assertEqual(report["properties"]["hyperos_version"]["status"], "unavailable")

    def test_redact_sensitive_strings(self):
        self.assertEqual(probe.redact("foo@example.org"), "[REDACTED]")
        self.assertEqual(probe.redact("00:11:22:33:44:55"), "[REDACTED]")
        self.assertEqual(probe.redact("model\nunexpected"), "model unexpected")

    def test_failure_messages_do_not_echo_stderr(self):
        def runner(args, **kwargs):
            if args[1:] == ["devices"]:
                return subprocess.CompletedProcess(args, 0, "List of devices attached\nABC123\tdevice\n", "")
            return subprocess.CompletedProcess(args, 1, "", "ABC123 top secret")
        report = probe.collect("adb", run=runner)
        self.assertNotIn("top secret", str(report))
        self.assertEqual(report["kernel_release"]["status"], "unavailable")


if __name__ == "__main__":
    unittest.main()
