---
title: Prerequisites
description: Verify engine version, account, platform, and network requirements before installing the Convai Unreal Engine plugin into your project.
last_reviewed: "4.0.0-beta.21"
---

Verify each requirement before you install the Convai Unreal Engine plugin. Missing any one of these will prevent the plugin from loading or running correctly.

## Unreal Engine version

The plugin supports Unreal Engine 5.0 and later — every UE 5.x release. The minimum supported version is <code class="expression">space.vars.unreal_min_version</code>.

The **Convai editor window** — the in-editor panel used for API key sign-in — requires **UE 5.2 or later**. On UE 5.0 and 5.1, all runtime gameplay features work, but the editor sign-in panel is not available. Add your API key to `Config/DefaultEngine.ini` instead — see [Configure your API key](configure-your-api-key.md).

| UE version range | Plugin support | API key setup |
|---|---|---|
| 5.0–5.1 | Supported | Add the key to `Config/DefaultEngine.ini` (Project Settings shows the value read-only) |
| 5.2 and later | Supported | Sign in through the Convai editor window (opens automatically after plugin enable) |

{% hint style="warning" %}
On Unreal Engine 5.0 and 5.1, the Convai editor window is not loaded. Add your API key to `Config/DefaultEngine.ini` — the **API Key** field in Project Settings is read-only on those engine versions.
{% endhint %}

## Convai account and API key

You need a Convai account to authenticate the plugin and to create or manage characters.

{% stepper %}
{% step %}
### Create a Convai account

Go to [convai.com](https://convai.com) and create a free account if you do not have one.
{% endstep %}

{% step %}
### Sign in to the dashboard

Sign in and open your account dashboard. Your API key is available under account settings.
{% endstep %}

{% step %}
### Copy your API key

Copy the API key string. You will enter it after installation — through the Convai editor window on UE 5.2+, or in `Config/DefaultEngine.ini` on UE 5.0 and 5.1. See [Configure your API key](configure-your-api-key.md).
{% endstep %}
{% endstepper %}

## Engine plugins (bundled dependencies)

The Convai Unreal Engine plugin depends on two engine plugins that ship with Unreal Engine. Both are enabled automatically when you enable the Convai plugin:

| Dependency | Purpose |
|---|---|
| `AudioCapture` | Provides microphone input on Win64 and Android. |
| `AndroidPermission` | Handles runtime microphone permission requests on Android. |

You do not need to enable these manually. If your project has previously disabled either plugin, re-enable it under **Edit > Plugins** before enabling the Convai plugin.

## Supported platforms

| Platform | Supported |
|---|---|
| Win64 | Yes |
| Android | Yes |
| Other | No |

Mac, iOS, Linux, and console targets are not supported in this release.

## Network access

The plugin connects to Convai at runtime over WebRTC. Ensure the device running your project can reach Convai's endpoints on HTTPS and WebRTC ports. Firewalls or proxies that block WebRTC will prevent conversations from starting.

{% hint style="success" %}
When all requirements are met, you are ready to install the plugin.
{% endhint %}

## Next steps

{% content-ref url="install-the-convai-plugin.md" %}
[Install the Convai plugin](install-the-convai-plugin.md)
{% endcontent-ref %}
