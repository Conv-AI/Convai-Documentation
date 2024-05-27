# Downloads

<table><thead><tr><th width="211">Version</th><th width="325">Features</th><th>Download Link</th></tr></thead><tbody><tr><td>Unity Verified Solution</td><td>This is the Long-Term Support version of our core version. It contains all the necessary tools for adding conversational AI to your characters. </td><td><a href="https://assetstore.unity.com/packages/tools/ai/npc-ai-dialog-actions-and-general-intelligence-by-convai-235621"><strong>Download here.</strong></a></td></tr><tr><td>WebGL</td><td>This plugin version should be used if you need to build for WebGL. Please ensure that Git is installed on your computer prior to proceeding.</td><td><a href="https://github.com/Conv-AI/Convai-Unity-WebGL-SDK/releases"><strong>Download here.</strong></a></td></tr></tbody></table>

### Limitations of WebGL

#### Size Constraints

iOS browsers impose strict limitations on the size of WebGL builds. These constraints are primarily due to:

* Memory Limits: iOS devices have limited available memory for web applications, which can affect the performance and feasibility of running large WebGL builds.
* Browser Storage Quotas: Safari and other iOS browsers restrict the amount of data that can be stored locally. This includes caching and IndexedDB, which are often used to store assets for WebGL builds.

#### Key Limitations

* Maximum Downloadable Asset Size: iOS browsers may restrict the size of individual downloadable assets. Large assets might fail to load, causing the application to break.
* Total Build Size: The total size of all assets combined should ideally be kept under 50-100 MB for smooth performance. Exceeding this limit can lead to crashes or extremely slow loading times.
* Memory Usage: iOS devices typically have less RAM available compared to desktop environments. High memory usage by WebGL builds can result in frequent browser crashes.

#### Browser Compatibility

* Safari: The default browser on iOS, Safari, is generally the best option for WebGL builds, but it still has significant limitations compared to desktop browsers.
* Third-Party Browsers: Other browsers like Chrome or Firefox on iOS use the WebKit engine due to Apple’s restrictions. Therefore, they inherit the same limitations as Safari.
