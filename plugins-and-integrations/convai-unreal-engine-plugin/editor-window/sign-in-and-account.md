---
title: Sign in and manage your account
description: Complete the Convai editor window welcome flow, enter your API key, and review your plan and usage quotas in the Account section.
last_reviewed: "4.0.0-beta.21"
---

The Convai editor window requires a valid API key before the plugin can send requests to Convai. The first time you open the window a two-step welcome flow collects and validates the key. After sign-in, the Account section shows your plan details and per-feature usage.

## Prerequisites

- Convai Unreal Engine plugin installed and enabled.
- A Convai account. Create one at <code class="expression">space.vars.dashboard_url</code> if you do not have one.
- Your API key, available on the **API Keys** page of your Convai dashboard.

## Complete the welcome flow

{% stepper %}
{% step %}
### Open the Convai editor window

Click the **Convai Editor** button in the Level Editor toolbar, or select **Window > Convai > Open Convai Editor** from the menu bar.

If you have not signed in before, the welcome screen appears automatically.
{% endstep %}

{% step %}
### Proceed past the welcome screen

The welcome screen gives an introduction to the plugin. Click **Connect Convai Account** to advance to the API key step.
{% endstep %}

{% step %}
### Enter your API key

Paste your API key into the input field and click **Validate & Continue**. The window validates the key against Convai before storing it.
{% endstep %}
{% endstepper %}

{% hint style="info" %}
The API key is stored as a read-only `Config` property on `UConvaiSettings`. Manage it only through the Convai editor window — do not edit it manually in **Project Settings** or in config files.
{% endhint %}

After the key is accepted, the window opens to the Home section. The welcome flow does not appear again unless the stored key becomes invalid.

## View your account details

Select **Account** in the navigation sidebar to open the Account section. The following information is displayed:

| Field | Description |
|---|---|
| `UserName` | Your Convai account username |
| `Email` | The email address associated with your account |
| `PlanName` | Your current subscription plan |
| Interaction usage | Number of interactions consumed in the current period |
| ElevenLabs voice usage | ElevenLabs voice quota consumed |
| Core API usage | Core API calls consumed |
| Pixel Streaming usage | Pixel Streaming minutes consumed |
| Plan expiry date | Date on which your current plan period ends |
| Quota renewal date | Date on which usage quotas reset |

## Troubleshooting

### API key validation fails

**Symptom:** The window shows an error after you enter the API key and click **Validate & Continue**.

**Cause:** The key is invalid, expired, or the editor cannot reach Convai.

**Fix:** Copy the key again directly from the **API Keys** page on your Convai dashboard and re-enter it. Confirm that your internet connection is active and that no firewall is blocking outbound HTTPS.

**Verify:** After re-entering the key, the welcome flow advances past the API key step and the window opens to the Home section.

### Account section shows no usage data

**Symptom:** The Account section is blank or shows placeholder values.

**Cause:** The window has not yet refreshed data from Convai, or the stored key is no longer valid.

**Fix:** Close and reopen the window. If the welcome flow reappears, complete it again with a fresh API key.

**Verify:** The Account section populates with your `UserName`, `Email`, and plan details.

## Next steps

{% content-ref url="browse-samples-and-content.md" %}
[Browse samples and content](browse-samples-and-content.md)
{% endcontent-ref %}
