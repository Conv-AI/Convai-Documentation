# network and api requirements

The Convai Unity SDK requires an internet connection at runtime. All speech recognition, language understanding, and text-to-speech processing runs on Convai — no offline or LAN mode is available.

***

## Required Domains

Add these domains to any allowlist or firewall rules in your deployment environment.

| Domain                      | Protocol   | Purpose                               |
| --------------------------- | ---------- | ------------------------------------- |
| `live.convai.com`           | HTTPS, WSS | Room connection and real-time session |
| `api.convai.com`            | HTTPS      | Character metadata and REST API       |
| LiveKit TURN / STUN servers | UDP / TCP  | WebRTC audio and video transport      |

`live.convai.com` is the default server URL. It is configurable in `Edit > Project Settings > Convai SDK` via the **Server URL** field if you need to point to a different environment.

***

## Protocol Stack

The SDK uses three protocols in combination:

| Protocol               | Port     | Used for                                                 |
| ---------------------- | -------- | -------------------------------------------------------- |
| HTTPS                  | 443      | REST API calls — room connection request, character data |
| WebSocket Secure (WSS) | 443      | LiveKit signaling — session setup and control messages   |
| WebRTC (UDP)           | Variable | Real-time audio, video, and data transport               |

{% hint style="info" %}
If outbound UDP is blocked on your network, LiveKit automatically falls back to TURN relay over TCP on port 443. All traffic uses TLS encryption.
{% endhint %}

***

## Authentication

Every request to Convai is authenticated using your API key, sent as an `X-API-Key` header. The key is stored in `ConvaiSettings` and configured at `Edit > Project Settings > Convai SDK`. No per-session token exchange is required — the API key is sufficient for all SDK operations.

***

## Connection Timeout

The default connection timeout is **30 seconds**. This is configurable in `ConvaiSettings` between 5 and 120 seconds. If the room connection does not succeed within the timeout, the SDK fires `ConvaiManager.OnError` and `ConvaiRoomManager.OnSessionError` with the failure reason.

***

## Enterprise and Firewall Configuration

Training simulation deployments often run in managed networks with outbound filtering. Minimum rules required:

```
ALLOW outbound TCP 443 → live.convai.com
ALLOW outbound TCP 443 → api.convai.com
ALLOW outbound UDP (any port) → any    ← WebRTC media
```

If UDP is blocked entirely, TURN fallback over TCP 443 activates automatically. Voice quality may be slightly lower than direct UDP. No inbound ports are required.

{% hint style="warning" %}
Proxy servers that perform TLS inspection (man-in-the-middle) may break the WebSocket connection. If the SDK fails to connect behind a proxy, check whether TLS inspection is enabled for `live.convai.com` and exclude it if so.
{% endhint %}

***

## WebGL Deployments

WebGL builds have an additional browser-enforced requirement: **the page must be served over HTTPS or from `localhost`**. An HTTP deployment blocks microphone access regardless of SDK configuration — this is a browser security policy, not an SDK limitation.

***

## Next Steps

{% content-ref url="/broken/pages/fbaedc8762e52778e0d684b9927484e7ef96fb8e" %}
[Broken link](/broken/pages/fbaedc8762e52778e0d684b9927484e7ef96fb8e)
{% endcontent-ref %}
