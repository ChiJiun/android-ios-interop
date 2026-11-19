package dev.chijiun.androidiosinterop.core

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class CapabilityRegistryTest {
    @Test fun everyFeatureHasExactlyOneStatus() {
        assertEquals(CapabilityId.entries.size, CapabilityRegistry.all().size)
        assertEquals(CapabilityId.entries.toSet(), CapabilityRegistry.all().map { it.id }.toSet())
    }

    @Test fun researchIsNotAdvertisedAsAvailable() {
        assertTrue(CapabilityRegistry.all().all { it.support == SupportLevel.RESEARCH })
        assertTrue(CapabilityRegistry.installableWithoutRoot().isEmpty())
    }

    @Test fun rootOnlyFeatureRemainsOptIn() {
        assertTrue(CapabilityRegistry.find(CapabilityId.SYSTEM_BIOMETRICS).requiresRoot)
        assertFalse(CapabilityRegistry.find(CapabilityId.LAN_FILE_SHARING).requiresRoot)
    }

    @Test fun mutationDoesNotChangeRegistry() {
        val snapshot = CapabilityRegistry.all().toMutableList()
        snapshot.clear()
        assertEquals(CapabilityId.entries.size, CapabilityRegistry.all().size)
    }
}
