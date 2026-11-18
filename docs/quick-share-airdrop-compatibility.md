# Quick Share ↔ AirDrop：POCO X6 Pro 相容性研究（2026-11-18）

## 結論與邊界

**截至研究時，沒有直接實機驗證 POCO X6 Pro (duchamp) 的 Quick Share ↔ Apple AirDrop。** Google 已在部分 Android 裝置提供直接點對點互通，並於 2026 年表示持續擴展 Samsung、OPPO、OnePlus、Vivo、Xiaomi、HONOR 等品牌；**品牌有合作不等於這個具體型號受支援**。

官方的 Quick Share **QR Code 雲端連結**可以讓不支援原生 AirDrop 的 Android 分享至 iOS，但不等於 iPhone 在原生 AirDrop 清單裡找到 Android，亦非離線傳輸。

| 功能 | POCO X6 Pro 狀態 | 判定條件 |
| --- | --- | --- |
| Android ↔ Android Quick Share | 待本機核實 | 原生 Quick Share 實際收發 |
| Android → iPhone 原生 AirDrop | **未驗證** | iPhone AirDrop 清單發現 POCO，成功完成檔案收發 |
| iPhone → Android 原生 AirDrop | **未驗證** | Android Quick Share 發現 iPhone，完成檔案傳輸 |
| Android → iPhone QR Code 分享 | 不等於 AirDrop | iPhone 使用相機讀取網頁／雲端連結 |
| Google Mosey / Quick Share Extension 是否安裝 | 待只讀檢查 | 套件存在僅是線索，**不是成功證據** |
| MediaTek Wi-Fi AWDL RF support | 未確認 | 需另外 Issue #5 的實際 RF TX/RX 驗證 |

## 不 Root、只讀診斷

1. 使用官方 Android SDK Platform Tools；手機同意 USB 偵錯授權。
2. 於專案根目錄，Windows、Linux 或 WSL2 執行：

```bash
adb devices
python3 tools/quick_share_audit.py --adb adb --output reports/poco-quickshare.json
# WSL2 若使用 Windows ADB：
python3 tools/quick_share_audit.py --adb adb.exe --output reports/poco-quickshare.json
python3 -m unittest discover -s tests -v
```

工具只讀取有限的 Android 版本/型號欄位，以及有限 Google/OEM 套件的 `pm path` 結果；不擷取 App 清單、帳號、裝置 serial、IMEI、MAC、Bluetooth 封包、logcat，也不執行 Root / Fastboot / Setprop。輸出預設放在忽略追蹤的 `reports/`；人工檢查後才可分享。

**重要：**

- `com.google.android.gms` 存在不代表手機支援 AirDrop。
- `com.google.android.mosey` 不存在不代表 Google 未在 GMS 內建其他整合路徑；不同 ROM、區域和 rollout 會有不同封裝。
- 原廠 Quick Share 功能可能由 Google Play services、OEM 套件與系統權限共同控制。**本專案不嘗試篡改 Google 簽章、Feature Flags 或 Play Integrity**。

## 可重現的真人測試矩陣

事先記錄：POCO/ iPhone/iPad/macOS 版本、Quick Share / Play Services 版本、是否登入 Google、AirDrop 可見性、Wi-Fi/Bluetooth 狀態、網路是否可用；不得公開裝置識別碼或帳號。

| 測試編號 | 方向 | 資料 | 網路 | 需要檢查 |
| --- | --- | --- | --- | --- |
| QS-01 | Android → iPhone | TXT / JPG | 離線或 Wi-Fi 開啟、無 Internet | 是否「原生 AirDrop 清單」直接互相發現、成功傳輸 |
| QS-02 | iPhone → Android | TXT / JPG | 相同 | 是否直接看到 Android、接收提示、檔案可讀 |
| QS-03 | Android ↔ iPad/Mac | JPG / PDF | 相同 | 雙向搜尋與收發 |
| QS-04 | Android → iPhone | 100MB+ 影片 | 穩定 Wi-Fi | 傳輸速度、成功率、SHA-256（可匯出到桌面核對） |
| QS-05 | Android → iPhone | 小檔案 | Internet 可用、直連不可用 | 只能 QR → 雲端時清楚分類為 fallback |
| QS-06 | Android ↔ Android | JPG | Wi-Fi / BT 開啟 | 比較普通 Quick Share 與 AirDrop 擴充差異 |

每項記錄：開始與結束時間、是否真正在對方**原生介面**出現、接受提示、檔案 hash/大小、是否走雲端、可重現錯誤。AirDrop 「Everyone for 10 Minutes」視 Apple 版本、操作和安全需求設定，測試完恢復原來可見性。

## 開源實作研究

- [mosey-extended](https://github.com/thelok1s/mosey-extended)：Pixel 10 Mosey 服務移植實驗。**README 明示虛擬 PHY 不提供真正 RF TX/RX**，非 Pixel 仍屬研究。不能因模組載入或 SELinux 放行就宣稱成功 AirDrop。
- [WarpShare](https://github.com/moseoridev/WarpShare)：Android → Mac 的 AirDrop 相容實驗，非完整 Android ↔ iPhone 雙向。
- [OpenDrop](https://github.com/seemoo-lab/opendrop)、[OWL](https://github.com/seemoo-lab/owl)：AWDL / AirDrop 原理；非 MediaTek driver 現成補丁。
- [LocalSend](https://github.com/localsend/localsend)：可立即部署的跨平台替代方案，但兩端需支援相同 App，與原生 AirDrop 不同。

不得將 Google vendor / Apple 專有二進位與未釐清授權的 ROM 程式碼打包成可下載 APK。

## 官方來源

- Google 2025-11-20 首次推出：https://blog.google/products-and-platforms/platforms/android/quick-share-airdrop/
- Google 2026-05-12 合作品牌擴展與 QR fallback：https://blog.google/products-and-platforms/platforms/android/new-android-updates/
- Google 官方 Quick Share 使用說明：https://support.google.com/android/answer/9286773
- Google 技術安全介紹：https://blog.google/security/android-quick-share-support-for-airdrop-security/

## 下一步

- [ ] 在 POCO 實機執行只讀掃描，補完整版本與官方相容狀態。
- [ ] 取得可用 iPhone / Mac，執行 QS-01 至 QS-06；沒實機不能標示通過。
- [ ] 如果直接互通失敗，分別記錄「未發現裝置」「連線失敗」「傳輸失敗」，而不是直接歸因 MediaTek driver。
- [ ] 若確定系統路徑不可行，再由 #5 研究 Wi-Fi/AWDL 最小 PoC，不先要求 Root。
