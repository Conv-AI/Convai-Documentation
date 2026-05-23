---
title: Platform guides
description: >-
  Deploy the Convai Unity SDK on any supported platform — covers what requires
  extra configuration on WebGL, iOS, Android, and XR headsets before shipping.
last_reviewed: "4.2.0"
---

The Convai Unity SDK runs on every platform Unity supports. Core features — voice conversation, lip sync, actions, emotion, and long-term memory — work without platform-specific changes. What changes between platforms is how the operating system or browser handles microphone access, audio playback, and camera permissions. These guides cover exactly that: what needs extra configuration, what behaves differently, and what to validate before shipping.

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Windows, macOS, and Linux</strong><br>Full feature support on all desktop targets — no extra configuration needed. Screen share is desktop-exclusive.</td><td><a href="windows-macos-and-linux.md">windows-macos-and-linux.md</a></td></tr><tr><td><strong>WebGL</strong><br>Browser audio constraints, HTTPS requirement, and gesture-gated microphone activation before first voice session.</td><td><a href="webgl.md">webgl.md</a></td></tr><tr><td><strong>iOS and Android</strong><br>Declare microphone and camera permissions before shipping — omitting them causes crashes and App Store rejection.</td><td><a href="ios-and-android.md">ios-and-android.md</a></td></tr><tr><td><strong>XR Headsets</strong><br>Platform overview for XR headsets — core features work without extra setup. Includes Meta Quest passthrough Vision configuration.</td><td><a href="xr-headsets.md">xr-headsets.md</a></td></tr></tbody></table>
