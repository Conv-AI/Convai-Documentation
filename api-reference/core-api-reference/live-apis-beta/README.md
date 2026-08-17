---
description: >-
  Enable real-time, low-latency interaction with Convai AI characters through
  WebRTC-based Live APIs that support text, audio, and dynamic contextual
  communication.
---

# Live APIs (Beta)

{% hint style="danger" %}
Live APIs are available only on the Enterprise Plan.
{% endhint %}

Convai’s **Live APIs** enable real-time, dynamic interaction between users and AI characters through **WebRTC**.\
These APIs allow your applications to send and receive **audio**, **text**, and other contextual data, making conversations with AI characters seamless and responsive.

Once your characters are created, the Live APIs manage conversational input and contextual responses automatically, ensuring natural and consistent behavior across sessions.

#### **With the Live APIs, you can:**

* **Engage in live conversations** — Send user text or voice inputs and receive contextual, natural replies in real time.
* **Retrieve responses in text and/or audio form** — Power both text-based chat and voice dialogue experiences.
* **Use realtime models** — Integrate with low-latency models (currently Google Realtime; OpenAI support coming soon) for high-speed conversational performance.

The **Live APIs** act as the bridge between your AI characters and users, enabling smooth, two-way communication across both **text** and **voice** channels — all in real time.

***

#### Where to start

| Page | What it covers |
| ---- | -------------- |
| [Connect API](connect-api.md) | Opening a session and every option you can configure on it |
| [Use multi-character sessions](multi-character-sessions.md) | Creating a shared room with multiple character instances, routing turns, and updating the roster |
| [Turn lifecycle and message ordering](turn-lifecycle-and-message-ordering.md) | How a bot turn is delivered, which ordering you can rely on, and field presence rules |
| [Response contract and parsing](response-contract-and-parsing.md) | How speech, actions, and emotion are separated — and exactly what the server removes from the spoken response |
| [Message Glossary](message-glossary.md) | Every message type at a glance |
| [Client-to-server messages](client-to-server-messages.md) | Messages you send |
| [Server-to-client messages](server-to-client-messages.md) | Messages you receive |
| [Audio Data (via data channel)](audio-data-via-data-channel.md) | Custom audio handling |
| [Metrics](metrics.md) | Performance metrics and monitoring |

{% hint style="info" %}
If you are writing a client from scratch, read [Turn lifecycle and message ordering](turn-lifecycle-and-message-ordering.md) first. It explains the three envelope shapes on the data channel and the ordering guarantees, which together account for most integration issues.
{% endhint %}
