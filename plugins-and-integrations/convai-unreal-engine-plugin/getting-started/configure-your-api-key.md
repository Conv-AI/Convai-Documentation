---
title: Configure your API key
description: Sign in through the Convai editor window to store your API key and allow the plugin to send authenticated requests to Convai.
last_reviewed: "4.0.0-beta.21"
---

The Convai Unreal Engine plugin authenticates every session using an API key tied to your Convai account. On UE 5.2 and later, sign in through the Convai editor window — the key is stored in `UConvaiSettings.API_Key` and used automatically at runtime. On UE 5.0 and 5.1, add the key to `Config/DefaultEngine.ini` because the Convai editor window is not available and the **API Key** field in Project Settings is read-only on those engine versions.

{% hint style="info" %}
The Convai editor window requires **Unreal Engine 5.2 or later**. If you are on UE 5.0 or 5.1, skip to [UE 5.0 and 5.1 fallback](#ue-5-0-and-5-1-fallback).
{% endhint %}

## Sign in through the Convai editor window (UE 5.2+)

After you enable the plugin and restart the editor, the Convai editor window opens automatically. Follow the sign-in flow in that window — you do not need to open it manually unless the window did not appear.

{% stepper %}
{% step %}
### Complete the automatic sign-in prompt

When the editor reopens, the Convai editor window displays a sign-in form. Sign in with your Convai account credentials. If you do not have an account, create one at [convai.com](https://convai.com).
{% endstep %}

{% step %}
### Confirm authentication

When authentication completes, the Convai editor window shows your account dashboard. Your API key is stored automatically — no separate save step is required.
{% endstep %}

{% step %}
### Verify the key in Project Settings

Open **Edit > Project Settings > Plugins > Convai** and confirm the **API Key** field is populated. This read-only field reflects the key written by the Convai editor window.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
Your API key is now stored. The Convai editor window shows your account dashboard — you are authenticated and ready to use the plugin.
{% endhint %}

If the Convai editor window did not open after restart, click the **Convai Editor** button in the toolbar, or select **Window > Convai > Open Convai Editor**.

## Verify the key is active

To confirm your API key is working, proceed to [Add your first Convai character](add-your-first-convai-character.md) and complete the conversation test.

## UE 5.0 and 5.1 fallback

The Convai editor window is not available on UE 5.0 or 5.1. Add your API key to `DefaultEngine.ini`:

{% stepper %}
{% step %}
### Add the key to DefaultEngine.ini

Open `Config/DefaultEngine.ini` in your project folder. Add or update the `[/Script/Convai.ConvaiSettings]` section with your API key from [convai.com](https://convai.com):

```ini
[/Script/Convai.ConvaiSettings]
API_Key=your_api_key_here
```

Restart the editor after editing the file.
{% endstep %}

{% step %}
### Verify the key in Project Settings

Open **Edit > Project Settings > Plugins > Convai**. The **API Key** field should show the value you set. On UE 5.0 and 5.1 this field is read-only — edit `DefaultEngine.ini` to change the key.
{% endstep %}
{% endstepper %}

## Troubleshooting

### API key is blank after sign-in

**Symptom:** Requests fail and `UConvaiSettings.API_Key` is empty in **Edit > Project Settings > Plugins > Convai**.

**Cause:** Sign-in did not complete, or the key was never saved.

**Fix:** On UE 5.2+, sign in again through the Convai editor window. On UE 5.0/5.1, edit `Config/DefaultEngine.ini` as described above and restart the editor.

**Verify:** Open **Project Settings > Plugins > Convai** and confirm the `API Key` field is populated, then run a conversation test from [Add your first Convai character](add-your-first-convai-character.md).

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

{% content-ref url="add-your-first-convai-character.md" %}
[Add your first Convai character](add-your-first-convai-character.md)
{% endcontent-ref %}
