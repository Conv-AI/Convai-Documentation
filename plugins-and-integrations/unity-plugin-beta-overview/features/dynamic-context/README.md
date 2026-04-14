---
description: >-
  Learn how Dynamic Context enables more relevant, adaptive, and context-aware
  AI character interactions.
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
IConvaiRoomConnectionService.UpdateDynamicContext(text, mode, runLlm)
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

### `text`

The content you want the character to be aware of. This is a plain string — it can be a sentence, a structured paragraph, or key-value data formatted however you prefer.

```
"The player's name is Aria. She is level 12 and currently on the quest 'Lost in the Fog'."
```

`text` is **required** for `append` and `replace` modes. When using `reset` mode, it is ignored.

***

### `mode`

Controls how the new text is applied to the character's existing ephemeral context.

| Mode      | Behavior                                                                                                                                           | When to Use                                                                         |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `append`  | Adds `text` to any existing ephemeral context. Prior entries remain.                                                                               | Progressive information — adding facts as the session unfolds.                      |
| `replace` | Discards all current ephemeral context and replaces it entirely with the new `text`.                                                               | A clean state transition — entering a new scene, starting a new chapter.            |
| `reset`   | Clears all runtime ephemeral context. `text` is ignored. Initial Dynamic Info is not affected — it remains pinned for the duration of the session. | Resetting accumulated runtime context while preserving session-level fixed context. |

**Default:** `"append"`

***

### `runLlm`

Whether to trigger an LLM inference pass after the context update.

| Value   | Behavior                                                                                 |
| ------- | ---------------------------------------------------------------------------------------- |
| `auto`  | The server decides based on its internal pipeline state. Recommended for most use cases. |
| `true`  | Always triggers an LLM response immediately after the context update.                    |
| `false` | Updates the context silently — no LLM response is triggered.                             |

**Default:** `"auto"`

Use `"false"` when you are batching multiple context updates and only want the LLM to respond after the final one. Use `"true"` when the context update itself should prompt a reaction from the character.

***

#### `mode`

Controls how the new text is applied to the character's existing ephemeral context.

| Mode      | Behavior                                                                                                                                                   | When to Use                                                                         |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `append`  | Adds `text` to any existing ephemeral context. Prior entries remain.                                                                                       | Progressive information — adding facts as the session unfolds.                      |
| `replace` | Discards all current ephemeral context and replaces it entirely with the new `text`.                                                                       | A clean state transition — entering a new scene, starting a new chapter.            |
| `reset`   | Clears all **runtime** ephemeral context. `text` is ignored. **Initial Dynamic Info is not affected** — it remains pinned for the duration of the session. | Resetting accumulated runtime context while preserving session-level fixed context. |

Default: `"append"`

***

## Initial Dynamic Info

`UpdateDynamicContext` is not the only way to provide session-level context to a character. The `ConvaiCharacter` component exposes a second layer that is fixed for the entire session: **Initial Dynamic Info**.

This is configured in the Unity Inspector on the `ConvaiCharacter` component, under the **SESSION** section:

1. Enable **Keep Initial Dynamic Info In Context** — this toggle controls whether the text below is included in the connection request and pinned by the server for the whole session.
2. Once enabled, the **Dynamic Info (Connection Request)** field appears. Enter your initial context text in **Initial Dynamic Info Text**.

<figure><img src="../../../../.gitbook/assets/image (459).png" alt=""><figcaption></figcaption></figure>

Unlike `UpdateDynamicContext`, this value is not sent over the data channel at runtime — it is embedded in the connection payload before the session starts.

**Key distinction:** `reset` mode in `UpdateDynamicContext` does **not** clear Initial Dynamic Info. It only resets the runtime ephemeral layer. The pinned initial text remains active for the entire session regardless of any context updates you send.

#### When to use each

|                        | Initial Dynamic Info                                                             | Runtime Dynamic Context                        |
| ---------------------- | -------------------------------------------------------------------------------- | ---------------------------------------------- |
| **Set via**            | Unity Inspector (`ConvaiCharacter`)                                              | Code (`UpdateDynamicContext`)                  |
| **When sent**          | At room connection, before session starts                                        | Any time during an active session              |
| **Mutable**            | No — fixed for the session                                                       | Yes — append, replace, or reset at will        |
| **Cleared by `reset`** | No                                                                               | Yes                                            |
| **Use for**            | Stable session configuration: character role, scenario rules, fixed instructions | Changing game state, player data, events, mood |

