---
title: Network and API requirements
description: Reference for Convai Unity SDK connectivity requirements, including required domains, protocols, ports, and firewall rules for runtime operation.
last_reviewed: "4.2.0"
---

The Convai Unity SDK requires internet connectivity during runtime. Speech processing, language understanding, and text-to-speech all execute through Convai — no offline or LAN mode is available.

## Required domains

| Domain                      | Protocol   | Purpose                               |
| --------------------------- | ---------- | ------------------------------------- |
| `live.convai.com`           | HTTPS, WSS | Room connection and real-time session |
| `api.convai.com`            | HTTPS      | Character metadata and REST API       |
| LiveKit TURN / STUN servers | UDP / TCP  | WebRTC audio and video transport      |

The default server URL (`live.convai.com`) is configurable in **Edit > Project Settings > Convai SDK** via the **Server URL** field.

## Protocol stack

| Protocol               | Port     | Used For                                                 |
| ---------------------- | -------- | -------------------------------------------------------- |
| HTTPS                  | 443      | REST API calls — room connection request, character data |
| WebSocket Secure (WSS) | 443      | LiveKit signaling — session setup and control messages   |
| WebRTC (UDP)           | Variable | Real-time audio, video, and data transport               |

{% hint style="info" %}
If UDP is blocked by your network, the SDK automatically falls back to TURN relay using TCP on port 443. All traffic uses TLS encryption.
{% endhint %}

## Authentication

Every request to Convai is authenticated using your API key, sent as an `X-API-Key` header. The key is stored in `ConvaiSettings` at **Edit > Project Settings > Convai SDK**. No per-session token exchange is required.

## Connection timeout

The default connection timeout is **30 seconds**, configurable in `ConvaiSettings` between 5 and 120 seconds. When a connection attempt exceeds the timeout, the SDK raises `ConvaiManager.OnError` and `ConvaiRoomManager.OnSessionError`.

## Enterprise and firewall configuration

Minimum outbound rules required for SDK operation:

```text
ALLOW outbound TCP 443 → live.convai.com
ALLOW outbound TCP 443 → api.convai.com
ALLOW outbound UDP (any port) → any    ← WebRTC media
```

TCP 443 TURN fallback activates automatically if UDP is blocked. No inbound ports are required.

{% hint style="warning" %}
Proxy servers that perform TLS inspection (man-in-the-middle) may break the WebSocket connection. Exclude `live.convai.com` from TLS inspection if your environment uses it.
{% endhint %}

## WebGL deployments

WebGL builds must be served over HTTPS or from `localhost`. HTTP deployments block microphone access due to browser security policy — this is a browser constraint, not an SDK limitation. See [Platform support matrix](platform-support-matrix.md) for the full list of WebGL constraints.

## Next steps

With network requirements confirmed, you are ready to install the SDK.

{% content-ref url="../getting-started/installation.md" %}
[Install the Convai Unity SDK](../getting-started/installation.md)
{% endcontent-ref %}
