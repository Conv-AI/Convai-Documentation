---
description: >-
  Deploy the Convai Unity SDK on any supported platform — covers what requires
  extra configuration on WebGL, iOS, Android, and XR headsets before shipping.
---

# Platform Guides

### Supported Platforms

The Convai Unity SDK runs on every platform Unity supports. Core features — voice conversation, lip sync, actions, emotion, and long-term memory — work without platform-specific changes. What changes between platforms is how the operating system or browser handles microphone access, audio playback, and camera permissions. These guides cover exactly that: what needs extra configuration, what behaves differently, and what to validate before shipping.

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Windows, macOS, and Linux</strong><br>Full feature support on all desktop targets — no extra configuration needed. Screen share is desktop-exclusive.</td><td><a href="/broken/pages/46aafe96f383fa3f67f8e70d49aab228928c510d">Broken link</a></td></tr><tr><td><strong>WebGL</strong><br>Browser audio constraints, HTTPS requirement, and gesture-gated microphone activation before first voice session.</td><td><a href="/broken/pages/7c410cfd4d9c7504b0c12683359a3fe4f6621a03">Broken link</a></td></tr><tr><td><strong>iOS and Android</strong><br>Declare microphone and camera permissions before shipping — omitting them causes crashes and App Store rejection.</td><td><a href="/broken/pages/4f132625c6b360c93d5ca4510a5d0fdaf715f34e">Broken link</a></td></tr><tr><td><strong>XR Headsets</strong><br>Vision passthrough setup for Meta Quest 3 and 3S — all other core features work without extra configuration.</td><td><a href="/broken/pages/948faa2b1e0b88993f107ea560c24e180385fe68">Broken link</a></td></tr></tbody></table>
