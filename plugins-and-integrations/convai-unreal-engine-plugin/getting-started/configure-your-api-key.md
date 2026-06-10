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

## Where the API key is stored locally

Signing in through the Convai editor window does not keep the API key only in memory. The plugin saves it to your project on disk.

| Item | Location |
|---|---|
| Config file | `Config/DefaultEngine.ini` in your Unreal project folder |
| Config section | `[/Script/Convai.ConvaiSettings]` |
| Field name | `API_Key` |
| Runtime object | `UConvaiSettings.API_Key` (loaded from that config section) |

After sign-in on UE 5.2+, the Convai editor window writes the key to `DefaultEngine.ini` automatically. The **API Key** field under **Edit > Project Settings > Plugins > Convai** is read-only — it displays the value saved in that file.

Example of what appears in `Config/DefaultEngine.ini`:

{% code title="Config/DefaultEngine.ini" %}
```ini
[/Script/Convai.ConvaiSettings]
API_Key=your_api_key_here
```
{% endcode %}

The same file and section are used when you add the key manually on UE 5.0 and 5.1. If you use an auth token later, the plugin can also persist `AuthToken` in this section.

Do not commit `Config/DefaultEngine.ini` to a public repository when it contains your API key. See [Connection and API key issues](../troubleshooting/connection-and-api-key-issues.md) for version-control guidance.

## Remove or clear the API key

Clear the key when you switch Convai accounts, remove Convai from a shared project, or prepare a build that must not ship a stored API key.

{% tabs %}
{% tab title="Convai editor window (UE 5.2+)" %}

{% stepper %}
{% step %}
### Open the account menu

In the Convai editor window, click the account control in the top-right corner (two letters from your account name).
{% endstep %}

{% step %}
### Sign out

Select **Sign out**. The plugin clears `API_Key`, `AuthToken`, and cached account details for this project and writes the empty values back to `Config/DefaultEngine.ini`.
{% endstep %}

{% step %}
### Confirm the key is gone

Open **Edit > Project Settings > Plugins > Convai** and confirm the **API Key** field is empty. Sign in again when you need to reconnect a Convai account.
{% endstep %}
{% endstepper %}

See [Sign in and manage your account](../editor-window/sign-in-and-manage-your-account.md) for the full sign-out flow.

{% endtab %}

{% tab title="DefaultEngine.ini (all UE versions)" %}

{% stepper %}
{% step %}
### Close the editor

Close Unreal Editor before editing `Config/DefaultEngine.ini` so the file is not overwritten on shutdown.
{% endstep %}

{% step %}
### Clear the credential fields

Open `Config/DefaultEngine.ini` in your project folder. Under `[/Script/Convai.ConvaiSettings]`, remove the `API_Key` line or set it to an empty value. If present, clear `AuthToken` the same way.

{% code title="Config/DefaultEngine.ini" %}
```ini
[/Script/Convai.ConvaiSettings]
API_Key=
AuthToken=
```
{% endcode %}
{% endstep %}

{% step %}
### Restart the editor

Restart Unreal Editor. Open **Edit > Project Settings > Plugins > Convai** and confirm the **API Key** field is empty.
{% endstep %}
{% endstepper %}

Use this method on UE 5.0 and 5.1, or when you need to remove a key without opening the Convai editor window.

{% endtab %}
{% endtabs %}

For packaged applications, `DefaultEngine.ini` is included in the build. Clear `API_Key` before packaging if you use a [personal access token](../advanced-topics/personal-access-token.md) at runtime instead.

## Verify the key is active

To confirm your API key is working, proceed to [Add your first Convai character](add-your-first-convai-character.md) and complete the conversation test.

## Prepare authentication for production

The API key flow above is the fastest way to validate the plugin in the editor and during early development. When you ship a **packaged application**, avoid embedding the real API key in the build — packaged project files and config can be inspected.

For production builds, use a **personal access token** flow instead: your backend stores the real API key, generates a short-lived `apiAuthToken`, and the Unreal project sets that token at runtime before a Convai session starts. Do not ship a real API key inside a packaged build.

{% content-ref url="../advanced-topics/personal-access-token.md" %}
[Use personal access tokens](../advanced-topics/personal-access-token.md)
{% endcontent-ref %}

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
