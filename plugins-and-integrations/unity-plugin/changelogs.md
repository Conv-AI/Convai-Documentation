# Changelogs

## Version 2.1.0 (current)

### What's Changed

* AR Support: Integrate Augmented Reality capabilities, allowing characters and environments to interact with the real world.&#x20;
* VR Support: Implement Virtual Reality features to create a fully immersive experience.&#x20;
* Settings Panel: Introduce a comprehensive settings panel that allows users to customize their experience.
* Microphone Test System: Incorporate a microphone testing feature to ensure optimal audio input quality.&#x20;
* Notification System: Implement a robust notification system to inform users of in-game events - specifically microphone-based issues.
* Input Manager: Develop an advanced input management system that supports various input devices such as keyboards, gamepads, and touchscreens.

### Bugs and Improvement

* Fixed: Head Tracking Doesn’t Work Without Action Component issue fixed.
* Improvement: Added support for a customizable and dynamic Chatbox
* Improvement: Improved Lip-Sync Smoothing and audio-visual synchronization
* Improvement: Implement Action Events and Event Callbacks
* Improvement: Improved Logging System
* Improvement: Added ability to interrupt Character Response with Voice Interruption
* Improvement: Improved mobile platform transcription UI

## Version 2.0.0

### What's Changed

* Lip-sync: Integrate off-the-shelf Lip-sync for Reallusion and Oculus-based Characters.
* Text-in Voice-out: Chat with the character using text.
* Character Importer: Import Ready Player Me characters created on the Convai Playground.
* Feature Control System: Enable Convai features as needed through the Convai NPC component.
* Logging System: Have better control over what Convai information you see on the debug console.
* Enhanced player controller: Automatically triggers the characters when you focus on them and then deactivates them when your focus has shifted.
* URP Upgrader: Upgrade the Render Pipeline to Universal Render Pipeline with the URP Upgrader package (present in the Convai Folder).
* UI Improvements: Improved user experience with automatically fading UI canvas.

### Bugs and Improvement

* Fixed: Unlocking the cursor will still cause the first-person camera to move around.
* Fixed: Exiting play mode before the character is done speaking will cause Unity to crash or not complete compilation.
* Fixed: Extra space between multiple chunks of text in the UI Text Fields.
* Fixed: Actions crashing the Android scene.
* Fixed: Empty responses from the server will not crash the game but only throw an error.
* Improvement: Smoothened Blinking.
* Improvement: Smoothened Gaze-Following-based Neck movement.
* Improvement: Plugin structure reorganization.
