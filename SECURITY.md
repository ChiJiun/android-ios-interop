# Security policy / 安全政策

## Scope
This repository is an experimental Android interoperability platform. No device, firmware, Apple protocol, or privileged operation should be considered production-safe without a documented device-specific test.

## Reporting vulnerabilities
Do not disclose exploits, credentials, device identifiers, or private logs in public Issues. Contact the repository maintainers through GitHub's private vulnerability reporting feature if enabled; otherwise request a private reporting channel without posting exploit details publicly. Do not claim that a private channel exists until verified.

## Required controls
- Default to standard Android APIs and least privilege. Root, Shizuku, ADB, bootloader unlocking and flashing are optional and separate.
- Never silently execute destructive actions, payment, credential entry, bootloader changes or security bypasses.
- Never collect Apple ID passwords, 2FA codes, IMEI, access tokens, recovery keys or signing keys in reports or telemetry.
- Treat third-party protocol implementations and APKs as untrusted until license, provenance and integrity are reviewed.
- Do not disable SELinux, Verified Boot, DRM or account authentication to make a feature work.
- Store pairing secrets in platform-protected storage; support revocation and clear user consent.
- Keep unknown or untested capabilities disabled by default. Record device, Android API, firmware and exact test evidence without unique identifiers.
- Never publish vendor firmware, proprietary APKs, copyrighted Apple/Google binaries, or undocumented private keys.

## Release security gate
Every release must record: dependency lock/provenance, license notices, static analysis results, Android build and lint evidence, permission diff, reproducible build instructions, and a list of unverified hardware features. Security-sensitive features require negative tests for denied permissions, revoked pairing, and interruption.

## Disclosure handling
Acknowledge privately, reproduce in a controlled environment, fix on a dedicated branch, add regression tests, and coordinate disclosure after a patched release. No response-time SLA is promised.
