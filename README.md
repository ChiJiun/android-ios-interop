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

## MediaTek Wi-Fi / AWDL 研究（Issue #5）

先閱讀 [POCO X6 Pro AWDL 與 Kernel Source 可行性報告](docs/awdl-mediatek-feasibility.md)。
若已取得對應版號的 Kernel Source，可用只讀工具檢查 `soc7_0` 原始碼與 Makefile 項目：

```bash
python3 tools/duchamp_wifi_source_audit.py /path/to/gen4-mt79xx
python3 -m unittest discover -s tests -v
```

**即使 Source 齊全，也不能據此宣稱已支援 AirDrop。** 尚未操作實機 RF、Kernel Module、Root 或刷機。

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

**已加入 Kernel Wi-Fi Source 靜態盤點工具；尚未完成實機 RF/Android Kernel/AirDrop 測試。**

## License

程式碼尚未加入，授權選型待完成相容性盤點；未經確認不得直接複製上游 GPL、Apache 或其他授權的程式碼。
