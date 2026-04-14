---
description: >-
  Learn how Dynamic Context enables more relevant, adaptive, and context-aware
  AI character interactions.
hidden: true
---

# Dynamic Context

## Introduction

Convai characters have two layers of context:

* **Character Level** — backstory, personality, and behavioral rules. Configured in the Convai dashboard, persists across all sessions.
* **Session Level** — information relevant only to the current interaction: who the player is, what just happened, the current game state.

Dynamic Context is a runtime feature of the Convai Unity SDK that lets your game push ephemeral, session-specific information to a Convai AI character during an active conversation. Unlike a character's fixed backstory configured in the Convai dashboard, Dynamic Context is injected at runtime and is temporary — it exists only for the duration of the current session.

Use it to bridge the gap between your game world and the AI: tell the character what just happened, who the player is, what they're carrying, where they are, or anything else that should influence the character's responses without being hardcoded into a prompt.

***

## How It Works

When you call `UpdateDynamicContext`, the SDK serializes a `context-update` message and delivers it to the Convai backend over the active session's data channel. The backend receives the update and folds the new information into the character's active context window before processing the next user utterance.

The flow is:

```
Your Game Code
      │
      ▼
ConvaiRoomManager.UpdateDynamicContext(text, mode, runLlm)
      │
      ▼
Serialized context-update message dispatched over the session data channel
      │
      ▼
Convai Backend → LLM Context Window
```

This is a **fire-and-forget, outbound-only** operation. There is no direct response to the context update itself — the effect is visible in the character's next spoken reply.

***

## Key Concepts

Before writing any code, understand these three parameters that control every `UpdateDynamicContext` call.

#### `text`

The content you want the character to be aware of. This is a plain string — it can be a sentence, a structured paragraph, or key-value data formatted however you prefer.

```
"The player's name is Aria. She is level 12 and currently on the quest 'Lost in the Fog'."
```

`text` is **required** for `append` and `replace` modes. When using `reset` mode, it is ignored.

***

#### `mode`

Controls how the new text is applied to the character's existing ephemeral context.

| Mode      | Behavior                                                                             | When to Use                                                              |
| --------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------ |
| `append`  | Adds `text` to any existing ephemeral context. Prior entries remain.                 | Progressive information — adding facts as the session unfolds.           |
| `replace` | Discards all current ephemeral context and replaces it entirely with the new `text`. | A clean state transition — entering a new scene, starting a new chapter. |
| `reset`   | Clears all runtime ephemeral context. `text` is ignored.                             | Resetting all accumulated runtime context.                               |

**Default:** `"append"`

***

#### `runLlm`

Whether to trigger an LLM inference pass after the context update.

| Value   | Behavior                                                                                 |
| ------- | ---------------------------------------------------------------------------------------- |
| `auto`  | The server decides based on its internal pipeline state. Recommended for most use cases. |
| `true`  | Always triggers an LLM response immediately after the context update.                    |
| `false` | Updates the context silently — no LLM response is triggered.                             |

**Default:** `"auto"`

Use `"false"` when you are batching multiple context updates and only want the LLM to respond after the final one. Use `"true"` when the context update itself should prompt a reaction from the character.

***

## Accessing the API

Dynamic Context is exposed through `ConvaiRoomManager`, the central session manager for the Convai Unity SDK. It is accessible as a persistent singleton via `ConvaiRoomManager.Instance`.

Two distinct patterns exist depending on who owns the connection lifecycle.

### Pattern A — Self-Contained

Use when the component is responsible for its own initialization.

The required readiness level depends on `runLlm`:

* **`runLlm: "false"` or `"auto"`** — waiting for `IsConnectedToRoom` is sufficient. The context is injected silently and no immediate audio response is expected.
* **`runLlm: "true"`** — the full audio pipeline must be ready before sending. See the note below.

