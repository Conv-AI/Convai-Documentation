# Changelogs

## Version 3.0.0（current）

Released: Jun 13, 2024

### **What's Changed**

#### **NPC2NPC System**

* Implemented NPC2NPC conversation flow system.
* Added handling for conversation interruptions and restarts.
* Enhanced conversation history tracking and flow management.

#### **Narrative Design**

1. Added Narrative Design-related files and trigger narrative section function.
2. Refactored Narrative Design API, created new behavior trees for movement and added section change events.
3. **Folder Restructuring**
   * Complete folder and scripts folder restructure
4. **Gender-Based Animator:** Added gender-based Animator controller
5. **Feedback System**
   * Implemented a feedback system with thumb icons and animations
   * Updated Transcript UI Prefabs with feedback buttons
6. **Convai Custom Packages:** Updated Convai Custom Package Installer and added iOS DLL Downloader
7. **Scene Perception:** Added feature to allow players to point at game objects and talk about them

### **Improvements**

1. **Texture and Material Compression**
   * Compressed Amelia and other images (POT and Crunch)
   * Updated image names and removed unused image assets
2. **UI Updates**
   * Updated UI prefabs, including Transcript UI, Mobile UI, and Mobile QA UI
   * Transcript UIs and text updated
   * Updated logos and logo paths
3. **System Improvements**
   * Refactored Lipsync system with added teeth support and implemented facial expression proto files
   * Updated ConvaiURPConverterPackage, burst and TMPro packages; Convai Custom Package Installer/Exporter
   * Updated NavMesh and NPC2NPC character rotation
   * Added new demo scene and RPM characters
   * Updated various demo scenes for consistency
4. **Microphone Manager:** Updated Microphone Manager to a singleton class
5. **API Key Access:** Simplified API Key access                                                                               &#x20;
6. **Convai Scene Template:** Created new scene template and dynamic input system assigner
7. **Demo Scenes**
   * Added NPC2NPC demo scene
   * Added Narrative Design demo scene
   * Added new demo scene with all features encompassed
   * "Convai Essentials" prefab for desktop and mobile
8. **Lipsync Overhaul**
   * Overhauled lipsync system, added AR-Kit and Reallusion character support
   * Updated version and added various improvements to frame processing
9. **Input System**
   * Added new input system pragma checks and Convai Character Layer
   * Simplified Input Manager and ensured future-proofing\


### **Bug Fixes**

1. **Transcript UI Bug Fixes:** Fixed bugs and improved system for Transcript UI character list
2. **Microphone Permission:** Fixed Android and iOS microphone permission issues

## Version 2.1.0

### What's Changed

1. VR Support: Implement Virtual Reality features to create a fully immersive experience with the press of a button.&#x20;
2. AR Support: Integrate Augmented Reality capabilities, allowing characters and environments to interact with you in the real world with the press of a button.&#x20;
3. Settings Panel: Introduce a comprehensive settings panel that allows users to customize their experience.
4. Microphone Test System: Incorporate a microphone testing feature to ensure optimal audio input quality.&#x20;
5. Notification System: Implement a robust notification system to inform users of in-game events - specifically microphone-based issues.
6. Input Manager: Develop a custom input management system that supports various input devices such as keyboards, gamepads, and touchscreens using Unity's new Input System.&#x20;

### Bugs and Improvement

1. Fixed: Head Tracking Doesn’t Work Without Action Component issue fixed.
2. Improvement: Added support for a customizable and dynamic Chatbox.
3. Improvement: Improved Lip-Sync Smoothing and audio-visual synchronization.
4. Improvement: Implement Action Events and Event Callbacks.
5. Improvement: Improved Logging System.
6. Improvement: Added ability to interrupt Character Response with Voice Interruption.
7. Improvement: Improved mobile platform transcription UI.

## Version 2.0.0

### What's Changed

1. Lip-sync: Integrate off-the-shelf Lip-sync for Reallusion and Oculus-based Characters.
2. Text-in Voice-out: Chat with the character using text.
3. Character Importer: Import Ready Player Me characters created on the Convai Playground.
4. Feature Control System: Enable Convai features as needed through the Convai NPC component.
5. Logging System: Have better control over what Convai information you see on the debug console.
6. Enhanced player controller: Automatically triggers the characters when you focus on them and then deactivates them when your focus has shifted.
7. URP Upgrader: Upgrade the Render Pipeline to Universal Render Pipeline with the URP Upgrader package (present in the Convai Folder).
8. UI Improvements: Improved user experience with automatically fading UI canvas.

### Bugs and Improvement

1. Fixed: Unlocking the cursor will still cause the first-person camera to move around.
2. Fixed: Exiting play mode before the character is done speaking will cause Unity to crash or not complete compilation.
3. Fixed: Extra space between multiple chunks of text in the UI Text Fields.
4. Fixed: Actions crashing the Android scene.
5. Fixed: Empty responses from the server will not crash the game but only throw an error.
6. Improvement: Smoothened Blinking.
7. Improvement: Smoothened Gaze-Following-based Neck movement.
8. Improvement: Plugin structure reorganization.
