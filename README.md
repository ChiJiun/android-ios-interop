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

## 開發方向（詳見 GitHub Issues）

- Quick Share / AirDrop 的官方相容性研究與 AWDL 硬體可行性。
- LocalSend 類跨平台檔案分享作為不需要 Root 的替代方案。
- AirPlay 接收／發送、Apple TV Remote、AirPods 整合。
- 動態島、待機模式與 Android 桌面／跨裝置操作。
- Apple 帳號、iMessage、iCloud 功能邊界研究（不承諾原生 iOS App Store 相容）。
- Android AI Agent、ADB / scrcpy 開發與系統級可行性。

## 裝置能力盤點（Issue #2）

在筆電安裝 Android SDK Platform Tools、手機授權 USB 偵錯後，使用 **Python 3.9+** 進行只讀能力盤點：

```bash
python3 tools/device_probe.py --adb adb --output reports/poco-x6-pro.json
python3 -m unittest discover -s tests -v
```

詳見 [Windows / WSL2 ADB 與安全回復清單](docs/adb-setup-and-recovery.md)、[POCO X6 Pro](docs/devices/poco-x6-pro.md)、[narzo 50](docs/devices/narzo-50.md)。這些工具不會 Root、刷機或修改手機設定；目前尚未連接真機，因此硬體能力與 Bootloader 狀態仍未實際驗證。

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

**目前尚未完成 Android APK 開發、部署或實機驗證；裝置盤點工具已加入原始碼，可在取得授權的 Android 裝置上執行。**

## License

新程式碼的專案授權選型待完成相容性盤點；未經確認不得直接複製上游 GPL、Apache 或其他授權的程式碼。
