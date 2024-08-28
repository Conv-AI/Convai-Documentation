---
description: Convai Unity Plugin Changelogs - Stay updated with the latest changes.
---

# Changelogs

## Version 3.1.0（current）

Released: Aug 28, 2024

### What's Changed

* New Convai Setup Editor Window
* Long term memory (beta) integration in Unity SDK
* ChatBox UI revamp with RTL support
* Input system revamp and Mobile UI improvements

### **Improvements**

* **UI Improvements**
  * Revamped ChatBox UI
  * Improved mobile UI
  * Implemented chat disabling feature
  * Added usage limit exceeded notification
  * Dialog box added for no API Key scenario
* **API and Backend**
  * Refactored ProcessUserQuery for better transcript handling
  * Implemented fuzzy matching for Action System
  * Ready Player Me and CC\_Tools automatic import process
* **Character and Animation**
  * Updated Character Importer Pipeline
  * Added OVR effectors for RPM characters
  * Fixed animators for all characters
  * Provided Weight Multiplier for LipSync user preference
  * RPM Characters will have Lipsync added when imported\


### **Bug Fixes and Improvements**

* **Bug Fixes**
  * Fixed character resuming dialogue after toggle
  * Fixed section deletion issue in NarrativeDesignManager
  * Fixed layer issues
  * Optimised Convai LipSync
* **Developer Tools and Workflow**
  * Improved Convai Logger System
  * Updated namespace and formatting for all editor scripts
  * Removed CC Tools Folder and other temporary/junk files
  * Added "Update Triggers" button to NarrativeDesignTrigger inspector
  * Implemented approximate string matching for actions system
* **Miscellaneous**
  * Added PlayerDataHandler and PlayerDataSO
  * Updated NPC positions and topics in demo scenes
  * Fixed Convai logo in Convai Setup window



## Version 3.0.1

Released: Jun 21, 2024

### **Bug Fixes and Improvements**

* Fix macOS TMP UGUI render issue in demo scene
* Prefab missing animator
* Updated ActiveNPC layer check logic

## Version 3.0.0

Released: Jun 13, 2024

### **What's Changed**

#### **NPC2NPC System**

* Implemented NPC2NPC conversation flow system.
* Added handling for conversation interruptions and restarts.
* Enhanced conversation history tracking and flow management.

#### **Narrative Design**

* Added Narrative Design-related files and trigger narrative section function.
* Refactored Narrative Design API, created new behavior trees for movement and added section change events.
* **Folder Restructuring**
  * Complete folder and scripts folder restructure
* **Gender-Based Animator:** Added gender-based Animator controller
* **Feedback System**
  * Implemented a feedback system with thumb icons and animations
  * Updated Transcript UI Prefabs with feedback buttons
* **Convai Custom Packages:** Updated Convai Custom Package Installer and added iOS DLL Downloader
* **Scene Perception:** Added feature to allow players to point at game objects and talk about them

### **Improvements**

* **Texture and Material Compression**
  * Compressed Amelia and other images (POT and Crunch)
  * Updated image names and removed unused image assets
* **UI Updates**
  * Updated UI prefabs, including Transcript UI, Mobile UI, and Mobile QA UI
  * Transcript UIs and text updated
  * Updated logos and logo paths
* **System Improvements**
  * Refactored Lipsync system with added teeth support and implemented facial expression proto files
  * Updated ConvaiURPConverterPackage, burst and TMPro packages; Convai Custom Package Installer/Exporter
  * Updated NavMesh and NPC2NPC character rotation
  * Added new demo scene and RPM characters
  * Updated various demo scenes for consistency
* **Microphone Manager:** Updated Microphone Manager to a singleton class
* **API Key Access:** Simplified API Key access                                                                               &#x20;
* **Convai Scene Template:** Created new scene template and dynamic input system assigner
* **Demo Scenes**
  * Added NPC2NPC demo scene
  * Added Narrative Design demo scene
  * Added new demo scene with all features encompassed
  * "Convai Essentials" prefab for desktop and mobile
* **Lipsync Overhaul**
  * Overhauled lipsync system, added AR-Kit and Reallusion character support
  * Updated version and added various improvements to frame processing
* **Input System**
  * Added new input system pragma checks and Convai Character Layer
  * Simplified Input Manager and ensured future-proofing\


### **Bug Fixes**

1. **Transcript UI Bug Fixes:** Fixed bugs and improved system for Transcript UI character list
2. **Microphone Permission:** Fixed Android and iOS microphone permission issues

## Version 2.1.0

### What's Changed

* VR Support: Implement Virtual Reality features to create a fully immersive experience with the press of a button.&#x20;
* AR Support: Integrate Augmented Reality capabilities, allowing characters and environments to interact with you in the real world with the press of a button.&#x20;
* Settings Panel: Introduce a comprehensive settings panel that allows users to customize their experience.
* Microphone Test System: Incorporate a microphone testing feature to ensure optimal audio input quality.&#x20;
* Notification System: Implement a robust notification system to inform users of in-game events - specifically microphone-based issues.
* Input Manager: Develop a custom input management system that supports various input devices such as keyboards, gamepads, and touchscreens using Unity's new Input System.&#x20;

### **Bug Fixes and Improvements**

* Fixed: Head Tracking Doesn’t Work Without Action Component issue fixed.
* Improvement: Added support for a customizable and dynamic Chatbox.
* Improvement: Improved Lip-Sync Smoothing and audio-visual synchronization.
* Improvement: Implement Action Events and Event Callbacks.
* Improvement: Improved Logging System.
* Improvement: Added ability to interrupt Character Response with Voice Interruption.
* Improvement: Improved mobile platform transcription UI.

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
