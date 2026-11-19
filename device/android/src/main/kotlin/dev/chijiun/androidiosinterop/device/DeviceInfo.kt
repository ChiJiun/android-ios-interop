package dev.chijiun.androidiosinterop.device

import android.os.Build

/**
 * A privacy-minimal view of public device properties.
 * Does not read serial numbers, Android ID, IMEI, network identifiers or accounts.
 */
data class DeviceInfo(
    val manufacturer: String,
    val model: String,
    val deviceCodename: String,
    val androidRelease: String,
    val sdkLevel: Int,
) {
    companion object {
        fun current(): DeviceInfo = DeviceInfo(
            manufacturer = Build.MANUFACTURER,
            model = Build.MODEL,
            deviceCodename = Build.DEVICE,
            androidRelease = Build.VERSION.RELEASE,
            sdkLevel = Build.VERSION.SDK_INT,
        )
    }
}
