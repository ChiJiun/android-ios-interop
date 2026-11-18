# POCO X6 Pro — 裝置能力與修改風險

> 裝置代號：**duchamp**。主要日常手機；預設維持原廠 HyperOS、**不要解鎖或刷機**。
> 文件狀態：硬體型號依公開資訊，**未連接實機，所有版本/硬體細節仍待驗證**。

| 能力 / 資訊 | 目前狀態 | 驗證方式與注意事項 |
| --- | --- | --- |
| 裝置代號 duchamp | 待實機驗證 | \`ro.product.device\`，和官方韌體型號交叉核對 |
| MediaTek Dimensity 8300-Ultra | 待實機驗證 | 官方規格＋\`ro.hardware\`，不推斷 Wi-Fi 晶片細節 |
| Android API / HyperOS 版本 | 待驗證 | \`ro.build.version.sdk\` / \`ro.mi.os.version.name\` |
| Build fingerprint / 安全修補版本 | 待驗證 | 只讀 \`getprop\` |
| Kernel release / GKI、編譯設定 | 待驗證 | \`uname -r\`；GKI/模組 ABI 需另驗證 |
| SELinux 模式 | 待驗證 | \`getenforce\` |
| Verified Boot / Bootloader 現況 | 待驗證 | \`ro.boot.*\` 僅供參考，不等於可解鎖 |
| Camera2 / Face HAL / Biometric class | 待驗證 | PM features 只能初步盤點；實際要用 Android API |
| Wi-Fi / BT/ NFC / IR | 待驗證 | \`pm list features\` + OEM 文檔；AWDL 無法據此判定 |
| AWDL / monitor mode / 802.11 injection | **未證實可用** | 必須有相容驅動與實際 RF TX/RX 測試 |
| Root / Custom Kernel / ROM | **未驗證** | 需另行審查解鎖資格與復原方式 |

## 安全的第一步

使用本 Repo 的 [只讀裝置能力報告](../../tools/device_probe.py)：

\`\`\`bash
python3 tools/device_probe.py --adb adb --output reports/poco-x6-pro.json
\`\`\`

若有兩台 Android，同時連接時請加 \`--serial\`；**序號僅用來選擇目標，不會寫入報告**。不要公開未審查的日誌、\`adb bugreport\`、Wi-Fi 設定、IMEI、Android ID 或帳號資訊。

## Bootloader 與回復事項

- 小米官方 HyperOS 有專屬的 Bootloader 解鎖資格與申請規則，且可能因地區、帳戶與韌體版本而改變；**不要依不明論壇腳本強制解鎖**。
- 解鎖可能清除手機資料；可降低系統安全保護、影響銀行 App 與 OTA。不要在主力機以 Root 為第一步。
- 任何寫入 boot、vendor_boot、init_boot、vbmeta、super 前，都必須核對完全一致的機型、分割區、ROM 版本、Rollback index、救援程序、官方可用映像與 USB/電力狀態。
- **尚未驗證可回復的完整官方映像來源；不得執行刷機**。
- 將來若確定需要 Kernel：先隔離測試機與 VM，記錄 \`git\` commit、編譯器/工具鏈版本與 image checksum。

## 上游資源

- Xiaomi 官方: https://github.com/MiCode/Xiaomi_Kernel_OpenSource （搜尋 duchamp 分支）
- 裝置開發社群: https://github.com/mt6897-devs
- Xiaomi 官方 Bootloader FAQ: https://www.mi.com/global/support/faq/details/KA-07238/
- AOSP Bootloader 原理: https://source.android.com/docs/core/architecture/bootloader/locking_unlocking
