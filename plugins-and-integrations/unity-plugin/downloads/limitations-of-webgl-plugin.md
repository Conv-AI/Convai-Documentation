---
description: >-
  Understand the limitations of the WebGL plugin for Unity with Convai. Optimize
  your development.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/plugins-and-integrations/unity-plugin/downloads/limitations-of-webgl-plugin
---

# Limitations of WebGL Plugin

### Size Constraints

iOS browsers impose strict limitations on the size of WebGL builds. These constraints are primarily due to:

* Memory Limits: iOS devices have limited available memory for web applications, which can affect the performance and feasibility of running large WebGL builds.
* Browser Storage Quotas: Safari and other iOS browsers restrict the amount of data that can be stored locally. This includes caching and Indexed DB, which are often used to store assets for WebGL builds.

### Key Limitations

* Maximum Downloadable Asset Size: iOS browsers may restrict the size of individual downloadable assets. Large assets might fail to load, causing the application to break.
* Total Build Size: The total size of all assets combined should ideally be kept under 50-100 MB for smooth performance. Exceeding this limit can lead to crashes or extremely slow loading times.
* Memory Usage: iOS devices typically have less RAM available compared to desktop environments. High memory usage by WebGL builds can result in frequent browser crashes.

### Browser Compatibility

* Safari: The default browser on iOS, Safari, is generally the best option for WebGL builds, but it still has significant limitations compared to other desktop browsers.
