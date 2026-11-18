# realme narzo 50 — 實驗機盤點

> **裝置待確認**：以下僅適用於 **realme narzo 50 4G / spaced（常見型號 RMX3286）**。narzo 50 5G 是不同硬體，絕不能套用本頁刷機資源。
> 目前未接到實機，因此型號、Android 版本、Bootloader 權限、Recovery 相容性均是 **待驗證**。

| 能力 / 資訊 | 目前狀態 | 驗證方式與注意事項 |
| --- | --- | --- |
| 裝置代號 spaced / RMX3286 | 待實機驗證 | 核對包裝/系統設定＋\`ro.product.device\`，不能只靠商品名稱 |
| MediaTek Helio G96（4G 版） | 待實機驗證 | 官方規格與核心資訊交叉核對 |
| Android、realme UI、Build | 待驗證 | \`getprop\` 報告 |
| Kernel release / 安全補丁 | 待驗證 | \`uname -r\` / \`getprop\` |
| AVB、SELinux、Bootloader 鎖定 | 待驗證 | 只讀查核 |
| Wi-Fi / Bluetooth / Camera / Sensors | 待驗證 | PM Features 僅是初步資訊 |
| TWRP Device Support | 待確認版本相容 | TWRP 有 realme 8i / narzo 50 (spaced) 頁面，不保證每個版本安全 |
| 解鎖 Bootloader | **未證實** | Realme 韌體及 unlock tool 受版本限制，需官方資料與實機確認 |
| AWDL / 802.11 injection | **未證實** | 不能推論有 Linux 驅動就能 AirDrop |
| 可回復的原廠韌體/分割區備份 | **尚未驗證** | **未取得前不得刷寫或修改分割區** |

## 安全盤點（不 Root）

\`\`\`bash
python3 tools/device_probe.py --adb adb --output reports/narzo-50.json
\`\`\`

若透過 Windows + WSL，優先使用 Windows \`adb.exe\` 以及已授權的 USB 裝置。只讀工具不會執行 \`fastboot\`、\`reboot\` 或修改設定。

## Recovery / Bootloader 風險

- TWRP 支援頁面不等於你的韌體版本已實機驗證。
- 先確認機型型號、分割區佈局、加密/AVB、可取得的原廠韌體與救援路徑，再考慮解鎖或測試自製核心。
- 解鎖可能抹除所有使用者資料；不要先實驗 Root 或 \`fastboot flash\` 再找還原方式。
- 任何 Recovery image 都只能使用經過精確機型/韌體核對的來源；**POCO 的 Kernel / recovery 絕對不能刷入 narzo**。
- 無 Apple 裝置、無 Root 的情況下，先測試純 Android API 功能及本機網路替代方案。

## 參考

- narzo 50 / realme 8i TWRP: https://twrp.me/realme/realme8i.html
- Realme 官方 kernel source: https://github.com/realme-kernel-opensource/realme_Narzo-50_8i-AndroidT-kernel-source
- AOSP Verified Boot / Bootloader: https://source.android.com/docs/core/architecture/bootloader/locking_unlocking