{% hint style="info" %}
Use Initial Dynamic Info for context that should never change during a session — role instructions, scenario setup, fixed rules. Use `UpdateDynamicContext` for everything that evolves as the session progresses.
{% endhint %}

***

## Accessing the API

Dynamic Context is exposed through `IConvaiRoomConnectionService`, obtained via `ConvaiManager`. Two distinct patterns exist depending on who owns the connection lifecycle.

### Pattern A — Self-Contained

Use when the component is responsible for its own initialization. Typical for session-start scenarios where context must be sent as soon as the connection is ready.

```csharp
using System.Collections;
using Convai.Runtime.Components;
using Convai.Runtime.Room;
using UnityEngine;

public class ExampleSelfContained : MonoBehaviour
{
    private IConvaiRoomConnectionService _connectionService;

    private IEnumerator Start()
    {
        // Poll until ConvaiManager and the room service are available.
        // Resolves within one or two frames under normal conditions.
        while (true)
        {
            ConvaiManager manager = ConvaiManager.ActiveManager;
            if (manager != null && manager.TryGetRoomConnectionService(out _connectionService))
                break;
            yield return null;
        }

        // The service reference is available, but the room may not be connected yet.
        // Check IsConnected first: if this component initializes after the session is
        // already established, the Connected event will never fire.
        if (_connectionService.IsConnected)
            OnReady();
        else
            _connectionService.Connected += OnConnected;
    }

    private void OnConnected()
    {
        _connectionService.Connected -= OnConnected;
        OnReady();
    }

    private void OnReady()
    {
        bool sent = _connectionService.UpdateDynamicContext("...", mode: "replace", runLlm: "false");
        if (!sent)
            Debug.LogWarning("[Example] UpdateDynamicContext returned false.");
    }

    private void OnDestroy()
    {
        // Prevent a dangling subscription if this object is destroyed before connection.
        if (_connectionService != null)
            _connectionService.Connected -= OnConnected;
    }
}
```

***

### Pattern B — Inject

Use when a session coordinator or parent system is responsible for providing a connected service. The component assumes the service is valid when its public methods are called.

