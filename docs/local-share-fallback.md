# Android ↔ iPhone / 桌面無 Root 傳檔替代方案

## 決策：優先整合現有 LocalSend，不自製 AirDrop

原生 Quick Share ↔ AirDrop 是不同的功能：本專案不保證 POCO X6 Pro 獲得 Google 官方支援。因此先提供 **Android Sharesheet 傳送入口**：使用者在 App 中輸入文字或以系統檔案選取器選擇圖片／影片／文件，並由**使用者主動選擇** LocalSend 或其他 Android 分享 App。這並非自製 LocalSend 傳輸協定。

參考原始碼與協定：
- https://github.com/localsend/localsend （Apache-2.0；專案是 Flutter App，保留獨立安裝、未複製其原始碼）
- https://github.com/KDE/kdeconnect-android （跨裝置控制及傳檔研究）
- Android ACTION_SEND / ACTION_SEND_MULTIPLE 和 Storage Access Framework 官方 API。

## 使用流程

1. 在 POCO 安裝我們的 Debug App（建置仍待 CI），在 iPhone 安裝 LocalSend 官方 App；雙方連上能互通的相同 LAN。
2. 在 Android App 的「跨平台分享入口」中輸入文字後按「分享文字」，或點「選擇檔案」透過 Android 系統檔案選取器勾選檔案。
3. Android Sharesheet 由你選擇 **LocalSend** 作為分享對象，並在 LocalSend 的接收端清單選擇 iPhone/桌面。
4. 在接收端核准傳輸，檢查文字內容或檔案大小；大檔案若要檢驗完整性，可在兩端匯出到電腦，以 SHA-256 對照。
5. 回到 App，不會留下背景掃描任務或長期存取許可。

本 App 只透過 Intent 傳遞資料給使用者挑選的第三方 App；**真正 LAN 裝置探索、加密配對與傳輸由 LocalSend 負責**。

## 目前實作的安全保護

- 不需要 Root、Storage 全域權限、Internet 權限、Accessibility 權限或 Apple 帳號。
- 使用 ACTION_OPEN_DOCUMENT 選取檔案，只對使用者選定的 URI 給短期讀取授權。
- 對多檔案使用 Intent.ACTION_SEND_MULTIPLE + ClipData + FLAG_GRANT_READ_URI_PERMISSION；由 Android 分享選單讓使用者再次確認目標。
- 文字只會在使用者按「分享文字」後傳送，拒絕空白或超過 10000 UTF-16 code unit 的文字。
- 不讀取剪貼簿、不儲存裝置 ID、不自行掃描 LAN 或上傳任何資料到本專案伺服器。

## 驗收矩陣（尚未實機測試）

| 測試 | 操作 | 驗收 |
| --- | --- | --- |
| LS-01 | POCO → iPhone：繁體中文文字 | ShareSheet 看得到 LocalSend、接受後內容一致 |
| LS-02 | POCO → iPhone：圖片 | 檔案可開啟、大小或雜湊一致 |
| LS-03 | POCO → Windows/macOS：100MB+ 影片 | 傳輸成功率與速度、有可比對大小/雜湊 |
| LS-04 | iPhone → POCO | 由 iPhone LocalSend 發送，Android LocalSend 可接收 |
| LS-05 | 接收端拒絕、App 未安裝、Wi-Fi 切換 | 無閃退、清楚顯示回退操作 |
| LS-06 | 同名裝置、隔離 Wi-Fi、VPN/Tailscale | 發現/連線錯誤可辨識，必要時改用手動指定/QR 支援方式 |

## 預期限制與比較

| 項目 | LocalSend | 原生 AirDrop |
| --- | --- | --- |
| Android 及 iPhone 可用 | 兩端安裝 App 後通常可用 | 只有官方支援或成功的移植實作 |
| 是否需要共用 Apple ID | 不需要 | 不需要，共享權限仍受 Apple 設定影響 |
| 是否要 Root | 不需要 | 不要求，但非官方 Android 移植可能需要 |
| 是否要 Internet | 同一可連通 LAN 下可離線 | 相容設備可點對點離線 |
| 相容性主要風險 | AP isolation、multicast、VPN、防火牆、版本不一致 | OEM/Google/GMS、AWDL 驅動與裝置授權 |
| 是否真實 AirDrop | 否 | 是 |

## 未完成

- [ ] 真機 Android App 的 Gradle / CI 編譯與 iPhone 端測試。依賴上游 Issue #3 的建置完成。
- [ ] LS-01 到 LS-06 的實測，包含 iPhone 反向傳檔與 100MB 大檔 SHA-256。
- [ ] 使用者操作體驗、性能、電量、異常操作處理及 iOS 端配對教學。
- [ ] 若未來要內建區網協定，需先另立設計與授權 Issue，不直接複製 Flutter 原始碼。
