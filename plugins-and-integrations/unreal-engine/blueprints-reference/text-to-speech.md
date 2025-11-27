---
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/plugins-and-integrations/unreal-engine/blueprints-reference/text-to-speech
---

# Text To Speech

### Text To Speech

*   **Description:** Creates audio for the corresponding text.

    <figure><img src="../../../.gitbook/assets/image (238).png" alt=""><figcaption></figcaption></figure>



**Inputs:**

* **Transcript:** The transcript for the audio.
* **Voice:** The voice name.

{% hint style="info" %}
For the list of supported voices, please refer to the [Voice List API](../../../api-reference/core-api-reference/character-crafting-apis/voice-list-api.md).
{% endhint %}

**Outputs:**

#### ✅ \[On Success]

* **Wave:** Audio response.

#### ⛔ \[On Failure]&#x20;

_Nothing is returned, check logs for details on why it failed._
