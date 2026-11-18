#!/usr/bin/env python3
"""Non-invasive Quick Share/AirDrop inventory. Never claims compatibility from APK presence."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

# Candidate package names are signals, NOT a confirmed compatibility database.
# Exact names can change with OEM, Google Play Services updates, regions and rollouts.
PACKAGES = (
    "com.google.android.gms",
    "com.google.android.mosey",
    "com.google.android.apps.nearby",
    "com.google.android.apps.nbu.files",
    "com.samsung.android.app.sharelive",
    "com.miui.mishare.connectivity",
)
PUBLIC_PROPS = {
    "device": "ro.product.device",
    "model": "ro.product.model",
    "android": "ro.build.version.release",
    "api_level": "ro.build.version.sdk",
    "hyperos": "ro.mi.os.version.name",
}
Run = Callable[..., subprocess.CompletedProcess[str]]


class AuditError(Exception):
    pass


def adb_call(adb: str, args: list[str], run: Run) -> str:
    try:
        r = run([adb, *args], capture_output=True, text=True, timeout=10, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise AuditError("ADB 無法執行或逾時，請先確認 USB 偵錯授權。") from exc
    if r.returncode:
        # Do not leak stderr: some ADB errors contain device serials.
        raise AuditError("ADB 指令未成功，請檢查手機授權與連線。")
    return r.stdout.strip()


def select(adb: str, serial: str | None, run: Run) -> str:
    lines = adb_call(adb, ["devices"], run).splitlines()[1:]
    connected = [
        parts[0] for line in lines
        if (parts := line.split()) and len(parts) >= 2 and parts[1] == "device"
    ]
    if serial:
        if serial not in connected:
            raise AuditError("指定裝置未授權或未連線。")
        return serial
    if len(connected) != 1:
        raise AuditError("請保持一台已授權裝置，或提供 --serial 選擇（不會儲存序號）。")
    return connected[0]


def audit(adb: str, serial: str | None, run: Run = subprocess.run) -> dict:
    device = select(adb, serial, run)
    prefix = ["-s", device, "shell"]
    build = {}
    for label, prop in PUBLIC_PROPS.items():
        try:
            val = adb_call(adb, [*prefix, "getprop", prop], run)
            build[label] = val[:160] if val and "\n" not in val else "unknown"
        except AuditError:
            build[label] = "unknown"
    present: dict[str, str] = {}
    for package in PACKAGES:
        try:
            output = adb_call(adb, [*prefix, "pm", "path", package], run)
            present[package] = "detected" if output.startswith("package:") else "not_detected"
        except AuditError:
            present[package] = "unknown"
    return {
        "schema_version": 1,
        "collected_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "device_info": build,
        "candidate_packages": present,
        "direct_airdrop_verified": False,
        "status": "unknown_requires_real_apple_device_test",
        "interpretation": [
            "Package present/absent is not proof of Google-certified Quick Share ↔ AirDrop support.",
            "Mosey virtual Wi-Fi PHY / service loading is not proof of real 802.11 frame transmission.",
            "Quick Share QR cloud share is NOT direct peer-to-peer AirDrop interoperability.",
            "No complete device inventory, privileged data, Bluetooth scan or private logs collected.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only Quick Share / AirDrop research probe")
    parser.add_argument("--adb", default=None, help="ADB executable, e.g. adb or adb.exe")
    parser.add_argument("--serial", help="Local device selector (never written to report)")
    parser.add_argument("--output", type=Path, help="Optional local JSON output")
    args = parser.parse_args(argv)
    adb = args.adb or ("adb" if shutil.which("adb") else "adb.exe")
    try:
        result = audit(adb, args.serial)
    except AuditError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
        print("完成唯讀能力報告。提交 GitHub 前仍請人工檢查資料。")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
