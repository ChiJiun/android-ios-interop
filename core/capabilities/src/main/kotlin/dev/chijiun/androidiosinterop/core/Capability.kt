package dev.chijiun.androidiosinterop.core

/**
 * No feature is marked usable before its module implements and verifies the
 * associated operation on a real target device.
 */
enum class CapabilityId {
    AIRDROP_QUICK_SHARE,
    LAN_FILE_SHARING,
    AIRPLAY_RECEIVER,
    AIRPLAY_SENDER,
    AIRPODS,
    APPLE_TV_REMOTE,
    DYNAMIC_ISLAND,
    STANDBY,
    CONTINUITY,
    APPLE_SERVICES,
    ANDROID_AGENT,
    SYSTEM_BIOMETRICS,
}

enum class SupportLevel { RESEARCH, NOT_SUPPORTED, AVAILABLE }

data class Capability(
    val id: CapabilityId,
    val titleZhTw: String,
    val descriptionZhTw: String,
    val support: SupportLevel,
    val requiresRoot: Boolean,
)

/**
 * Authoritative inventory for UI capabilities, deliberately conservative.
 * Root-only work is never enabled automatically.
 */
object CapabilityRegistry {
    private val inventory = listOf(
        Capability(CapabilityId.AIRDROP_QUICK_SHARE, "AirDrop / Quick Share", "裝置相容性研究，尚未驗證", SupportLevel.RESEARCH, false),
        Capability(CapabilityId.LAN_FILE_SHARING, "區網檔案分享", "LocalSend 類替代方案待整合", SupportLevel.RESEARCH, false),
        Capability(CapabilityId.AIRPLAY_RECEIVER, "AirPlay 接收", "需要相容的 Apple 裝置驗證", SupportLevel.RESEARCH, false),
        Capability(CapabilityId.AIRPLAY_SENDER, "AirPlay 發送", "協定與投影權限待研究", SupportLevel.RESEARCH, false),
        Capability(CapabilityId.AIRPODS, "AirPods", "Bluetooth 功能相容性待研究", SupportLevel.RESEARCH, false),
        Capability(CapabilityId.APPLE_TV_REMOTE, "Apple TV 遙控", "配對與認證機制待研究", SupportLevel.RESEARCH, false),
        Capability(CapabilityId.DYNAMIC_ISLAND, "動態島", "先比較 Hyper Island 現有能力", SupportLevel.RESEARCH, false),
        Capability(CapabilityId.STANDBY, "待機模式", "需評估耗電與防烙印設計", SupportLevel.RESEARCH, false),
        Capability(CapabilityId.CONTINUITY, "跨裝置接力", "Android 背景存取需使用者同意", SupportLevel.RESEARCH, false),
        Capability(CapabilityId.APPLE_SERVICES, "Apple 服務", "非 iOS App Store，僅研究官方與橋接服務", SupportLevel.RESEARCH, false),
        Capability(CapabilityId.ANDROID_AGENT, "手機 Agent", "需要使用者授權的 ADB / Android API", SupportLevel.RESEARCH, false),
        Capability(CapabilityId.SYSTEM_BIOMETRICS, "系統級生物辨識", "需 HAL / TEE 與安全級別驗證", SupportLevel.RESEARCH, true),
    )

    fun all(): List<Capability> = inventory.toList()
    fun find(id: CapabilityId): Capability = inventory.first { it.id == id }
    fun installableWithoutRoot(): List<Capability> =
        inventory.filter { it.support == SupportLevel.AVAILABLE && !it.requiresRoot }
}
