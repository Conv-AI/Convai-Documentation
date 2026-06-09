---
title: Prerequisites
description: Verify engine version, account, platform, and network requirements before installing the Convai Unreal Engine plugin into your project.
last_reviewed: "4.0.0-beta.21"
---

Verify each requirement before you install the Convai Unreal Engine plugin. Missing any one of these will prevent the plugin from loading or running correctly.

## Unreal Engine version

The plugin supports Unreal Engine 5.0 and later — every UE 5.x release. The minimum supported version is <code class="expression">space.vars.unreal_min_version</code>.

The **Convai editor window** — the in-editor panel used for API key sign-in — requires **UE 5.2 or later**. On UE 5.0 and 5.1, all runtime gameplay features work, but the editor sign-in panel is not available. Set your API key with the **Set API Key** Blueprint node (`UConvaiUtils::SetAPI_Key`, category **Convai > Settings**) instead — see [Configure your API key](configure-api-key.md).

| UE version range | Plugin support | Convai editor window |
|---|---|---|
| 5.0–5.1 | Supported | Not available. Use **Set API Key** (`UConvaiUtils::SetAPI_Key`) or add the key to `Config/DefaultEngine.ini`. |
| 5.2 and later | Supported | Available via the toolbar **Convai Editor** button and **Window** menu (**Convai** section > **Open Convai Editor**). |

{% hint style="warning" %}
On Unreal Engine 5.0 and 5.1, the Convai editor window and its Project Settings customization are not loaded. `UConvaiSettings.API_Key` is read-only in the default Project Settings UI — use **Set API Key** or `DefaultEngine.ini` instead.
{% endhint %}

## Convai account and API key

You need a Convai account to authenticate the plugin and to create or manage characters.

1. Go to [convai.com](https://convai.com) and create a free account if you do not have one.
2. After signing in, your API key is available on the dashboard. You will enter it through the Convai editor window after installation — see [Configure your API key](configure-api-key.md).

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

{% content-ref url="installation.md" %}
[Install the Convai plugin](installation.md)
{% endcontent-ref %}
