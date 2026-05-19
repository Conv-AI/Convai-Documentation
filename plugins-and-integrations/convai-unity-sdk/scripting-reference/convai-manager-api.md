# convai manager api

`ConvaiManager` is the primary scripting entry point for the Convai Unity SDK. It bootstraps the runtime, manages room connections, owns the `Events`, `Audio`, and `Transcripts` facades, and provides access to lower-level services through typed accessors. Every scripted interaction with the SDK starts here.

**Access:** `ConvaiManager.ActiveManager` (singleton)

```csharp
var manager = ConvaiManager.ActiveManager;
if (manager == null)
{
    Debug.LogError("ConvaiManager not found in scene. Add it via Convai → Create Manager.");
    return;
}
```

{% hint style="warning" %}
`ActiveManager` returns `null` if no `ConvaiManager` exists in the scene or if it has not yet bootstrapped. Always null-check before use, especially in components that may `OnEnable` before the manager initializes.
{% endhint %}

***

## SDK Version

The `ConvaiSDK` static class exposes the SDK version. It has no other members.

```csharp
using Convai.Application;

Debug.Log($"Convai SDK {ConvaiSDK.Version}"); // e.g. "4.2.0"

// Conditional feature check
if (ConvaiSDK.Version >= new System.Version(4, 2, 0))
{
    // Use a feature introduced in 4.2
}
```

***

## State Properties

| Property         | Type   | Description                                                                             |
| ---------------- | ------ | --------------------------------------------------------------------------------------- |
| `IsBootstrapped` | `bool` | Static. True when the runtime has completed initial bootstrap — safe to access facades. |
| `IsInitialized`  | `bool` | True when bootstrap is complete AND the event hub is available.                         |
| `IsConnected`    | `bool` | True when the room session is in `Connected` state.                                     |

***

## Facade Accessors

These properties give direct access to the high-level scripting facades. Each is documented on its own page.

| Property      | Type                | Page                                                                                                                                                 |
| ------------- | ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Events`      | `ConvaiEvents`      | [Session Events](/broken/pages/a7e3f4a9d58a1af76a754f96aace9c0e8c0f5b75), [Character Events](/broken/pages/a9404d9d31173368658d5c855f56adc153ddc00c) |
| `Audio`       | `ConvaiAudio`       | [Audio API](/broken/pages/f4c7cb90e621fec9c036f882745dbb0509a141b7)                                                                                  |
| `Transcripts` | `ConvaiTranscripts` | [Transcript API](/broken/pages/9c72706d1316b0d8788f937d556d965b9ee5c279)                                                                             |

***

## Ownership Properties

| Property                      | Type                             | Description                                                           |
| ----------------------------- | -------------------------------- | --------------------------------------------------------------------- |
| `Characters`                  | `IReadOnlyList<ConvaiCharacter>` | All `ConvaiCharacter` instances currently owned by this manager       |
| `Player`                      | `ConvaiPlayer`                   | The `ConvaiPlayer` instance owned by this manager                     |
| `ActiveConversationCharacter` | `ConvaiCharacter`                | The character currently set as the conversation target; may be `null` |
| `ConversationMode`            | `ConvaiManagerConversationMode`  | The configured conversation mode for this manager                     |
| `ActiveConversationInputMode` | `ConversationInputMode`          | The runtime conversation input mode currently in effect               |
| `PushToTalkKey`               | `KeyCode`                        | The key code used for push-to-talk, when mode is `PushToTalk`         |

### `ConvaiManagerConversationMode` Enum

| Value                 | Description                                                                       |
| --------------------- | --------------------------------------------------------------------------------- |
| `UseRoomDefaults` (0) | Uses the conversation input mode configured in `TurnTakingOptions` on the manager |
| `HandsFree` (1)       | Sets hands-free (LocalAudio) mode, overriding room defaults                       |
| `PushToTalk` (2)      | Sets push-to-talk mode, overriding room defaults                                  |

***

## Room Operations

### `ConnectAsync`

```csharp
// Simple connect — uses scene configuration
IConvaiOperation<RoomSession> ConnectAsync(CancellationToken ct = default)