```csharp
using Convai.Runtime.Room;
using UnityEngine;

public class ExampleInjected : MonoBehaviour
{
    private IConvaiRoomConnectionService _connectionService;

    /// <summary>
    /// Initializes this component with an active room connection service.
    /// Must be called by the session owner after the Convai session is established.
    /// </summary>
    public void Initialize(IConvaiRoomConnectionService connectionService)
    {
        _connectionService = connectionService;
    }

    public void DoSomething()
    {
        // ?. guards against Initialize not having been called yet.
        bool sent = _connectionService?.UpdateDynamicContext("...", mode: "append", runLlm: "false") ?? false;
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

| Parameter | Type     | Required           | Default    | Description                                                        |
| --------- | -------- | ------------------ | ---------- | ------------------------------------------------------------------ |
| `text`    | `string` | Yes (unless reset) | —          | The context text to inject.                                        |
| `mode`    | `string` | No                 | `"append"` | How to apply the text: `"append"`, `"replace"`, or `"reset"`.      |
| `runLlm`  | `string` | No                 | `"auto"`   | Whether to trigger an LLM response: `"true"`, `"false"`, `"auto"`. |

**Returns:** `true` if the message was dispatched to the transport layer; `false` if the session is not connected.

***

#### `mode`

Controls how the new text is applied to the character's existing ephemeral context.

| Mode      | Behavior                                                                                                                                                   | When to Use                                                                         |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `append`  | Adds `text` to any existing ephemeral context. Prior entries remain.                                                                                       | Progressive information — adding facts as the session unfolds.                      |
| `replace` | Discards all current ephemeral context and replaces it entirely with the new `text`.                                                                       | A clean state transition — entering a new scene, starting a new chapter.            |
| `reset`   | Clears all **runtime** ephemeral context. `text` is ignored. **Initial Dynamic Info is not affected** — it remains pinned for the duration of the session. | Resetting accumulated runtime context while preserving session-level fixed context. |

**Default:** `"append"`

***

## Dynamic Context vs. Related Features

<table><thead><tr><th>Feature</th><th width="216.407470703125">Method</th><th width="127.9259033203125">Scope</th><th width="107.370361328125">Persists Across Sessions</th><th>Use For</th></tr></thead><tbody><tr><td><strong>Dynamic Context</strong></td><td><code>UpdateDynamicContext</code></td><td>Ephemeral (runtime)</td><td>No</td><td>Runtime facts: player state, game events, situational awareness.</td></tr><tr><td><strong>Initial Dynamic Info</strong></td><td><code>ConvaiCharacter</code> Inspector</td><td>Ephemeral (session-start, pinned)</td><td>No</td><td>Fixed session instructions: scenario rules, character role, stable setup. Not affected by <code>reset</code>.</td></tr><tr><td><strong>Dynamic Info</strong></td><td><code>SendDynamicInfo</code></td><td>Per-message</td><td>No</td><td>Inline context attached to a specific user utterance.</td></tr><tr><td><strong>Template Keys</strong></td><td><code>UpdateTemplateKeys</code></td><td>Session</td><td>No</td><td>Resolving named placeholders (<code>{PlayerName}</code>) in narrative design text.</td></tr><tr><td><strong>Scene Metadata</strong></td><td><code>UpdateSceneMetadata</code></td><td>Session</td><td>No</td><td>Structural scene data for the backend's contextual grounding pipeline.</td></tr><tr><td><strong>Dashboard Backstory</strong></td><td>Convai dashboard</td><td>Permanent</td><td>Yes</td><td>Character personality, lore, fixed behavioral rules.</td></tr></tbody></table>

***

## Common Pitfalls

* **Calling before the session is connected** `UpdateDynamicContext` returns `false` and silently drops the update. Use a coroutine or subscribe to `IConvaiRoomConnectionService.Connected` to delay context injection until the session is live.
* **Using `append` indefinitely** Every `append` expands the context window. In long sessions this degrades response coherence and increases latency. Use `replace` periodically, or adopt the `DynamicContextManager` pattern.
* **Sending `text` with `reset` mode** `text` is ignored when `mode` is `"reset"`. Pass `null` explicitly to make the intent clear.
* **Expecting a synchronous effect** Dynamic Context is asynchronous end-to-end. The character will not know about the update until the next LLM inference pass. Do not design logic that assumes an instant effect.
* **Overusing `runLlm: "true"`** Forcing an immediate response on every update creates conversational noise. Reserve it for moments where a character reaction is genuinely expected.

***

## Quick Reference

```csharp
// Append new information to existing ephemeral context (default)
connectionService.UpdateDynamicContext("Player just entered the dungeon.");

// Replace all ephemeral context with new content
connectionService.UpdateDynamicContext("Player is now in Act 2.", mode: "replace");

// Clear all ephemeral context
connectionService.UpdateDynamicContext(null, mode: "reset");

// Accumulate silently (no LLM response)
connectionService.UpdateDynamicContext("Player picked up the golden key.", runLlm: "false");

// Update and trigger an immediate character response
connectionService.UpdateDynamicContext("The village is on fire!", runLlm: "true");

// Inject emotional state
connectionService.UpdateDynamicContext("Speak with urgency. A threat is approaching.", mode: "replace", runLlm: "false");
```

***

## Conclusion

Dynamic Context is the bridge between your game or application's live state and your AI character's understanding of it. The character's permanent configuration — personality, backstory, behavioral rules — stays stable in the Convai dashboard. Everything that belongs to this session, this user, and this moment flows through `UpdateDynamicContext`.

The API is intentionally simple: a single method with three parameters. The sophistication lives in how you use it — whether that is personalizing a conversation at session start, reacting to a threshold crossing mid-session, silently accumulating events until they are worth commenting on, or tracking competency gaps across an entire training session.

A few principles to carry forward:

* **Silent updates are the default posture.** Use `runLlm: "false"` for state synchronization. Reserve `runLlm: "true"` for moments that genuinely warrant a character response.
* **Treat the context window as a resource.** Unbounded `append` degrades quality over time. Use `replace` at natural boundaries — scene transitions, module changes, session resets.
* **Your application owns the state. The character receives it.** Dynamic Context is the mechanism that enforces that separation cleanly.

{% include "../../../../.gitbook/includes/need-help-for-questions-p....md" %}
