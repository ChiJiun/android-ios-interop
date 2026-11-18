package dev.chijiun.androidiosinterop

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import dev.chijiun.androidiosinterop.core.Capability
import dev.chijiun.androidiosinterop.core.CapabilityRegistry
import dev.chijiun.androidiosinterop.core.SupportLevel
import dev.chijiun.androidiosinterop.device.DeviceInfo

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                Surface(modifier = Modifier.fillMaxSize()) {
                    CapabilityScreen()
                }
            }
        }
    }
}

@Composable
private fun CapabilityScreen() {
    val device = remember { DeviceInfo.current() }
    val capabilities = remember { CapabilityRegistry.all() }
    Scaffold { insets ->
        Column(modifier = Modifier.fillMaxSize().padding(insets).padding(16.dp)) {
            Text("Android 互通實驗室", style = MaterialTheme.typography.headlineSmall)
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                "目前僅提供能力盤點。以下功能尚未啟用、也不會要求 Root。",
                style = MaterialTheme.typography.bodyMedium,
            )
            Spacer(modifier = Modifier.height(16.dp))
            Text(
                "裝置：" + device.manufacturer + " " + device.model +
                    " / Android " + device.androidRelease + " (API " + device.sdkLevel + ")",
                style = MaterialTheme.typography.bodySmall,
            )
            Spacer(modifier = Modifier.height(16.dp))
            LazyColumn(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                items(capabilities, key = { it.id.name }) { capability ->
                    CapabilityCard(capability)
                }
            }
        }
    }
}

@Composable
private fun CapabilityCard(capability: Capability) {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(14.dp)) {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                Text(capability.titleZhTw, style = MaterialTheme.typography.titleMedium)
                Text(
                    when (capability.support) {
                        SupportLevel.RESEARCH -> "研究中"
                        SupportLevel.NOT_SUPPORTED -> "不支援"
                        SupportLevel.AVAILABLE -> "可使用"
                    },
                    style = MaterialTheme.typography.labelMedium,
                )
            }
            Spacer(modifier = Modifier.height(5.dp))
            Text(capability.descriptionZhTw, style = MaterialTheme.typography.bodySmall)
            if (capability.requiresRoot) {
                Spacer(modifier = Modifier.height(5.dp))
                Text("需進一步評估 Root / 系統權限", style = MaterialTheme.typography.labelSmall)
            }
        }
    }
}
