---
description: Speech-to-Text - Blueprint Reference for Convai Unreal Engine integration.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/plugins-and-integrations/unreal-engine/blueprints-reference/speech-to-text
---

# Speech To Text

### Speech To Text From Sound Wave

* **Description:** Transcribes the provided audio.

<figure><img src="../../../.gitbook/assets/image (290).png" alt=""><figcaption></figcaption></figure>

**Inputs:**

* **Sound Wave:** The recorded output from the microphone, please take a look over the tutorial/sample project for an example on how to use Convai voice capture component with the API.

**Outputs:**

#### ✅ \[On Success]

**Response:** Contains the text output of the audio file if the API was successful, otherwise might contain information on why the API call failed.

#### ⛔ \[On Failure]&#x20;

_Nothing is returned, check logs for details on why it failed._

### Speech To Text From Sound Wave

* **Description:** Transcribes the provided audio file.

<figure><img src="../../../.gitbook/assets/image (331).png" alt=""><figcaption></figcaption></figure>

**Inputs:**

* **Filename:** The path to the recorded audio file on your local disk, the file should be in a .wav format.

**Outputs:**

#### ✅ \[On Success]

**Response:** Contains the text output of the audio file if the API was successful, otherwise might contain information on why the API call failed.

#### ⛔ \[On Failure]&#x20;

_Nothing is returned, check logs for details on why it failed._
