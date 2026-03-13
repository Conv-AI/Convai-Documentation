---
description: >-
  Add a ready-made chat UI prefab to enable text input and conversation
  transcripts.
---

# Add Chat UI (Transcript UI)

## Introduction

Chat UI is optional, but it’s extremely useful for debugging, testing without voice, and demonstrating text-based conversations.

## Prerequisites

* Convai SDK installed
* A scene with Convai setup

## Step-by-step

{% stepper %}
{% step %}
### Locate the Transcript UI prefab

* In the Project window search bar, search:
  * `TranscriptUI_Chat`
* Make sure your search scope includes **In Packages** or **All**.

<figure><img src="../../../../.gitbook/assets/image (11) (1) (1).png" alt=""><figcaption></figcaption></figure>

* Alternatively, you can use the package path:
  * `Packages/com.convai.convai-sdk-for-unity/Prefabs/TranscriptUI/TranscriptUI_Chat.prefab`
{% endstep %}

{% step %}
### Add the prefab to your scene

* Drag and drop **TranscriptUI\_Chat.prefab** into the scene.
* **Expected result:** The UI appears in the Hierarchy and is visible in Game view (Play Mode).
{% endstep %}

{% step %}
### Ensure an Event System exists

* If your scene does not have an EventSystem:
  * Right-click in Hierarchy → **UI → Event System**
* **Expected result:** An EventSystem exists and UI input works in Play Mode.

<figure><img src="../../../../.gitbook/assets/image (12) (1) (1).png" alt=""><figcaption></figcaption></figure>
{% endstep %}
{% endstepper %}

## Troubleshooting

* **UI doesn’t respond to clicks/typing**
  * Confirm there is exactly one EventSystem in the scene.
* **Prefab not found**
  * Confirm the package is installed correctly.
  * Confirm your Project window search includes “In Packages” or “All”.

## Conclusion

You’ve added the Transcript UI to your scene, enabling text input and readable conversation logs. You can now test conversations via keyboard or microphone.

{% hint style="info" %}
**Need help?** For questions, please visit the [**Convai Developer Forum**](https://forum.convai.com/).
{% endhint %}
