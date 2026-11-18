# Android × Apple Interoperability Lab

以繁體中文記錄 Android 與 Apple 生態系功能互通的研究、開發與測試，重視可安裝、可回復、合法開源的實作。

> 非 Apple、Google、Xiaomi 或 realme 官方專案。不保證 AirDrop、AirPlay、iMessage、iCloud、AirPods 在所有裝置上運作。

## 裝置與目標

- **POCO X6 Pro (duchamp)**：主要目標；預設保留 HyperOS，不先要求 Root。
- **realme narzo 50 (4G, spaced，待確認實際型號)**：次要測試裝置；Bootloader、Recovery、Kernel 需先確認支援與回復方案。
- **Apple 裝置**：進行雙向互通驗收時，需要實機，記錄 iOS / macOS / tvOS 版本與網路設定。

## 原則

1. **Capability-first**：先盤點官方支援與 Android API，無法達成才評估 ADB、Shizuku、Root、Kernel、ROM。
2. **Evidence-based**：區分「API 可用」「裝置可發現」「完成傳輸」「跨裝置實測」，不得只以模組載入視為成功。
3. **Modular**：Android UI、互通協定、裝置適配、底層系統修改互相隔離。
4. **Safe by default**：非破壞性偵測優先；刷機、解鎖或改 SELinux 需單獨評估並保留回復路徑。
5. **Open-source compliance**：先查清上游授權；不分發 Google/Apple 專有 APK、二進位、私密憑證與使用者資料。

## Android App 建置（Issue #3）

此 Repository 已含 Android App 初始架構與功能能力清單，並新增 **實驗性的 Android 系統 Sharesheet 分享入口**：使用者可以選擇文字或檔案，手動交給 LocalSend 等第三方 App。**真正 AirDrop、LAN 傳輸協定、AirPlay 等仍未實作。**

- 需求：JDK 17、Android SDK API 36、Gradle 8.13，或 Android Studio 相容環境。
- 建置：`gradle :core:capabilities:test :app:lintDebug :app:assembleDebug`
- APK：`app/build/outputs/apk/debug/app-debug.apk`，無簽章密鑰且不依賴 Root。
- GitHub Actions：規劃執行 Lint／Unit Tests／Debug APK 組裝；範本在 `ci/android-ci.yml.example`。目前帳號權杖缺少 `workflow` scope，**尚未啟用 CI**。
- 完整指南：[Android 開發、測試與發行](docs/android-development.md)。
- 無 Root 分享替代方案與驗收：[LocalSend 整合說明](docs/local-share-fallback.md)。

## 開發方向（詳見 GitHub Issues）

- Quick Share / AirDrop 的官方相容性研究與 AWDL 硬體可行性。
- LocalSend 類跨平台檔案分享作為不需要 Root 的替代方案。
- AirPlay 接收／發送、Apple TV Remote、AirPods 整合。
- 動態島、待機模式與 Android 桌面／跨裝置操作。
- Apple 帳號、iMessage、iCloud 功能邊界研究（不承諾原生 iOS App Store 相容）。
- Android AI Agent、ADB / scrcpy 開發與系統級可行性。

## 優先參考的上游

- https://github.com/thelok1s/mosey-extended — 研究性實驗；虛擬 Wi-Fi phy 不等於真實無線傳輸。
- https://github.com/moseoridev/WarpShare — Android → Mac，並非完整雙向 iPhone AirDrop。
- https://github.com/seemoo-lab/opendrop 及 https://github.com/seemoo-lab/owl — AWDL / AirDrop 協定研究。
- https://github.com/localsend/localsend — 跨平台區網分享。
- https://github.com/jqssun/android-airplay-server 與 https://github.com/itsHenry35/Kite — AirPlay 接收／發送。
- https://github.com/librepods-org/librepods — AirPods 功能。
- https://github.com/POX-project/disland 與 https://github.com/Haxintosh/standby — UI 與待機模式。
- https://github.com/BlueBubblesApp/bluebubbles-app — Mac 橋接的 iMessage 客戶端。
- https://github.com/KDE/kdeconnect-android 與 https://github.com/Genymobile/scrcpy — 跨裝置操作。

**Android 基礎骨架已開始實作；由於 VM 沒有 Java / Android SDK，且 GitHub workflow scope 不足，目前未通過 Android 編譯或 CI 驗證；互通功能尚未完成。**

## License

尚未引入上游程式碼；本專案自有程式碼授權選型待完成相容性盤點，未經確認不得複製上游 GPL、Apache 或其他授權的程式碼。
