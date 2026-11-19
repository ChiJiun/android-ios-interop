package dev.chijiun.androidiosinterop.core

/**
 * Only user-entered text is handed to Android's system Sharesheet.
 * Never reads clipboard, background files, message content or Apple credentials.
 */
object SharePayloadPolicy {
    const val MAX_TEXT_LENGTH = 10_000
    const val MAX_FILE_COUNT = 50
    fun canShareFiles(count: Int): Boolean = count in 1..MAX_FILE_COUNT
    fun canShareText(text: String): Boolean =
        text.isNotBlank() && text.length <= MAX_TEXT_LENGTH
}
