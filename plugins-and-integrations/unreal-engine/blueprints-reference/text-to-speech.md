# Text To Speech

### Text To Speech

*   **Description:** Creates audio for the corresponding text.

    <figure><img src="../../../.gitbook/assets/image (137).png" alt=""><figcaption></figcaption></figure>



**Inputs:**

* **Transcript:** The transcript for the audio.
* **Voice:** The voice name.

{% hint style="info" %}
For the list of supported voices please refer to the [table](../../../reference/core-api-reference/standalone-voice-api/text-to-speech-api/#list-of-available-voices-and-their-supported-audio-file-encodings) in Text To Speech API.
{% endhint %}

**Outputs:**

#### ✅ \[On Success]

* **Wave:** Audio response.

#### ⛔ \[On Failure]&#x20;

_Nothing is returned, check logs for details on why it failed._
