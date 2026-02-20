---
description: >-
  Import Convai sample content and run a scene to test a conversation
  immediately.
---

# Import & Run Sample Scenes

## Introduction

Sample scenes are the fastest way to verify your installation and API setup end-to-end.

## Prerequisites

* Convai SDK installed
* API key configured successfully

## Step-by-step

{% stepper %}
{% step %}
### Open Package Manager

In Unity, go to **Window → Package Manager**.
{% endstep %}

{% step %}
### Find the Convai package

* Select **In Project** (left panel).
* Click **Convai SDK** (or the installed Convai package).
{% endstep %}

{% step %}
### Import Samples

* Open the **Samples** section in the package details.
* Click **Import** next to a sample (example: `<SAMPLE_NAME>`).
* **Expected result:** A **Samples** folder appears under **Assets**, containing the imported sample content.
{% endstep %}

{% step %}
### Open the sample scene

* Navigate to:
  * `Assets/Samples/Convai SDK for Unity/1.0.0/Convai Sample/Scenes`
* Open the scene:
  * `Convai Basic Scene`
{% endstep %}

{% step %}
### Run the conversation test

* Click **Play**.
* Speak using your microphone **or** type into the Chat UI input field.
* **Expected result:** The character responds. Microphone conversation is **hands-free** (no push-to-talk required).
{% endstep %}
{% endstepper %}

## Troubleshooting

* **Sample doesn’t appear after import**
  * Confirm you imported the sample and check the **Assets/Samples** folder.
* **No voice input detected**
  * Check OS microphone permissions for Unity.
  * Confirm the correct microphone device is selected.
* **No response from character**
  * Confirm API key is set and valid.
  * Check Console for authentication/network errors.

## Conclusion

You’ve successfully imported a sample scene and verified a working conversation. Next, you can integrate Convai into your own scene via **Custom Scene Setup**.

{% hint style="info" %}
**Need help?** For questions, please visit the [**Convai Developer Forum**](https://forum.convai.com/).
{% endhint %}
