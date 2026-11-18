package dev.chijiun.androidiosinterop.device

import android.content.Context
import android.content.pm.PackageManager
import android.os.Build

/**
 * Read-only, permission-free capability observations.
 *
 * A reported hardware feature is NOT proof that an Apple protocol works.
 * No Bluetooth/Wi-Fi scans, pairing, privileged commands or unique identifiers.
 */
data class CapabilityObservation(
    val key: String,
    val supported: Boolean?,
    val evidence: String,
)

object RuntimeCapabilities {
    fun inspect(context: Context): List<CapabilityObservation> {
        val pm = context.packageManager
        fun feature(key: String, androidFeature: String): CapabilityObservation =
            CapabilityObservation(key, pm.hasSystemFeature(androidFeature), "PackageManager: $androidFeature")

        val result = mutableListOf(
            feature("bluetooth", PackageManager.FEATURE_BLUETOOTH),
            feature("bluetooth_le", PackageManager.FEATURE_BLUETOOTH_LE),
            feature("wifi", PackageManager.FEATURE_WIFI),
            feature("wifi_direct", PackageManager.FEATURE_WIFI_DIRECT),
            feature("nfc", PackageManager.FEATURE_NFC),
            feature("camera", PackageManager.FEATURE_CAMERA_ANY),
            feature("fingerprint", PackageManager.FEATURE_FINGERPRINT),
            feature("telephony", PackageManager.FEATURE_TELEPHONY),
        )
        result += CapabilityObservation(
            "airdrop_awdl", null,
            "Android public APIs cannot establish AWDL driver support or AirDrop interoperability",
        )
        result += CapabilityObservation(
            "root", null,
            "Not probed: no shell commands, root escalation or filesystem inspection",
        )
        result += CapabilityObservation(
            "android_api", true, "API ${Build.VERSION.SDK_INT}; ABI ${Build.SUPPORTED_ABIS.firstOrNull() ?: "unknown"}",
        )
        return result.toList()
    }
}
