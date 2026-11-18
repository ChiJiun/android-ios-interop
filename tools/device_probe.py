#!/usr/bin/env python3
"""Read-only ADB capability inventory, designed to avoid collecting device identifiers.

No Root, unlocking, reboot, fastboot, settings changes, logcat or full dumpsys.
Requires Python 3.9+ and Android SDK Platform Tools on the host.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

# Deliberately allowlisted non-unique system properties; never collect serial,
# Android ID, IMEI, network addresses, account names, installed apps or logs.
PROPERTIES = {
    "manufacturer": "ro.product.manufacturer",
    "model": "ro.product.model",
    "device_codename": "ro.product.device",
    "board": "ro.product.board",
    "android_release": "ro.build.version.release",
    "api_level": "ro.build.version.sdk",
    "build_fingerprint": "ro.build.fingerprint",
    "security_patch": "ro.build.version.security_patch",
    "hyperos_version": "ro.mi.os.version.name",
    "miui_version": "ro.miui.ui.version.name",
    "kernel_hardware": "ro.hardware",
    "wifi_hardware": "ro.hardware.wifi",
    "vendor_wifi_hardware": "ro.vendor.wifi.hardware",
    "verified_boot_state": "ro.boot.verifiedbootstate",
    "flash_locked": "ro.boot.flash.locked",
    "vbmeta_device_state": "ro.boot.vbmeta.device_state",
}
FEATURE_PREFIXES = (
    "android.hardware.camera",
    "android.hardware.wifi",
    "android.hardware.bluetooth",
    "android.hardware.nfc",
    "android.hardware.fingerprint",
    "android.hardware.biometrics",
    "android.hardware.sensor.",
    "android.hardware.usb.",
)
PRIVATE_PATTERNS = (
    re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}"),
    re.compile(r"(?i)\b(?:[0-9a-f]{2}:){5}[0-9a-f]{2}\b"),
)
MAX_FIELD_LENGTH = 512
Run = Callable[..., subprocess.CompletedProcess[str]]


class ProbeError(RuntimeError):
    """Safe error for public output (does not contain device identifiers)."""


def redact(value: str) -> str:
    value = value.strip().replace("\r", "")
    for pattern in PRIVATE_PATTERNS:
        value = pattern.sub("[REDACTED]", value)
    return value[:MAX_FIELD_LENGTH]


def call_adb(adb: str, args: list[str], run: Run = subprocess.run, timeout: float = 10) -> str:
    try:
        result = run([adb, *args], capture_output=True, text=True, timeout=timeout, check=False)
    except FileNotFoundError as exc:
        raise ProbeError("ADB 未安裝或找不到；請設定 --adb 為 adb / adb.exe 的實際路徑。") from exc
    except subprocess.TimeoutExpired as exc:
        raise ProbeError("ADB 指令逾時；請檢查 USB 偵錯授權與連線。") from exc
    if result.returncode:
        # Do not echo arbitrary stderr: it can contain a device identifier.
        raise ProbeError("ADB 指令失敗；請確認裝置已授權且可使用 shell。")
    return result.stdout.strip()


def choose_device(adb: str, requested: str | None, run: Run) -> str:
    raw = call_adb(adb, ["devices"], run)
    lines = raw.splitlines()[1:]
    authorized = [
        line.split()[0] for line in lines
        if len(line.split()) >= 2 and line.split()[1] == "device"
    ]
    if requested:
        if requested not in authorized:
            raise ProbeError("指定裝置未連線或尚未授權 USB 偵錯。")
        return requested
    if len(authorized) != 1:
        raise ProbeError("需要剛好一台已授權裝置；若有多台請使用 --serial 選擇（序號不會存入報告）。")
    return authorized[0]


def collect(adb: str, serial: str | None = None, run: Run = subprocess.run) -> dict:
    chosen = choose_device(adb, serial, run)
    # Only commands from a static allowlist; no shell command provided by user.
    prefix = ["-s", chosen, "shell"]
    props: dict[str, dict[str, str]] = {}
    for name, key in PROPERTIES.items():
        try:
            value = redact(call_adb(adb, [*prefix, "getprop", key], run))
            props[name] = {"value": value, "status": "reported" if value else "unavailable"}
        except ProbeError:
            props[name] = {"value": "", "status": "unavailable"}
    try:
        kernel = redact(call_adb(adb, [*prefix, "uname", "-r"], run))
    except ProbeError:
        kernel = ""
    try:
        selinux = redact(call_adb(adb, [*prefix, "getenforce"], run))
    except ProbeError:
        selinux = ""
    try:
        feature_lines = call_adb(adb, [*prefix, "pm", "list", "features"], run).splitlines()
        features = sorted({
            name for line in feature_lines
            if line.startswith("feature:")
            for name in [line.removeprefix("feature:").split("=", 1)[0]]
            if name.startswith(FEATURE_PREFIXES)
            and re.fullmatch(r"[a-zA-Z0-9_.]+", name)
        })
        feature_status = "reported"
    except ProbeError:
        features = []
        feature_status = "unavailable"
    # No device serial, account, IMEI, MAC, private identifiers or raw diagnostics.
    return {
        "schema_version": 1,
        "collected_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "method": "read_only_adb",
        "properties": props,
        "kernel_release": {"value": kernel, "status": "reported" if kernel else "unavailable"},
        "selinux_mode": {"value": selinux, "status": "reported" if selinux else "unavailable"},
        "features": {"status": feature_status, "values": features},
        "caveats": [
            "屬於 Android 自行回報資訊，不等於 OEM 原始碼或晶片規格已經核實。",
            "pm list features 未列出不代表硬體不存在；也不能證明 AWDL/802.11 monitor/injection 支援。",
            "此報告不測試 Bootloader 能否解鎖、Root、Fastboot、刷機或人臉辨識安全級別。",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only, privacy-conscious Android capability probe")
    parser.add_argument("--adb", default=None, help="ADB command, e.g. adb or adb.exe")
    parser.add_argument("--serial", help="Select one of multiple connected devices; not stored in report")
    parser.add_argument("--output", type=Path, help="Write JSON to file (otherwise print to stdout)")
    args = parser.parse_args(argv)
    adb = args.adb or ("adb" if shutil.which("adb") else "adb.exe")
    try:
        report = collect(adb, args.serial)
    except ProbeError as exc:
        print(f"裝置讀取失敗：{exc}", file=sys.stderr)
        return 2
    content = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        # Report is intentionally untracked by default; only opt-in paths used.
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content, encoding="utf-8")
        print(f"已產生能力報告：{args.output}")
    else:
        sys.stdout.write(content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
