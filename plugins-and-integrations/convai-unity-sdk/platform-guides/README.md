---
title: Platform guides
description: >-
  Deploy the Convai Unity SDK on any supported platform — covers what requires
  extra configuration on WebGL, iOS, Android, and XR headsets before shipping.
last_reviewed: "4.5.0"
---

The Convai Unity SDK 4.5.0 contains native, mobile, XR, and WebGL integration paths, but it does not claim support for every Unity build target. Platform behavior differs around native libraries, microphone access, audio playback, browser gestures, and camera permissions. Use these guides as setup guidance, then validate the distributed SDK artifact on the exact devices, operating systems, browsers, and hosting environment you plan to ship.

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Windows, macOS, and Linux</strong><br>Review native desktop requirements, microphone behavior, architectures, and the checks required before distribution.</td><td><a href="windows-macos-and-linux.md">windows-macos-and-linux.md</a></td></tr><tr><td><strong>WebGL</strong><br>Configure secure hosting, browser audio, gesture-gated capture, and canvas-based Vision.</td><td><a href="webgl.md">webgl.md</a></td></tr><tr><td><strong>iOS and Android</strong><br>Configure microphone and camera permissions, then validate the native media path on physical devices.</td><td><a href="ios-and-android.md">ios-and-android.md</a></td></tr><tr><td><strong>XR Headsets</strong><br>Review Android or Windows XR requirements and configure Meta Quest passthrough Vision when needed.</td><td><a href="xr-headsets.md">xr-headsets.md</a></td></tr></tbody></table>
