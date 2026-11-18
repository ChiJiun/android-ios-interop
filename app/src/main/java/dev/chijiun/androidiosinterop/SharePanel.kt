package dev.chijiun.androidiosinterop

import android.content.ActivityNotFoundException
import android.content.ClipData
import android.content.Intent
import android.net.Uri
import android.widget.Toast
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import dev.chijiun.androidiosinterop.core.SharePayloadPolicy

/**
 * Safe, explicit hand-off to Android Sharesheet (LocalSend if installed).
 * No Root, no background discovery, no Apple credentials and no silent uploads.
 */
@Composable
fun SharePanel() {
    val context = LocalContext.current
    var text by remember { mutableStateOf("") }

    fun openSharesheet(intent: Intent) {
        try {
            context.startActivity(Intent.createChooser(intent, "選擇分享應用程式（可選 LocalSend）"))
        } catch (_: ActivityNotFoundException) {
            Toast.makeText(context, "目前沒有可使用的分享應用程式", Toast.LENGTH_SHORT).show()
        }
    }

    val picker = rememberLauncherForActivityResult(
        ActivityResultContracts.OpenMultipleDocuments()
    ) { selected: List<Uri> ->
        if (selected.isNotEmpty()) {
            val clipboard = ClipData.newUri(context.contentResolver, "選擇的檔案", selected.first())
            selected.drop(1).forEach { clipboard.addItem(ClipData.Item(it)) }
            val share = Intent(Intent.ACTION_SEND_MULTIPLE).apply {
                type = "*/*"
                putParcelableArrayListExtra(Intent.EXTRA_STREAM, ArrayList(selected))
                clipData = clipboard
                addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
            }
            openSharesheet(share)
        }
    }

    Card(modifier = Modifier.fillMaxWidth()) {
        Column(
            modifier = Modifier.padding(14.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            Text("跨平台分享入口（實驗性）", style = MaterialTheme.typography.titleMedium)
            Text(
                "使用 Android 系統分享選單；如已安裝 LocalSend，可由你自行選擇。"
                    + " 這不是真正的 Apple AirDrop，iPhone 也需安裝 LocalSend。",
                style = MaterialTheme.typography.bodySmall,
            )
            OutlinedTextField(
                value = text,
                onValueChange = { text = it },
                modifier = Modifier.fillMaxWidth(),
                label = { Text("要分享的文字") },
                maxLines = 3,
                supportingText = { Text("僅在你按下分享後才交給所選 App") },
            )
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Button(
                    enabled = SharePayloadPolicy.canShareText(text),
                    onClick = {
                        val share = Intent(Intent.ACTION_SEND).apply {
                            type = "text/plain"
                            putExtra(Intent.EXTRA_TEXT, text)
                        }
                        openSharesheet(share)
                    },
                ) {
                    Text("分享文字")
                }
                Button(onClick = { picker.launch(arrayOf("*/*")) }) {
                    Text("選擇檔案")
                }
            }
            Text("沒有 Root、儲存空間全域權限或背景掃描。請確認接收對象。", style = MaterialTheme.typography.labelSmall)
        }
    }
}
