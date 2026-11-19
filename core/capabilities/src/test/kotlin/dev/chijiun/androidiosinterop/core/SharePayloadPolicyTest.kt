package dev.chijiun.androidiosinterop.core

import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class SharePayloadPolicyTest {
    @Test fun blankTextIsNotShared() {
        assertFalse(SharePayloadPolicy.canShareText(""))
        assertFalse(SharePayloadPolicy.canShareText(" \n\t "))
    }

    @Test fun normalAndChineseTextCanBeShared() {
        assertTrue(SharePayloadPolicy.canShareText("Send with LocalSend"))
        assertTrue(SharePayloadPolicy.canShareText("繁體中文資料測試"))
    }

    @Test fun fileCountMustBeBounded() {
        assertFalse(SharePayloadPolicy.canShareFiles(0))
        assertTrue(SharePayloadPolicy.canShareFiles(1))
        assertTrue(SharePayloadPolicy.canShareFiles(SharePayloadPolicy.MAX_FILE_COUNT))
        assertFalse(SharePayloadPolicy.canShareFiles(SharePayloadPolicy.MAX_FILE_COUNT + 1))
    }

    @Test fun oversizedTextIsBlocked() {
        assertTrue(SharePayloadPolicy.canShareText("a".repeat(SharePayloadPolicy.MAX_TEXT_LENGTH)))
        assertFalse(SharePayloadPolicy.canShareText("a".repeat(SharePayloadPolicy.MAX_TEXT_LENGTH + 1)))
    }
}
