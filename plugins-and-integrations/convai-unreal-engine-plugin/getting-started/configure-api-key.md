---
title: Configure your API key
description: Sign in through the Convai editor window to store your API key and allow the plugin to send authenticated requests to Convai.
last_reviewed: "4.0.0-beta.21"
---

The Convai Unreal Engine plugin authenticates through the Convai editor window. Signing in stores your API key in `UConvaiSettings.API_Key` (a read-only config property) so all runtime requests are authenticated automatically. You do not edit this value directly.

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

Follow the authentication flow in the window. When authentication is complete, close the sign-in panel.
{% endstep %}

{% step %}
### Verify your login

Click the Convai icon in the toolbar again. The Convai editor window should now show your account dashboard with your login details visible. This confirms that the API key has been stored successfully.
{% endstep %}
{% endstepper %}

{% hint style="info" %}
The API key is stored as a read-only `Config` property on `UConvaiSettings`. It is managed entirely by the Convai editor window — do not edit it in **Project Settings** or in config files manually. The window calls `SetAPIKey()` and `SaveSettings()` internally.
{% endhint %}

## Verify the key is active

After signing in, place any character with a `UConvaiChatbotComponent` (or use the bundled demo) and enter Play mode. If the character responds to input, authentication is working. If requests fail, confirm the API key is stored (check **Edit > Project Settings > Convai** and verify the key is not blank) and that your account is active on the Convai dashboard.

## Next steps

With authentication configured, run the bundled demo to verify the full pipeline works before building your own scene: [Run the bundled demo](import-and-run-sample-scenes.md).
