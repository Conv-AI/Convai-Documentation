---
title: Network and API requirements
description: Reference for Convai Unreal Engine plugin connectivity requirements, including required domains, protocols, ports, and firewall rules for runtime operation.
last_reviewed: "4.0.0-beta.21"
---

The Convai Unreal Engine plugin requires internet connectivity during runtime. Runtime sessions connect to Convai through the realtime endpoint, while editor and HTTPS API requests use the API endpoint.

## Required domains

| Domain | Protocol | Purpose |
| --- | --- | --- |
| `realtime-api.convai.com` | HTTPS | Realtime session connection endpoint |
| `api.convai.com` | HTTPS | Character data, account, and HTTPS API requests |

## Protocol stack

| Protocol | Port | Purpose |
| --- | --- | --- |
| HTTPS | 443 | Realtime connection setup and HTTPS API calls |
| Convai WebRTC client | Managed by the plugin | Runtime audio, video, and data transport after the session is connected |

{% hint style="info" %}
The public Unreal source exposes the realtime endpoint as `https://realtime-api.convai.com/connect`. It does not expose separate LiveKit, TURN, STUN, WSS, or UDP port settings.
{% endhint %}

## Authentication

HTTPS API requests use the configured API key as a `CONVAI-API-KEY` header. Realtime session setup starts from the same configured API key, but the subsystem maps that header to `X-API-KEY` before passing it to the Convai WebRTC client. The key is stored on `UConvaiSettings.API_Key` and is visible in **Project Settings > Plugins > Convai > API Key**.

## Enterprise and firewall configuration

Minimum outbound rules visible in the public Unreal source:

```text
ALLOW outbound TCP 443 → realtime-api.convai.com
ALLOW outbound TCP 443 → api.convai.com
```

The Unreal plugin source does not expose additional TURN, STUN, WSS, or UDP firewall targets.

{% hint style="warning" %}
Proxy servers that block or inspect HTTPS traffic may prevent session setup or HTTPS API requests. Allow outbound HTTPS traffic to both required domains before testing in Play In Editor.
{% endhint %}

## Next steps

With network requirements confirmed, you are ready to install the plugin.

{% content-ref url="../getting-started/install-the-convai-plugin.md" %}
[Install the Convai Unreal Engine plugin](../getting-started/install-the-convai-plugin.md)
{% endcontent-ref %}