```csharp
using System.Collections;
using Convai.Scripts;
using UnityEngine;

public class ExampleSelfContained : MonoBehaviour
{
    private ConvaiRoomManager _roomManager;

    private IEnumerator Start()
    {
        // Poll until ConvaiRoomManager singleton is available.
        // Resolves within one or two frames under normal conditions.
        while (ConvaiRoomManager.Instance == null)
            yield return null;

        _roomManager = ConvaiRoomManager.Instance;

        // Wait for the room connection to be established.
        // Check IsConnectedToRoom first: if this component initializes after the session is
        // already established, OnRoomConnectionSuccessful will never fire.
        if (!_roomManager.IsConnectedToRoom)
        {
            bool connected = false;
            _roomManager.OnRoomConnectionSuccessful.AddListener(() => connected = true);
            yield return new WaitUntil(() => connected);
        }

        OnReady();
    }

    private void OnReady()
    {
        bool sent = _roomManager.UpdateDynamicContext("...", mode: "replace", runLlm: "false");
        if (!sent)
            Debug.LogWarning("[Example] UpdateDynamicContext returned false.");
    }

    private void OnDestroy()
    {
        if (_roomManager != null)
            _roomManager.OnRoomConnectionSuccessful.RemoveListener(OnConnected);
    }

    private void OnConnected() { }
}
```

{% hint style="warning" %}
**If you use `runLlm: "true"` to trigger an immediate character response**, waiting for `IsConnectedToRoom` is not enough. The character's audio pipeline goes through three asynchronous stages after the room connects: the bot participant joins, the audio track is subscribed, and the audio buffer is initialised. Sending before all three are complete causes the server's TTS response to be silently dropped.

Use the pattern below instead:

```csharp
using System.Collections;
using System.Linq;
using Convai.Scripts;
using UnityEngine;

public class ExampleImmediateGreeting : MonoBehaviour
{
    private ConvaiRoomManager _roomManager;

    private IEnumerator Start()
    {
        while (ConvaiRoomManager.Instance == null)
            yield return null;

        _roomManager = ConvaiRoomManager.Instance;

        while (!_roomManager.IsConnectedToRoom)
            yield return null;

        // Wait until the bot's audio pipeline is fully ready:
        //   1. Bot participant has joined the room      (ParticipantConnected)
        //   2. Bot audio track has been published       (TrackPublished)
        //   3. Audio track has been subscribed          (TrackSubscribed)
        //   4. AudioSource.Play() has been called       (AudioStream constructor)
        while (_roomManager.NpcToParticipantMap == null ||
               !_roomManager.NpcToParticipantMap.Values.Any(d => d.AudioStream != null))
        {
            yield return null;
        }

        bool sent = _roomManager.UpdateDynamicContext("...", mode: "replace", runLlm: "true");
        if (!sent)
            Debug.LogWarning("[Example] UpdateDynamicContext returned false.");
    }
}
```
{% endhint %}

***

### Pattern B — Inject

Use when a session coordinator or parent system is responsible for providing the room manager. The component assumes the manager is valid when its public methods are called.

```csharp
using Convai.Scripts;
using UnityEngine;

public class ExampleInjected : MonoBehaviour
{
    private ConvaiRoomManager _roomManager;

    /// <summary>
    /// Initializes this component with the active room manager.
    /// Must be called by the session owner after the Convai session is established.
    /// </summary>
    public void Initialize(ConvaiRoomManager roomManager)
    {
        _roomManager = roomManager;
    }

    public void DoSomething()
    {
        // ?. guards against Initialize not having been called yet.
        bool sent = _roomManager?.UpdateDynamicContext("...", mode: "append", runLlm: "false") ?? false;
        if (!sent)
            Debug.LogWarning("[Example] UpdateDynamicContext returned false.");
    }
}
```

{% hint style="info" %}
`UpdateDynamicContext` returns `false` if the session is not connected. Always check the return value.
{% endhint %}

***

## API Reference

```csharp
bool UpdateDynamicContext(string text, string mode = "append", string runLlm = "auto");
```

Available on `ConvaiRoomManager`. Also callable via `ConvaiNPC.UpdateDynamicContext(...)`, which delegates to `ConvaiRoomManager.Instance` internally.

