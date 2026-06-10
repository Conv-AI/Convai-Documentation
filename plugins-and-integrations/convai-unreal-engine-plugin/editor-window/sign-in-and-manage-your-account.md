---
title: Sign in and manage your account
description: Connect your Convai account through the editor window, sign out to switch accounts, and review plan, quota, and usage details inside Unreal Editor.
last_reviewed: "4.0.0-beta.21"
---

The Convai editor window helps you connect the Unreal project to Convai. Sign in with your Convai account to store the project API key automatically, review plan details and usage quotas in the **Account** section, and sign out from the top-right account menu when you need to use a different account.

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
Authentication is complete when the Convai editor window opens and the **Account** section shows your plan details.
{% endhint %}

## Sign out and switch accounts

Use the account menu in the top-right corner when you need to sign out and connect a different Convai account.

{% stepper %}
{% step %}
### Open the account menu

In the Convai editor window, click the account control in the top-right corner. It shows two letters from your account name.
{% endstep %}

{% step %}
### Sign out

Select **Sign out**. The plugin clears the stored authentication for this project.
{% endstep %}

{% step %}
### Sign in with another account

Repeat the welcome flow above and sign in with the Convai account you want to use. The plugin stores the API key for the new account automatically.
{% endstep %}
{% endstepper %}

## View your account details

Click **Account** in the navigation bar to open the Account section.

| Area | What it shows |
|---|---|
| **Account Details** | Current plan, plan expiry, and quota renewal date |
| **Usages** | Interaction Usage, Elevenlabs Usage, Core API Usage, and Pixel Streaming Usage |

The account menu in the top-right corner shows two letters from your account name, your cached username and email after authentication, and a **Sign out** option.

## Troubleshooting

### Sign-in fails

**Symptom:** The authentication flow does not return to Unreal Editor, or the Convai editor window does not open after login.

**Cause:** The login was not completed, the local callback was not received, or Unreal Editor could not reach Convai.

**Fix:** Repeat the login flow. Keep Unreal Editor open until authentication completes, and confirm that your network allows outbound HTTPS.

**Verify:** The Convai editor window opens and the **Account** section shows your plan details.

### Account section shows no usage data

**Symptom:** The Account section shows empty or placeholder usage values.

**Cause:** The window has not loaded usage data yet, authentication is invalid, or the editor cannot reach Convai.

**Fix:** Close and reopen the Convai editor window. If the data still does not load, sign out from the account menu, sign in again, and wait for the **Account** section to refresh.

**Verify:** The Account section shows plan details and usage bars.

## Next steps

{% content-ref url="export-diagnostic-logs.md" %}
[Export diagnostic logs](export-diagnostic-logs.md)
{% endcontent-ref %}