// Connect with runtime overrides
IConvaiOperation<RoomSession> ConnectAsync(RoomSessionConnectOptions options, CancellationToken ct = default)
```

Returns a `RoomSession` on success. See [Operation & Stream Types](/broken/pages/899573c6355c9e81274dd551dab24ec910d8459b) for consumption patterns.

#### `RoomSessionConnectOptions` Fields

Pass this to the second overload to override runtime behavior at connect time.

| Field                       | Type                                  | Description                                                          |
| --------------------------- | ------------------------------------- | -------------------------------------------------------------------- |
| `TurnTaking`                | `TurnTakingOptions`                   | Override the turn-taking configuration for this session              |
| `EndUserId`                 | `string`                              | Override the end-user ID for this session (used by Long-Term Memory) |
| `EndUserMetadata`           | `IReadOnlyDictionary<string, object>` | Additional metadata for the end user                                 |
| `ActionConfigOverride`      | `ConvaiActionConfig`                  | Override the action configuration for this session                   |
| `ActionDefinitionsOverride` | `List<ConvaiActionDefinition>`        | Override the action definitions registered for this session          |

```csharp
var options = new RoomSessionConnectOptions
{
    EndUserId = currentUser.Id,
    EndUserMetadata = new Dictionary<string, object>
    {
        ["department"] = "Engineering",
        ["cohort"]     = "2025-Q2"
    }
};

var result = await manager.ConnectAsync(options, destroyCancellationToken);
if (!result.IsSuccessful)
    Debug.LogError($"Connect failed: {result.Error.Message}");
```

### `DisconnectAsync`

```csharp
IConvaiOperation<Unit> DisconnectAsync(CancellationToken ct = default)
```

Gracefully disconnects the room session. Resolves when the session reaches `Disconnected`.

***

## Conversation Control

| Method                                                                                      | Returns                  | Description                                                                                                |
| ------------------------------------------------------------------------------------------- | ------------------------ | ---------------------------------------------------------------------------------------------------------- |
| `SetConversationInputModeAsync(ConversationInputMode mode, CancellationToken ct = default)` | `IConvaiOperation<Unit>` | Switches the room's conversation input mode at runtime                                                     |
| `StartListening()`                                                                          | `void`                   | Starts microphone capture. Shortcut for `Audio.StartListeningAsync()` with default device.                 |
| `ToggleMicMute()`                                                                           | `bool`                   | Toggles microphone mute. Returns the new mute state.                                                       |
| `EnableAudioAndStartListening()`                                                            | `void`                   | Calls `Audio.EnableAudioPlayback()` then starts listening. Required on WebGL before any audio interaction. |

***

## Ownership Management

Use these methods to control which characters and player the manager owns, and which character is the active conversation target.

| Method                                                           | Description                                                                                     |
| ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `SetExplicitConversationTarget(ConvaiCharacter character)`       | Sets the active conversation target character. Pass `null` to clear.                            |
| `SetExplicitPlayer(ConvaiPlayer player)`                         | Assigns a specific `ConvaiPlayer` instance as the managed player                                |
| `SetExplicitCharacters(IEnumerable<ConvaiCharacter> characters)` | Replaces the managed character list with the provided set                                       |
| `RefreshReferences()`                                            | Rescans the scene for `ConvaiCharacter` and `ConvaiPlayer` instances to rebuild the managed set |

***

## Service Accessor Pattern

For advanced scenarios that require direct access to internal services, `ConvaiManager` exposes 12 typed `TryGet*` accessors. Each returns `true` and sets the `out` parameter on success, or returns `false` if the service is unavailable (not yet bootstrapped or not registered).

```csharp
if (manager.TryGetMicrophoneDeviceService(out var micService))
{
    var devices = micService.GetAvailableDevices();
    // populate device picker UI
}
```

| Method                                                              | Service Type                     | Common Use Case                                                         |
| ------------------------------------------------------------------- | -------------------------------- | ----------------------------------------------------------------------- |
| `TryGetEventHub(out IEventHub)`                                     | `IEventHub`                      | Raw event bus access via `ConvaiEvents.Raw`; advanced subscriptions     |
| `TryGetRoomConnectionService(out IConvaiRoomConnectionService)`     | `IConvaiRoomConnectionService`   | Low-level connection lifecycle control                                  |
| `TryGetRoomAudioService(out IConvaiRoomAudioService)`               | `IConvaiRoomAudioService`        | Direct audio service access (bypasses `ConvaiAudio` facade)             |
| `TryGetAgentRegistry(out IAgentRegistry)`                           | `IAgentRegistry`                 | Query registered characters and players                                 |
| `TryGetSettingsPanelController(out IConvaiSettingsPanelController)` | `IConvaiSettingsPanelController` | Programmatically open/close the settings panel                          |
| `TryGetRuntimeSettingsService(out IConvaiRuntimeSettingsService)`   | `IConvaiRuntimeSettingsService`  | Read and write runtime settings (audio volume, mic device, etc.)        |
| `TryGetMicrophoneDeviceService(out IMicrophoneDeviceService)`       | `IMicrophoneDeviceService`       | Enumerate available microphone devices; build device picker UI          |
| `TryGetPermissionService(out IConvaiPermissionService)`             | `IConvaiPermissionService`       | Request platform microphone permissions (Android, iOS)                  |
| `TryGetNotificationService(out IConvaiNotificationService)`         | `IConvaiNotificationService`     | Trigger SDK notifications from your own scripts                         |
| `TryGetPlayerInputService(out IPlayerInputService)`                 | `IPlayerInputService`            | Access player input state and text message routing                      |
| `TryGetVisibleCharacterService(out IVisibleCharacterService)`       | `IVisibleCharacterService`       | Query which characters are visible in the camera frustum                |
| `TryGetTransportProvider(out ITransportProvider)`                   | `ITransportProvider`             | Access the transport layer for diagnostic or custom transport scenarios |

{% hint style="info" %}
Prefer the `Events`, `Audio`, and `Transcripts` facade properties for common tasks. The `TryGet*` accessors are intended for advanced integrations and custom tooling.
{% endhint %}

***

## Usage Examples

### Example 1 — Connect On Scene Load With Cancellation

An industrial safety simulation connects to Convai when the scene loads, tied to the component's lifetime via `destroyCancellationToken` so the connect operation cancels cleanly if the scene unloads mid-attempt.

{% code title="SceneConnector.cs" %}
```csharp
using Convai.Runtime.Core.Async;
using Convai.Runtime.Facades;
using UnityEngine;

