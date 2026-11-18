#!/usr/bin/env python3
"""Static, read-only checklist for the published Duchamp MT6897 Wi-Fi source gap.

This checks source-tree completeness only. It does NOT compile, flash, change
wireless settings, or prove monitor mode, AWDL or RF TX/RX support.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def analyze(driver_tree: Path) -> dict:
    if not driver_tree.is_dir():
        raise ValueError("指定的 gen4-mt79xx driver 目錄不存在。")
    chip = driver_tree / "chips" / "soc7_0"
    header = driver_tree / "include" / "chips" / "coda" / "soc7_0"
    makefile = driver_tree / "Makefile"
    chip_dir = chip.is_dir()
    chip_code = chip_dir and (chip / "soc7_0.c").is_file()
    headers = header.is_dir() and any(p.is_file() for p in header.iterdir())
    makefile_present = makefile.is_file()
    try:
        makefile_text = makefile.read_text(encoding="utf-8", errors="replace") if makefile_present else ""
    except OSError:
        makefile_text = ""
    makefile_wired = "SOC7_0" in makefile_text or "soc7_0" in makefile_text

    complete = bool(chip_code and headers and makefile_wired)
    missing = [
        name for name, present in (
            ("chips/soc7_0/soc7_0.c", chip_code),
            ("include/chips/coda/soc7_0", headers),
            ("Makefile SOC7_0 / soc7_0 build wiring", makefile_wired),
        ) if not present
    ]
    return {
        "schema_version": 1,
        "target": "duchamp / mt6897 / gen4-mt79xx",
        "checks": {
            "soc7_0_dir": bool(chip_dir),
            "soc7_0_c": bool(chip_code),
            "soc7_0_headers": bool(headers),
            "makefile_present": bool(makefile_present),
            "makefile_soc7_0_wiring": bool(makefile_wired),
        },
        "missing": missing,
        "source_completeness": "candidate_complete" if complete else "incomplete",
        "rf_tx_rx_verified": False,
        "awdl_interoperability_verified": False,
        "warning": (
            "即使原始碼項目齊全，也不代表能編譯、載入、啟動監聽模式、"
            "收發 802.11 frame、或和 iPhone 完成 AirDrop。"
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only audit for MT6897 Duchamp Wi-Fi source")
    parser.add_argument("driver_tree", type=Path, help="gen4-mt79xx driver directory within an extracted kernel tree")
    parser.add_argument("--output", type=Path, help="Save JSON locally; no source paths included in output")
    args = parser.parse_args(argv)
    try:
        report = analyze(args.driver_tree)
    except (ValueError, PermissionError) as exc:
        print(f"無法分析：{exc}", file=sys.stderr)
        return 2
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
