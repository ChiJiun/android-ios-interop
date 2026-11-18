# Upstream license and provenance register

This is a **candidate evaluation**, not permission to copy code. The listed license claims are preliminary and MUST be checked against the exact upstream revision, its LICENSE file, included dependencies, assets, and build artifacts before reuse. No upstream source is vendored by this document.

| Upstream | Intended use | Preliminary license / gate | Integration decision |
| --- | --- | --- | --- |
| [LocalSend](https://github.com/localsend/localsend) | Cross-platform file sharing | Apache-2.0 claimed in Issue #6; verify revision and dependency notices | Prefer separate installed app via Android Sharesheet; no vendoring |
| [KDE Connect Android](https://github.com/KDE/kdeconnect-android) | Continuity / sharing reference | GPL family; verify exact license and dependencies | Separate application/protocol reference; legal review before copying |
| [BlueBubbles](https://github.com/BlueBubblesApp) | iMessage bridge | Check exact client/server repository and license independently | External app and user-operated macOS server only |
| [pyatv](https://github.com/postlund/pyatv) | Apple TV protocol reference | Verify exact revision, license and dependencies | Protocol reference; do not copy until reviewed |
| [UxPlay](https://github.com/FDH2/UxPlay) | AirPlay receiver reference | Verify GPL and bundled components | Keep standalone; evaluate redistribution obligations |
| [android-airplay-server](https://github.com/jqssun/android-airplay-server) | Android receiver candidate | GPL-3.0 claimed in Issue #7; verify revision | No code import without copyleft review |
| [Kite](https://github.com/itsHenry35/Kite) | Android sender candidate | LGPL-3.0 claimed in Issue #8; verify revision and linking obligations | No code import until reviewed |
| [CAPod](https://github.com/d4rken-org/capod) | AirPods capability reference | License not verified | Separate app reference only |
| [LibrePods](https://github.com/kavishdevar/librepods) | AirPods capability reference | License not verified | Separate app reference only |
| [scrcpy](https://github.com/Genymobile/scrcpy) | Agent screen/control reference | License and native dependencies to verify | Prefer separate user-installed executable |
| [Shizuku](https://github.com/RikkaApps/Shizuku) | Optional privilege mediation | License and API version to verify | Optional adapter; no mandatory privileged path |

## Mandatory intake record before any source reuse
For each imported component record:
1. Canonical repository URL and immutable upstream commit SHA (never a floating branch).
2. SPDX license identifier(s), license file, copyright notices, exceptions, and dependency/asset licenses.
3. Exact source paths and whether code is copied, modified, dynamically linked, statically linked, or used as a separately installed application.
4. Distribution obligations, attribution and source availability requirements; patent and trademark constraints.
5. Security review, update strategy, pinned dependency hashes, and vulnerability handling.
6. Approved integration decision, reviewer, date, and downstream NOTICE / SBOM entry.

A permissive top-level license does not automatically license embedded proprietary firmware, Apple protocols, bundled libraries or third-party media. GPL/LGPL compatibility and distribution obligations require review of the actual integration model. If licensing cannot be verified, do not import or redistribute.

## Release gate
Produce an SBOM and third-party notices from the **resolved** dependency graph, check all distributed artifacts for unknown binaries, verify license compatibility and dependency provenance, and record an explicit approval for every vendored upstream. Do not claim this gate has passed until evidence exists.
