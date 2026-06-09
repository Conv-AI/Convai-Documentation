---
title: Configure your API key
description: Sign in through the Convai editor window to store your API key and allow the plugin to send authenticated requests to Convai.
last_reviewed: "4.0.0-beta.21"
---

The Convai Unreal Engine plugin authenticates through the Convai editor window. Signing in stores your API key in `UConvaiSettings.API_Key` (a read-only `Config` property) so all runtime requests are authenticated automatically. The editor window writes and saves the key — you do not edit this value directly in **Project Settings**.

{% hint style="info" %}
The Convai editor window requires **Unreal Engine 5.2 or later**. If you are on UE 5.0 or 5.1, skip to [Verify the key is active](#verify-the-key-is-active) and follow the manual entry path in the troubleshooting table.
{% endhint %}

## Open the Convai editor window

After enabling the plugin and restarting the editor, the Convai editor window may open automatically as a welcome prompt. If it does not, open it in one of two ways:

- Click the **Convai Editor** button in the Unreal Editor toolbar.
- In the **Window** menu, open the **Convai** section and select **Open Convai Editor**.

The window opens and shows a sign-in form if you are not yet authenticated.

## Sign in

{% stepper %}
{% step %}
### Enter your Convai credentials

In the Convai editor window, sign in with your Convai account credentials. If you do not have an account, create one at [convai.com](https://convai.com).
{% endstep %}

{% step %}
### Complete authentication

Follow the authentication flow in the window. When authentication completes, close the sign-in panel.
{% endstep %}

{% step %}
### Verify your login

Click the Convai icon in the toolbar again. The Convai editor window should now show your account dashboard with your login details visible. This confirms that the API key has been stored successfully.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
Your API key is now stored. The Convai editor window shows your account dashboard — you are authenticated and ready to use the plugin.
{% endhint %}

## Verify the key is active

To confirm your API key is working, proceed to [Add your first Convai character](add-your-first-character.md) and complete the conversation test.

## UE 5.0 and 5.1 fallback

The Convai editor window is not available on UE 5.0 or 5.1. Use one of these paths instead:

{% stepper %}
{% step %}
### Set the key with a Blueprint utility node

In any Editor Utility Widget or startup Blueprint, call **Set API Key** (`UConvaiUtils::SetAPI_Key`, category **Convai > Settings**) with your API key string from [convai.com](https://convai.com).
{% endstep %}

{% step %}
### Or add the key to DefaultEngine.ini

Add your key under the `[/Script/Convai.ConvaiSettings]` section in `Config/DefaultEngine.ini`:

```ini
[/Script/Convai.ConvaiSettings]
API_Key=your_api_key_here
```

Restart the editor after editing the file.
{% endstep %}
{% endstepper %}

## Troubleshooting

### API key is blank after sign-in

**Symptom:** Requests fail and `UConvaiSettings.API_Key` is empty in **Edit > Project Settings > Plugins > Convai**.

**Cause:** Sign-in did not complete, or the key was never saved.

**Fix:** On UE 5.2+, sign in again through the Convai editor window. On UE 5.0/5.1, call **Set API Key** or edit `DefaultEngine.ini` as described above.

**Verify:** Open **Project Settings > Plugins > Convai** and confirm the `API Key` field is populated, then run a conversation test from [Add your first Convai character](add-your-first-character.md).

### Account is inactive

**Symptom:** Sign-in fails or requests are rejected.

**Cause:** The Convai account is inactive or suspended.

**Fix:** Sign in to [convai.com](https://convai.com) and confirm your account status.

**Verify:** Retry sign-in through the Convai editor window.

### Network blocked

**Symptom:** Sign-in or runtime requests time out.

**Cause:** The editor cannot reach Convai over HTTPS.

**Fix:** Confirm outbound HTTPS access. See [Network access](prerequisites.md#network-access).

**Verify:** Retry sign-in after network access is restored.

## Next steps

{% content-ref url="add-your-first-character.md" %}
[Add your first Convai character](add-your-first-character.md)
{% endcontent-ref %}
