---
title: Prerequisites
description: Reference for what you need before installing the Convai Unreal Engine plugin, including engine version, account, and dependencies.
last_reviewed: "4.0.0-beta.21"
---

Verify each requirement before you install the Convai Unreal Engine plugin. Missing any one of these will prevent the plugin from loading or running correctly.

## Unreal Engine version

The plugin requires Unreal Engine <code class="expression">space.vars.unreal_min_version</code> or later. All UE 5.x releases are supported.

## Convai account and API key

You need a Convai account to authenticate the plugin and to create or manage characters.

1. Go to <code class="expression">space.vars.dashboard_url</code> and create a free account if you do not have one.
2. After signing in, your API key is available on the dashboard. You will enter it through the Convai editor window after installation — see [Configure your API key](configure-api-key.md).

## Engine plugins (bundled dependencies)

The Convai Unreal Engine plugin depends on two engine plugins that are bundled with Unreal Engine. Both are enabled automatically when you enable the Convai plugin:

| Dependency | Purpose |
|---|---|
| `AudioCapture` | Provides microphone input on Win64 and Android. |
| `AndroidPermission` | Handles runtime microphone permission requests on Android. |

You do not need to enable these manually. If your project has previously disabled them, re-enable them under **Edit > Plugins** before enabling the Convai plugin.

## Supported platforms

| Platform | Supported |
|---|---|
| Win64 | Yes |
| Android | Yes |
| Other | No |

Mac, iOS, Linux, and console targets are not in the `PlatformAllowList` in `ConvAI.uplugin` and are not supported by this plugin version.

## Network access

The plugin connects to Convai at runtime over WebRTC. Ensure the device running your project can reach Convai's endpoints on HTTPS and WebRTC ports. Firewalls or proxies that block WebRTC will prevent conversations from starting.

## Next steps

Once you have verified all requirements, proceed to [Install the Convai plugin](installation.md).
