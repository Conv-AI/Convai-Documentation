---
description: >-
  Enter your Convai API key in the SDK settings to authenticate your project and
  enable character communication.
---

# Configure API Key

### Connect Your Project to Convai

The Convai SDK for Unity authenticates every session using an API key tied to your Convai account. You enter this key once in the Unity Editor — it is stored in your project and used automatically at runtime.

{% stepper %}
{% step %}
**Copy Your API Key**

Log in to your Convai dashboard at [convai.com](https://convai.com/), navigate to **Account Settings**, and copy your API key.
{% endstep %}

{% step %}
**Open the Convai Configuration Window**

In the Unity Editor menu bar, open **Convai > Account**.

The Convai Configuration window opens to the Account section.
{% endstep %}

{% step %}
**Paste the API Key**

Paste your API key into the **API Key** field.

The key is saved immediately to `Assets/Resources/ConvaiSettings.asset`. No additional save step is required.
{% endstep %}

{% step %}
**Verify the Key Is Accepted**

Run **GameObject > Convai > Validate Scene Setup**. A missing API key appears as a warning in the validator dialog. If no API key warning appears, your key is configured correctly.
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
`Assets/Resources/ConvaiSettings.asset` stores the API key in plain text. If your project uses source control, decide whether to commit this file based on your team's security policy.
{% endhint %}

### How the Key Is Used at Runtime

The SDK reads the key from `ConvaiSettings` via the `ICredentialProvider` interface before initiating any connection to Convai. You do not need to pass the key manually in code — the SDK resolves it automatically on startup.

For production deployments where storing the key in source control is not acceptable, implement a custom `ICredentialProvider` that reads the key from a secure source. See the Custom Credential Provider guide in Advanced Topics for details.

### Next Steps

With your API key in place, import a sample scene to verify the SDK is working before you build your own scene.

{% content-ref url="/broken/pages/f5ee22f898fef18c646e93691db16ad6cb6fcc17" %}
[Broken link](/broken/pages/f5ee22f898fef18c646e93691db16ad6cb6fcc17)
{% endcontent-ref %}
