---
title: Configure the API key
description: >-
  Enter your Convai API key in the SDK settings to authenticate your project and
  enable character communication.
last_reviewed: "4.2.0"
---

The Convai SDK for Unity authenticates every session using an API key tied to your Convai account. You enter this key once in the Unity Editor — it is stored in your project and used automatically at runtime.

{% stepper %}
{% step %}
### Copy your API key

Log in to your Convai dashboard at [convai.com](<code class="expression">space.vars.dashboard_url</code>), navigate to **Account Settings**, and copy your API key.
{% endstep %}

{% step %}
### Open the Convai configuration window

In the Unity Editor menu bar, open **Convai > Account**.

The Convai Configuration window opens to the Account section.
{% endstep %}

{% step %}
### Paste the API key

Paste your API key into the **API Key** field.

The key is saved immediately to `Assets/Resources/ConvaiSettings.asset`. No additional save step is required.
{% endstep %}

{% step %}
### Verify the key is accepted

Run **GameObject > Convai > Validate Scene Setup**. A missing API key appears as a warning in the validator dialog. If no API key warning appears, your key is configured correctly.
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
**Screenshot required before publishing:** Capture the Convai Configuration window open to the Account section, showing the API Key field and input area. Mask any real API key value. Use SDK <code class="expression">space.vars.unity_sdk_version</code>.
{% endhint %}

<figure><img src="../../../.gitbook/assets/TODO-convai-configuration-window-api-key.png" alt="Convai Configuration window in the Unity Editor showing the Account section with the API Key input field"><figcaption><p>TODO: Replace with screenshot of the Convai Configuration window (Convai > Account) showing the API Key field.</p></figcaption></figure>

{% hint style="warning" %}
`Assets/Resources/ConvaiSettings.asset` stores the API key in plain text. If your project uses source control, decide whether to commit this file based on your team's security policy.
{% endhint %}

## How the key is used at runtime

The SDK reads the key from `ConvaiSettings` via the `ICredentialProvider` interface before initiating any connection to Convai. You do not need to pass the key manually in code — the SDK resolves it automatically on startup.

For production deployments where storing the key in source control is not acceptable, implement a custom `ICredentialProvider` that reads the key from a secure source.

{% content-ref url="../advanced-topics/custom-providers/custom-credential-provider.md" %}
[Custom credential provider](../advanced-topics/custom-providers/custom-credential-provider.md)
{% endcontent-ref %}

## Next steps

With your API key in place, import a sample scene to verify the SDK is working before you build your own scene.

{% content-ref url="import-and-run-sample-scenes.md" %}
[Import and run sample scenes](import-and-run-sample-scenes.md)
{% endcontent-ref %}
