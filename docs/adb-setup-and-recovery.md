# ADB 設定、資料隱私與回復檢查

## Windows 10 / WSL2 連接方式

1. 先從 Android 官方下載 [SDK Platform Tools](https://developer.android.com/tools/releases/platform-tools)，解壓縮到 Windows 使用者可讀取的資料夾。
2. Android 系統設定中啟用「開發人員選項」及「USB 偵錯」。使用可傳資料的 USB-C 線連線；在手機解鎖畫面同意該台電腦的 USB 偵錯授權。
3. 在 Windows PowerShell 使用 `adb.exe devices`：看到一筆狀態 `device` 才進下一步。若顯示 unauthorized，必須在手機上授權。
4. 若 Claude Code 在 Windows 執行，可直接呼叫 `adb.exe`；若在 WSL2，可以試 `adb.exe`（需要 Windows PATH 已共享），或指定 Windows ADB 的 WSL 路徑：`python3 tools/device_probe.py --adb '/mnt/c/.../platform-tools/adb.exe'`。優先以 Windows ADB Server 管理 USB；不必為了讀取資訊而做 `usbipd` 附加。
5. 多台裝置同時連線時，使用 `adb devices` 在本機查看 serial，再以 `--serial` 選擇一台。不要把原始裝置列表貼到公開 Issue。
6. 若使用 [Android Wireless Debugging](https://developer.android.com/tools/adb#connect-to-a-device-over-wi-fi)，須先在手機端確認，且僅在可信任網路使用；不要將 ADB TCP port 直接暴露到公網。

## 可重現的只讀盤點

```bash
# 在 repo 根目錄執行；使用標準 Python 3.9+，不需安裝 Python 套件
python3 tools/device_probe.py --adb adb --output reports/poco-x6-pro.json
# WSL2 使用 Windows adb
python3 tools/device_probe.py --adb adb.exe --output reports/narzo-50.json
python3 -m unittest discover -s tests -v
```

`tools/device_probe.py` 僅執行 allowlist：`adb devices`、指定 `getprop`、`uname -r`、`getenforce`、`pm list features`。不要求 Root、不解鎖、不收集 IMEI、MAC、序號、帳號、App 清單或全量 `dumpsys` / `logcat`。

報告 **不** 代表支援 AirDrop / AWDL / Apple Services / 安全生物認證；裝置回報只供起點判斷。建議保存在 `reports/`，此資料夾已由 Git 忽略；提交 GitHub Issue 前先人工再次檢查。若需要共享，僅使用欄位級摘要與去識別樣本。

## 刷機前必須人工確認的清單

- [ ] 完成照片、聊天記錄、2FA、重要 App、媒體檔案的獨立備份和資料還原驗證；若無法還原，禁止解鎖。
- [ ] 實機機型、Device Codename、分割區、現有韌體 Build 與官方可用映像一一對上。
- [ ] 核對 USB 線、電池、Windows 驅動、Fastboot 相容性，並準備一台可連外的電腦。
- [ ] 確認 Bootloader 解鎖資格、可能清除資料，以及 AVB / OTA / Play Integrity 影響。
- [ ] 取得可受信任的原廠 Recovery/映像與經核實的回復流程；不得只相信論壇截圖。
- [ ] 為每個映像核對 SHA-256 與上游來源，不下載不明破解工具。
- [ ] 任何高風險操作需另外提出 PR、說明必要性並取得裝置持有人明確同意。

**目前沒有實機與完整回復流程驗證，因此本專案沒有刷機指令或 Root 自動化腳本。**
