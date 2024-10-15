---
description: Render other language character transcripts
---

# Language Support

Convai offers comprehensive transcript and voice support for a wide range of languages. To facilitate seamless integration, our Unity plugin comes with a custom TextMeshPro (TMP) package, which includes essential fonts and required settings for major languages.

To implement these language-specific features in your project:

1. Navigate to the Convai Setup Window within Unity.
2. Locate the Package Management section.
3. Click on the "Convai Custom TMP Package" button.

{% hint style="warning" %}
This requires TMP essentials pre-installed, which can be done through TextMeshPro option in the Window tab or through a prompt on starting the project.&#x20;
{% endhint %}

<figure><img src="../../../.gitbook/assets/Doc.png" alt=""><figcaption></figcaption></figure>

Once installed, just import your character for which you require the language support, talk with it and the font will automatically render in the transcript.

For now, we provide fonts for these langauges:

* Arabic
* Japanesec
* Korean
* Chinese

## RTL Support

We also provide support for Right-to-Left languages, like Urdu, Persian and Arabic through our Chat UIs.  So, for example, if you talk with an Arabic character or if the character's name is in Arabic, the text will automatically enable the RTL feature provided by unity to reflect proper transcripts.

<figure><img src="../../../.gitbook/assets/image.png" alt=""><figcaption></figcaption></figure>
