---
description: >-
  Required domains, protocols, ports, and firewall rules for Convai Unity SDK
  runtime connectivity.
---

# Network and API Requirements

### Runtime Connectivity Requirements

The Convai Unity SDK requires internet connectivity during runtime. Speech processing, language understanding, and text-to-speech all execute through Convai — no offline or LAN mode is available.

### Required Domains

| Domain                      | Protocol   | Purpose                               |
| --------------------------- | ---------- | ------------------------------------- |
| `live.convai.com`           | HTTPS, WSS | Room connection and real-time session |
| `api.convai.com`            | HTTPS      | Character metadata and REST API       |
| LiveKit TURN / STUN servers | UDP / TCP  | WebRTC audio and video transport      |

The default server URL (`live.convai.com`) is configurable in **Edit > Project Settings > Convai SDK** via the **Server URL** field.

### Protocol Stack

| Protocol               | Port     | Used For                                                 |
| ---------------------- | -------- | -------------------------------------------------------- |
| HTTPS                  | 443      | REST API calls — room connection request, character data |
| WebSocket Secure (WSS) | 443      | LiveKit signaling — session setup and control messages   |
| WebRTC (UDP)           | Variable | Real-time audio, video, and data transport               |

{% hint style="info" %}
If UDP is blocked by your network, the SDK automatically falls back to TURN relay using TCP on port 443. All traffic uses TLS encryption.
{% endhint %}

### Authentication

Every request to Convai is authenticated using your API key, sent as an `X-API-Key` header. The key is stored in `ConvaiSettings` at **Edit > Project Settings > Convai SDK**. No per-session token exchange is required.

### Connection Timeout

The default connection timeout is **30 seconds**, configurable in `ConvaiSettings` between 5 and 120 seconds. When a connection attempt exceeds the timeout, the SDK raises `ConvaiManager.OnError` and `ConvaiRoomManager.OnSessionError`.

### Enterprise and Firewall Configuration

Minimum outbound rules required for SDK operation:

```
ALLOW outbound TCP 443 → live.convai.com
ALLOW outbound TCP 443 → api.convai.com
ALLOW outbound UDP (any port) → any    ← WebRTC media
```

TCP 443 TURN fallback activates automatically if UDP is blocked. No inbound ports are required.

{% hint style="warning" %}
Proxy servers that perform TLS inspection (man-in-the-middle) may break the WebSocket connection. Exclude `live.convai.com` from TLS inspection if your environment uses it.
{% endhint %}

### WebGL Deployments

WebGL builds must be served over HTTPS or from `localhost`. HTTP deployments block microphone access due to browser security policy — this is a browser constraint, not an SDK limitation. See [Platform Support Matrix](/broken/pages/17cdf00d4d51e730cf08a14faa6f6a7782f03510) for the full list of WebGL constraints.

### Next Steps

With network requirements confirmed, you are ready to install the SDK.

{% content-ref url="/broken/pages/9ea16d3f59b94ff8b5cf0fdc4f8971a84c7bc3a0" %}
[Broken link](/broken/pages/9ea16d3f59b94ff8b5cf0fdc4f8971a84c7bc3a0)
{% endcontent-ref %}
