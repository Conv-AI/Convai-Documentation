---
title: Sign in and manage your account
description: Sign in to the Convai editor window using email, Google, or GitHub, and review your plan and usage quotas in the Account section.
last_reviewed: "4.0.0-beta.21"
---

The Convai editor window requires you to sign in before the plugin can send requests to Convai. The first time you open the window, a welcome screen appears. After sign-in, the Account section shows your plan details and per-feature usage.

## Prerequisites

- Convai Unreal Engine plugin installed and enabled.
- A Convai account. Create one at <code class="expression">space.vars.dashboard_url</code> if you do not have one.

## Complete the welcome flow

The welcome flow appears the first time you open the editor window, or if your session expires.

{% stepper %}
{% step %}
### Open the Convai editor window

Click the **Convai Editor** button in the Level Editor toolbar, or select **Window > Convai > Open Convai Editor** from the menu bar.

If you have not signed in before, the welcome screen appears automatically.
{% endstep %}

{% step %}
### Click Connect Convai Account

Click the **Connect Convai Account** button. The Convai login page opens inside the editor window.
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
**Screenshot required before publishing:** Capture the Convai login page as it appears inside the editor window. The image must show the email and password fields, the **Login to Convai** button, and the Google and GitHub sign-in icons.
{% endhint %}

<figure><img src="../../../.gitbook/assets/TODO-convai-editor-login-page.png" alt="The Convai login page inside the editor window, showing email and password fields and Google and GitHub sign-in options"><figcaption><p>TODO: Replace with screenshot of the Convai login page inside the editor window.</p></figcaption></figure>

Sign in using one of the available methods:

{% tabs %}
{% tab title="Email and password" %}
Enter your Convai account email address and password, then click **Login to Convai**.
{% endtab %}

{% tab title="Google" %}
Click the **Google** icon below the login form. Your default browser opens to the Google authorization page. Select your Google account and approve access.

Your browser tab then displays: **Authentication Successful! You can now return to Unreal Engine. Please close this window.**

Close the browser tab and return to Unreal Editor. The editor window completes sign-in automatically.
{% endtab %}

{% tab title="GitHub" %}
Click the **GitHub** icon below the login form. Your default browser opens to the GitHub authorization page. Sign in and approve access. After authorization, your browser shows the authentication success message. Close the browser tab and return to Unreal Editor — the editor window completes sign-in automatically.
{% endtab %}
{% endtabs %}

{% hint style="success" %}
Sign-in is complete when the editor window opens to the Home section. The welcome flow does not appear again unless your session expires.
{% endhint %}

## View your account details

Click **Account** in the navigation bar to open the Account section. The following information is displayed:

| Field | Description |
|---|---|
| **Username** | Your Convai account username |
| **Email** | The email address associated with your account |
| **Plan** | Your current subscription plan |
| **Interaction usage** | Number of interactions consumed in the current period |
| **ElevenLabs voice usage** | ElevenLabs voice quota consumed |
| **Core API usage** | Core API calls consumed |
| **Pixel Streaming usage** | Pixel Streaming minutes consumed |
| **Plan expiry date** | Date on which your current plan period ends |
| **Quota renewal date** | Date on which usage quotas reset |

## Troubleshooting

### Sign-in fails

**Symptom:** The login page shows an error after clicking **Login to Convai**, or the window does not advance to the Home section after signing in.

**Cause:** Incorrect credentials, or the editor cannot reach the Convai login page.

**Fix:** Verify your email and password. Confirm that your internet connection is active and that no firewall is blocking outbound HTTPS.

**Verify:** After successful sign-in, the window opens to the Home section.

### OAuth sign-in does not complete

**Symptom:** The browser opens for Google or GitHub authorization, but the editor window does not advance after you close the browser.

**Cause:** The browser was closed before the authorization completed, or the OAuth callback was not received.

**Fix:** Reopen the editor window and repeat the sign-in flow. Ensure you complete the full authorization step in the browser before closing it.

**Verify:** The editor window opens to the Home section.

### Account section shows no usage data

**Symptom:** The Account section is blank or shows placeholder values.

**Cause:** The window has not yet refreshed data from Convai, or the session is no longer valid.

**Fix:** Close and reopen the window. If the welcome flow reappears, sign in again.

**Verify:** The Account section populates with your username, email, and plan details.

## Next steps

{% content-ref url="browse-samples-and-content.md" %}
[Browse samples and content](browse-samples-and-content.md)
{% endcontent-ref %}

{% content-ref url="export-diagnostic-logs.md" %}
[Export diagnostic logs](export-diagnostic-logs.md)
{% endcontent-ref %}
