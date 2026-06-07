---
title: Configure your API key
description: Sign in through the Convai editor window to store your API key and allow the plugin to send authenticated requests to Convai.
last_reviewed: "4.0.0-beta.21"
---

The Convai Unreal Engine plugin authenticates through the Convai editor window. Signing in stores your API key in `UConvaiSettings.API_Key` so all runtime requests are authenticated automatically. You do not edit this value directly — the Convai editor window manages it entirely.

## Open the Convai editor window

After enabling the plugin and restarting the editor, the Convai editor window may open automatically. If it does not:

- Click the **Convai** icon in the Unreal Editor toolbar.

The window opens and shows a sign-in form if you are not yet authenticated.

## Sign in

{% stepper %}
{% step %}
### Enter your Convai credentials

In the Convai editor window, sign in with your Convai account credentials. If you do not have an account, create one at <code class="expression">space.vars.dashboard_url</code>.
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

{% hint style="info" %}
The API key is stored as a read-only `Config` property on `UConvaiSettings`. It is managed entirely by the Convai editor window — do not edit it in **Project Settings** or in config files manually. The window calls `SetAPIKey()` and `SaveSettings()` internally.
{% endhint %}

## Verify the key is active

**Expected outcome:** Place any character with a `UConvaiChatbotComponent` and enter Play mode. If the character responds to input, authentication is working. For a guided first test, see [Explore the sample Blueprints](import-and-run-sample-scenes.md).

**If requests fail:**

| Check | Action |
|---|---|
| API key is blank | Go to **Edit > Project Settings > Plugins > Convai** and confirm the key field is populated. If it is empty, sign in again through the Convai editor window. |
| Account is inactive | Sign in to <code class="expression">space.vars.dashboard_url</code> and confirm your account status. |
| Network blocked | Ensure the editor can reach Convai's endpoints. See [Prerequisites — Network access](prerequisites.md#network-access). |
| Convai editor window does not appear (UE 5.0–5.1) | The ConvaiEditor module is disabled on UE 5.0 and 5.1. Enter your API key directly in **Edit > Project Settings > Plugins > Convai > API Key**. |

## Next steps

{% content-ref url="import-and-run-sample-scenes.md" %}
[Explore the sample Blueprints](import-and-run-sample-scenes.md)
{% endcontent-ref %}