| Parameter | Type     | Required           | Default    | Description                                                        |
| --------- | -------- | ------------------ | ---------- | ------------------------------------------------------------------ |
| `text`    | `string` | Yes (unless reset) | —          | The context text to inject.                                        |
| `mode`    | `string` | No                 | `"append"` | How to apply the text: `"append"`, `"replace"`, or `"reset"`.      |
| `runLlm`  | `string` | No                 | `"auto"`   | Whether to trigger an LLM response: `"true"`, `"false"`, `"auto"`. |

**Returns:** `true` if the message was dispatched to the transport layer; `false` if the session is not connected (RTVIHandler not initialized) or if `text` is empty and `mode` is not `"reset"`.

***

#### **`mode`**

Controls how the new text is applied to the character's existing ephemeral context.

| Mode      | Behavior                                                                             | When to Use                                                              |
| --------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------ |
| `append`  | Adds `text` to any existing ephemeral context. Prior entries remain.                 | Progressive information — adding facts as the session unfolds.           |
| `replace` | Discards all current ephemeral context and replaces it entirely with the new `text`. | A clean state transition — entering a new scene, starting a new chapter. |
| `reset`   | Clears all runtime ephemeral context. `text` is ignored.                             | Resetting all accumulated runtime context.                               |

**Default:** `"append"`

***

## Common Pitfalls

* **Calling before the session is connected** `UpdateDynamicContext` returns `false` and silently drops the update. Use a coroutine or subscribe to `ConvaiRoomManager.OnRoomConnectionSuccessful` (a `UnityEvent`) to delay context injection until the session is live.
* **Using `append` indefinitely** Every `append` expands the context window. In long sessions this degrades response coherence and increases latency. Use `replace` periodically, or adopt the `DynamicContextManager` pattern.
* **Sending `text` with `reset` mode** `text` is ignored when `mode` is `"reset"`. Pass `null` explicitly to make the intent clear.
* **Expecting a synchronous effect** Dynamic Context is asynchronous end-to-end. The character will not know about the update until the next LLM inference pass. Do not design logic that assumes an instant effect.
* **Overusing `runLlm: "true"`** Forcing an immediate response on every update creates conversational noise. Reserve it for moments where a character reaction is genuinely expected.

***

### Quick Reference

```csharp
ConvaiRoomManager room = ConvaiRoomManager.Instance;

// Append new information to existing ephemeral context (default)
room.UpdateDynamicContext("Player just entered the dungeon.");

// Replace all ephemeral context with new content
room.UpdateDynamicContext("Player is now in Act 2.", mode: "replace");

// Clear all ephemeral context
room.UpdateDynamicContext(null, mode: "reset");

// Accumulate silently (no LLM response)
room.UpdateDynamicContext("Player picked up the golden key.", runLlm: "false");

// Update and trigger an immediate character response
room.UpdateDynamicContext("The village is on fire!", runLlm: "true");

// Inject emotional state
room.UpdateDynamicContext("Speak with urgency. A threat is approaching.", mode: "replace", runLlm: "false");
```

***

## Conclusion

Dynamic Context is the bridge between your game or application's live state and your AI character's understanding of it. The character's permanent configuration — personality, backstory, behavioral rules — stays stable in the Convai dashboard. Everything that belongs to this session, this user, and this moment flows through `UpdateDynamicContext`.

The API is intentionally simple: a single method with three parameters. The sophistication lives in how you use it — whether that is personalizing a conversation at session start, reacting to a threshold crossing mid-session, silently accumulating events until they are worth commenting on, or tracking competency gaps across an entire training session.

A few principles to carry forward:

* **Silent updates are the default posture.** Use `runLlm: "false"` for state synchronization. Reserve `runLlm: "true"` for moments that genuinely warrant a character response.
* **Treat the context window as a resource.** Unbounded `append` degrades quality over time. Use `replace` at natural boundaries — scene transitions, module changes, session resets.
* **Your application owns the state. The character receives it.** Dynamic Context is the mechanism that enforces that separation cleanly.

{% hint style="info" %}
**Need help?** For questions, please visit the [**Convai Developer Forum**](https://forum.convai.com/).
{% endhint %}
