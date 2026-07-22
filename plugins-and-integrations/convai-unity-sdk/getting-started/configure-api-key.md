---
title: Configure the API key
last_reviewed: "4.4.0"
description: >-
  Enter and validate your Convai API key in the SDK Settings window so your
  Unity project can authenticate and communicate with Convai characters.
---

The Convai SDK for Unity authenticates every session using an API key tied to your Convai account. You enter this key once in the Unity Editor — it is stored in your project and used automatically at runtime.

{% stepper %}
{% step %}
### Copy your API key

Log in to your Convai dashboard at <code class="expression">space.vars.dashboard_url</code>, navigate to **Account Settings**, and copy your API key.
{% endstep %}

{% step %}
### Open the Credentials section

In the Unity Editor menu bar, open **Convai > Settings** (or **Edit > Project Settings > Convai SDK**). The SDK Settings page opens with a **Credentials** section for API key entry.

**Convai > Account** still shows your plan, quota usage, and a link back to Settings, but no longer has an editable API key field.
{% endstep %}

{% step %}
### Paste and validate the API key

Paste your API key into the **API Key** field, then select **Validate & Save**. Convai checks the key and, if it accepts the key, the SDK saves it to the project.

The status badge next to the button reports the result: **Key valid** when Convai accepts the key, or an error message such as **Key invalid** when it does not.
{% endstep %}

{% step %}
### Verify the key is accepted

Run **GameObject > Convai > Validate Scene Setup**. A missing API key appears as a warning in the validator dialog. If no API key warning appears, your key is configured correctly.

<figure><img src="../../../.gitbook/assets/image (14).png" alt="Scene validator dialog with no missing-API-key warning"><figcaption></figcaption></figure>
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
`Assets/Resources/ConvaiSettings.asset` stores the API key obfuscated (XOR plus Base64), not encrypted — anyone with the SDK source can reverse it. Decide whether to commit this file to source control based on your team's security policy. If the project previously stored the key in plain text, the SDK migrates it to the obfuscated format automatically the first time the Unity Editor loads.
{% endhint %}

## How the key is used at runtime

The SDK reads the key from `ConvaiSettings` via the `ICredentialProvider` interface before initiating any connection to Convai. You do not need to pass the key manually in code — the SDK resolves it automatically on startup.

For production deployments where storing the key in source control is not acceptable, supply credentials from a secure source at runtime instead of relying on `ConvaiSettings`.

{% content-ref url="../advanced-topics/custom-providers/custom-credential-provider.md" %}
[custom-credential-provider.md](../advanced-topics/custom-providers/custom-credential-provider.md)
{% endcontent-ref %}

## Next steps

With your API key in place, import a sample scene to verify the SDK is working before you build your own scene.

{% content-ref url="import-and-run-sample-scenes.md" %}
[import-and-run-sample-scenes.md](import-and-run-sample-scenes.md)
{% endcontent-ref %}
