---
title: Sign in and manage your account
description: Connect your Convai account, validate the project API key, and review plan, quota, and usage details inside Unreal Editor.
last_reviewed: "4.0.0-beta.21"
---

The Convai editor window helps you connect the Unreal project to Convai. You can authenticate with your Convai account, then use the Account section to review or edit the stored API key, plan details, and usage quotas.

## Prerequisites

- Convai Unreal Engine plugin installed and enabled.
- Convai Editor window available. See [The Convai editor window](README.md) for editor-window version requirements.
- A Convai account.
- Internet access from Unreal Editor.

## Complete the welcome flow

The welcome flow can appear after Unreal Editor initializes when the project has not completed welcome setup or does not have a valid API key.

{% stepper %}
{% step %}
### Open the Convai editor window

Click the **Convai Editor** button in the Level Editor toolbar, or select **Window > Convai > Open Convai Editor** from the menu bar.

If the **Welcome to Convai** screen is already open, continue with the next step.
{% endstep %}

{% step %}
### Click Connect Convai Account

Click **Connect Convai Account**. The plugin opens the Convai login flow.
{% endstep %}

{% step %}
### Finish authentication

Follow the Convai login flow. Email and password authentication stays in the Convai authentication window. OAuth provider buttons, such as Google or GitHub, open in your external browser.
{% endstep %}

{% step %}
### Wait for the editor window to open

When authentication completes, the plugin validates and stores the API key, closes the authentication window, and opens the Convai editor window.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
Authentication is complete when the Convai editor window opens and the Account section shows a populated API key.
{% endhint %}

## Edit the API key

Use the Account section when you need to update the API key stored for the project.

{% stepper %}
{% step %}
### Open the Account section

Open the Convai editor window and click **Account** in the navigation bar.
{% endstep %}

{% step %}
### Paste the API key

Paste your Convai API key into the **Paste your API key here** field.
{% endstep %}

{% step %}
### Validate the key

The plugin stores the key as you edit the field and validates it. Press Enter or move focus away from the field to force validation.
{% endstep %}
{% endstepper %}

The stored key is written through `UConvaiSettings.API_Key`, which is a `Config` property managed by the plugin.

## View your account details

Click **Account** in the navigation bar to open the Account section.

| Area | What it shows |
|---|---|
| **Account Details** | Current plan, plan expiry, and quota renewal date |
| **API Key** | Editable API key field with visibility toggle |
| **Usages** | Interaction Usage, Elevenlabs Usage, Core API Usage, and Pixel Streaming Usage |

The account menu in the top-right corner shows the cached username and email after the authentication response includes user information.

## Troubleshooting

### Sign-in fails

**Symptom:** The authentication flow does not return to Unreal Editor, or the Convai editor window does not open after login.

**Cause:** The login was not completed, the local callback was not received, or Unreal Editor could not reach Convai.

**Fix:** Repeat the login flow. Keep Unreal Editor open until authentication completes, and confirm that your network allows outbound HTTPS.

**Verify:** The Convai editor window opens and the Account section shows a populated API key.

### Manual API key validation fails

**Symptom:** The Account section shows a validation error after you edit the API key.

**Cause:** The key is empty, mistyped, rejected by Convai, or cannot be validated because the editor has no network access.

**Fix:** Copy the API key again from your Convai account, paste it into the field, and validate it again. Confirm that Unreal Editor can reach Convai over HTTPS.

**Verify:** The validation error clears and the Account section shows the stored API key.

### Account section shows no usage data

**Symptom:** The Account section shows empty or placeholder usage values.

**Cause:** The window has not loaded usage data yet, the API key is invalid, or the editor cannot reach Convai.

**Fix:** Confirm that the API key is populated, then close and reopen the Convai editor window. If the key is invalid, enter a valid key and wait for validation.

**Verify:** The Account section shows plan details and usage bars.

## Next steps

{% content-ref url="export-diagnostic-logs.md" %}
[Export diagnostic logs](export-diagnostic-logs.md)
{% endcontent-ref %}
