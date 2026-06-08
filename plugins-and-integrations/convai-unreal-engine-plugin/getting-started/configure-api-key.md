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
- Select **Window > Convai > Open Convai Editor** from the menu bar.

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

**If requests fail:**

| Check | Action |
|---|---|
| API key is blank | Go to **Edit > Project Settings > Plugins > Convai** and confirm the `API Key` field is populated. If it is empty, sign in again through the Convai editor window. |
| Account is inactive | Sign in to [convai.com](https://convai.com) and confirm your account status. |
| Network blocked | Confirm the editor can reach Convai over HTTPS. See [Network access](prerequisites.md#network-access). |
| UE 5.0 or 5.1 — Convai editor window not available | Enter your API key directly in **Edit > Project Settings > Plugins > Convai > API Key**. The key field is editable in Project Settings when the editor UI is absent. |

## Next steps

{% content-ref url="add-your-first-character.md" %}
[Add your first Convai character](add-your-first-character.md)
{% endcontent-ref %}
