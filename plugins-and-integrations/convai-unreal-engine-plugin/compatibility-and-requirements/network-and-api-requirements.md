---
title: Network and API requirements
description: Reference for Convai Unreal Engine plugin connectivity requirements, including required domains, protocols, ports, and firewall rules for runtime operation.
last_reviewed: "4.0.0-beta.21"
---

The Convai Unreal Engine plugin requires internet connectivity during runtime. Speech processing, language understanding, and text-to-speech all execute through Convai — no offline or LAN mode is available.

## Required domains

| Domain                      | Protocol   | Purpose                               |
| --------------------------- | ---------- | ------------------------------------- |
| `live.convai.com`           | HTTPS, WSS | Room connection and real-time session |
| `api.convai.com`            | HTTPS      | Character metadata and REST API       |
| LiveKit TURN / STUN servers | UDP / TCP  | WebRTC audio and video transport      |

## Protocol stack

| Protocol               | Port     | Purpose                                                  |
| ---------------------- | -------- | -------------------------------------------------------- |
| HTTPS                  | 443      | REST API calls — room connection request, character data |
| WebSocket Secure (WSS) | 443      | LiveKit signaling — session setup and control messages   |
| WebRTC (UDP)           | Variable | Real-time audio, video, and data transport               |

{% hint style="info" %}
If UDP is blocked by your network, the connection automatically falls back to TURN relay using TCP on port 443. All traffic uses TLS encryption.
{% endhint %}

## Authentication

Every request to Convai is authenticated using your API key, sent as an `X-API-Key` header. The key is stored in **Project Settings > Plugins > Convai > API Key**. No per-session token exchange is required.

## Enterprise and firewall configuration

Minimum outbound rules required for plugin operation:

```text
ALLOW outbound TCP 443 → live.convai.com
ALLOW outbound TCP 443 → api.convai.com
ALLOW outbound UDP (any port) → any    ← WebRTC media
```

TCP 443 TURN fallback activates automatically if UDP is blocked. No inbound ports are required.

{% hint style="warning" %}
Proxy servers that perform TLS inspection (man-in-the-middle) may break the WebSocket connection. Exclude `live.convai.com` from TLS inspection if your environment uses it.
{% endhint %}

## Next steps

With network requirements confirmed, you are ready to install the plugin.

{% content-ref url="../getting-started/installation.md" %}
[Install the Convai Unreal Engine plugin](../getting-started/installation.md)
{% endcontent-ref %}
