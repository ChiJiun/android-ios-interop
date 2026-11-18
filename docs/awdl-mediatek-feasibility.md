# AWDL / POCO X6 Pro MediaTek Wi-Fi 可行性研究

研究日期：2026-11-18。**未完成 POCO / narzo 實機 RF TX/RX、AWDL Peer Discovery 或真正的 AirDrop 傳檔。**

## 核心結論

Google Quick Share 與 Apple AirDrop 的互通不能只靠編譯可載入的 Kernel Module。分層需求包含 Google Mosey 系統服務、Apple 裝置探索、合法且真正的 802.11 實體收發、AWDL 連線與安全檔案傳輸。載入虛擬 Wi-Fi PHY 不等於完成 RF 傳輸。

## POCO X6 Pro 的公開技術線索

- [MiCode Kernel Issue #41084](https://github.com/MiCode/Xiaomi_Kernel_OpenSource/issues/41084) 回報 `bsp-duchamp-u-oss` 中的 `gen4-mt79xx` 缺少 `chips/soc7_0`、對應 headers 與 Makefile wiring。該 Issue 回報的 Wi-Fi 屬性是 `ro.hardware.wlan.chip=mt6637`，但**本專案尚未在你的實機核對**。
- 其他 Kernel 分支可能存在這些原始碼；即使補齊 Source Tree，也仍要確保專有 Firmware、GKI/ABI、Module Signing、SELinux、AVB 等條件相容。
- [mosey-extended](https://github.com/thelok1s/mosey-extended) 明確標註虛擬 PHY **沒有真正 802.11 RF TX/RX**，非 Pixel 仍處於研究；不應直接宣稱可在 POCO 完成 AirDrop。
- [airdrop-mt7921](https://github.com/jedbillyb/airdrop-mt7921) 在另一種 MediaTek MT7921 裝置研究 OWL／iPhone Peer Discovery 與 Channel Hopping，部分步驟已有實測，但**MT7921 不等於 POCO 的 MT6897 Wi-Fi 裝置**，不能照搬驅動或測試結論。
- [OpenDrop](https://github.com/seemoo-lab/opendrop) 與 [OWL](https://github.com/seemoo-lab/owl) 可參考 AWDL 架構，不是 POCO 現成的 Wi-Fi 驅動。

## 可執行的靜態稽核

在取得授權且對應 duchamp 的 Kernel Source Tree 後，找出 `gen4-mt79xx` 目錄並執行：

```bash
python3 tools/duchamp_wifi_source_audit.py /path/to/gen4-mt79xx --output reports/duchamp-wifi-source.json
python3 -m unittest discover -s tests -v
```

此工具只讀三項：`chips/soc7_0/soc7_0.c`、`include/chips/coda/soc7_0`、`Makefile` 的 SOC7_0 wiring。輸出 **incomplete** 或 **candidate_complete**；兩種結果都明確標示 **未驗證真正 RF TX/RX 或 AirDrop**。不編譯、不刷機、也不呼叫 ADB。

## 階段與完成證據

| 層級 | 需要的證據 | 不能等同 |
| --- | --- | --- |
| L0 | Kernel 原始碼、對應 commit、Makefile 齊全 | 可載入、可操作 RF |
| L1 | 在完全匹配的 Kernel/ABI 成功編譯 | 硬體真正收發封包 |
| L2 | 透過系統公開介面確認 Wi-Fi Driver 能力 | 802.11 RF TX/RX 已成功 |
| L3 | 在合法且同意的測試環境驗證實體收發 | AWDL Peer Discovery |
| L4 | 與 iPhone/Mac 完成 AWDL 探索與同步 | AirDrop 安全配對或檔案傳輸 |
| L5 | 雙向原生 AirDrop 傳檔與雜湊比對 | 所有型號、ROM 或 iOS 通用 |

## 後續工作與安全條件

- [ ] 在 POCO 實機查詢 Android Build、Kernel/ROM 版本及 Wi-Fi Chip，交叉核對官方 Kernel Source。
- [ ] 完整測試前不修改主力手機的 Bootloader、Wi-Fi Driver、SELinux 或分割區。
- [ ] 不使用 narzo 的 Kernel 或 driver 刷入 POCO；兩種硬體不可互換。
- [ ] 實驗必須在可合法控制的設備與 RF 環境中進行；保留回復方案，不分發 Google/Apple/OEM 專有元件。
- [ ] 若來源缺失或韌體不相容，應標記 **Blocked: source/driver/hardware**；優先使用 LocalSend 等非 Root 替代方案。

參考：[AOSP Wi-Fi HAL](https://source.android.com/docs/core/connect/wifi-hal) ／ [mt6897-devs](https://github.com/mt6897-devs)。
