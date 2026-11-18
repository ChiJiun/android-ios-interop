# Android App 開發、測試與發行

## 架構與權限邊界

| 模組 | 內容 | 必要權限 |
| --- | --- | --- |
| `:app` | Compose 的能力登錄畫面，顯示狀態與基本裝置資訊 | 無 |
| `:core:capabilities` | 純 Kotlin 功能清單、狀態定義與不可用功能過濾 | 無 Android API |
| `:device:android` | Android `Build` 公開欄位的最小安全包裝 | 無敏感權限 |
| `feature-*`（未建立） | 功能實作時才建立，例如檔案分享、AirPlay | 依需求個別審查 |
| `experimental-root`（未建立） | Root / Kernel 的 **可選、隔離** 實驗，永不自動啟用 | 須另外核准 |

**現階段沒有任何檔案分享、AirDrop、AirPlay、AirPods 或 Root 功能可用。** 不用虛假的「成功啟用」指示誤導使用者。

## 版本與環境

- Kotlin 2.2.20、Android Gradle Plugin 8.13.2、Gradle 8.13、JDK 17。
- `compileSdk=36`、`targetSdk=35`、`minSdk=26`，現有兩支裝置實際 Android 版本仍待確認。
- 使用 Jetpack Compose + Material 3。
- 在 Android Studio 中開啟 Repo 根目錄，選擇 JDK 17 與 Gradle 8.13。專案 **目前沒有包含 Gradle Wrapper 二進位**，因此 CLI 需先安裝 Gradle 8.13；GitHub Actions 會自行下載指定版本，不能把 `./gradlew` 當作已存在的命令。

## 不接手機的建置

```bash
gradle :core:capabilities:test :app:lintDebug :app:testDebugUnitTest :app:assembleDebug
```

產物：`app/build/outputs/apk/debug/app-debug.apk`。Debug 版不能作為簽章受保護的正式釋出；CI 的 APK artifact 只用於測試。

### 實機煙霧測試

```bash
adb devices
adb install -r app/build/outputs/apk/debug/app-debug.apk
adb shell am start -n dev.chijiun.androidiosinterop/.MainActivity
```

驗收清單：

- [ ] App 可在主力 POCO 及 narzo（型號確認後）啟動、不崩潰。
- [ ] 顯示基本機型與 Android 版本；不顯示 IMEI、serial、帳號或裝置唯一 ID。
- [ ] 所有尚未開發的功能都顯示「研究中」，按不到不存在的功能。
- [ ] 不要求 Root、Accessibility、Internet 或檔案存取權限。
- [ ] 繁體中文介面正確顯示，系統英語時名稱仍可辨識。
- [ ] 停止/移除 App 後系統原有功能不變。

### Emulator 測試

- 由 Android Studio AVD Manager 建立 API 35/36 的 Android 虛擬裝置；不要把 VM 的 ARM 資源用於大型模擬器。
- Debug APK 安裝並打開後確認畫面、沒有崩潰、功能狀態均為「研究中」。
- 需要用真實 POCO 的 MediaTek 功能驗證 AirDrop / Wi-Fi / NFC 等時，**Emulator 結果無效**。

## CI 與安全

- CI 範本：`ci/android-ci.yml.example`，規劃對 App、Gradle、模組變更執行 Android lint、JVM Unit Test、Debug APK 組裝。由於遠端 GitHub 權杖缺少 `workflow` scope，現在 **尚未啟用 GitHub Actions 工作流程**；需有適當權限的維護者將範本放到 `.github/workflows/android-ci.yml`。
- 單元測試使用 JUnit；真正的硬體互通要另外連接實機執行。
- CI 只要求 `contents: read`，不包含簽章憑證、Apple ID、API Token、專有 APK。
- 使用 `adb logcat` 或 bugreport 診斷時，僅分享必要截圖和已遮蔽個資的錯誤摘要；預設不把日誌作為 CI Artifact。

## 待驗證項目

- Gradle wrapper 尚未納入；可在具 JDK + Gradle 的環境執行 `gradle wrapper --gradle-version 8.13`，產生 wrapper 後應驗證 `gradle-wrapper.jar` 官方 checksum，並透過獨立 PR 審查。
- 主力與備用手機均未連到目前的遠端 VM，仍缺 Android 實機煙霧測試。
- Root/Kernel 與 iOS 功能開發都屬後續 Issues，不包含在此骨架。