public class SceneConnector : MonoBehaviour
{
    private async void Start()
    {
        var manager = ConvaiManager.ActiveManager;
        if (manager == null) return;

        try
        {
            var session = await manager.ConnectAsync(destroyCancellationToken);
            Debug.Log($"Connected. Session: {session.RoomId}");
        }
        catch (ConvaiOperationException ex)
        {
            Debug.LogError($"Connect failed: {ex.Message}");
        }
        catch (System.OperationCanceledException) { /* scene unloaded */ }
    }
}
```
{% endcode %}

### Example 2 — Swap Conversation Target On Trigger Zone Entry

A corporate onboarding simulation has multiple AI advisors in a room. When a learner walks into an advisor's zone, that advisor becomes the active conversation target.

{% code title="AdvisorZone.cs" %}
```csharp
using Convai.Runtime.Components;
using Convai.Runtime.Facades;
using UnityEngine;

public class AdvisorZone : MonoBehaviour
{
    [SerializeField] private ConvaiCharacter _advisor;

    private void OnTriggerEnter(Collider other)
    {
        if (!other.CompareTag("Player")) return;
        ConvaiManager.ActiveManager?.SetExplicitConversationTarget(_advisor);
    }

    private void OnTriggerExit(Collider other)
    {
        if (!other.CompareTag("Player")) return;
        ConvaiManager.ActiveManager?.SetExplicitConversationTarget(null);
    }
}
```
{% endcode %}

### Example 3 — Microphone Device Picker UI

An interactive experience lets users choose their preferred microphone before a session starts, using the `IMicrophoneDeviceService` to enumerate available devices.

{% code title="MicrophonePicker.cs" %}
```csharp
using Convai.Runtime.Facades;
using System.Linq;
using TMPro;
using UnityEngine;

public class MicrophonePicker : MonoBehaviour
{
    [SerializeField] private TMP_Dropdown _deviceDropdown;

    private void Start()
    {
        var manager = ConvaiManager.ActiveManager;
        if (manager == null || !manager.TryGetMicrophoneDeviceService(out var micService))
            return;

        var devices = micService.GetAvailableDevices();
        _deviceDropdown.ClearOptions();
        _deviceDropdown.AddOptions(devices.Select(d => d.Name).ToList());
    }
}
```
{% endcode %}

***

## Next Steps

{% content-ref url="/broken/pages/f4c7cb90e621fec9c036f882745dbb0509a141b7" %}
[Broken link](/broken/pages/f4c7cb90e621fec9c036f882745dbb0509a141b7)
{% endcontent-ref %}
