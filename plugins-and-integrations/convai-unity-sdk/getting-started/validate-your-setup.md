---
title: Validate your setup
description: >-
  Run the scene validation tool to confirm all required components are present,
  connected, and configured correctly.
last_reviewed: "4.2.0"
---

Before deploying or sharing your scene, run the SDK's built-in validator and verify the Play Mode startup sequence. This page covers every check the validator performs, the expected console output on success, and a troubleshooting table for common failures.

## Run the scene validator

The Scene Validator inspects your scene for missing components, empty required fields, and common misconfigurations. Run it at any point during development — not just at the end.

In the Unity Editor menu bar, select **GameObject > Convai > Validate Scene Setup**.

A dialog appears with a list of **Errors** (must fix), **Warnings** (recommended), and **Next Steps** (suggested actions).

## Validator checks

### Errors — must fix

These prevent the scene from connecting to Convai.

| Error                                 | Cause                    | Fix                                                     |
| ------------------------------------- | ------------------------ | ------------------------------------------------------- |
| No `ConvaiManager` found in scene     | SDK is not initialized   | Run **GameObject > Convai > Setup Required Components** |
| No `ConvaiCharacter` found in scene   | No characters registered | Add `ConvaiCharacter` to your NPC GameObject            |
| `ConvaiCharacter` has no Character ID | Required field is empty  | Enter the Character ID from your Convai dashboard       |
| No `ConvaiPlayer` found in scene      | Player component missing | Run **GameObject > Convai > Setup Required Components** |

### Warnings — recommended

These do not block connection but may affect functionality.

| Warning                                      | Cause                                                                          | Fix                                                    |
| -------------------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------ |
| API key not configured                       | `ConvaiSettings.HasApiKey` returns false                                       | Open **Convai > Account** and enter your API key       |
| Video mode active but no vision source found | `_connectionType` is `AudioVideo` but no `IVisionFrameSource` component exists | Add a frame source component or switch to `Audio` mode |

{% hint style="success" %}
When the validator shows zero errors and zero warnings, your scene is ready for Play Mode.
{% endhint %}

## Play mode startup checklist

After the validator passes, enter Play Mode and watch the Console for these log lines in order.

* [ ] `[ConvaiRuntime] Started successfully` — SDK initialized all internal services
* [ ] `[RoomConnectionRuntimeAdapter] Character <character-id> connected successfully (mode=create).` — character connected to Convai
* [ ] `[ChatTranscriptUI] Dependencies injected via explicit initialization` — transcript UI connected (if present)
* [ ] Character `IsCharacterReady` becomes `true` within 30 seconds — Convai has acknowledged the character

{% hint style="info" %}
The character-ready signal may arrive 2–10 seconds after the room connects, depending on server load. If it does not arrive within `_characterReadyTimeoutSeconds` (default: 30s), the SDK logs a timeout warning.
{% endhint %}

To check `IsCharacterReady` at runtime:

```csharp
void Start()
{
    var character = FindFirstObjectByType<ConvaiCharacter>();
    character.OnCharacterReady += () => Debug.Log("Character is ready to converse.");
}
```

## Troubleshooting

| Symptom                                               | Likely cause                                                      | Fix                                                                                                                                                         |
| ----------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `[ConvaiRuntime] Started successfully` not in Console | `ConvaiManager` missing or failed to bootstrap                    | Check that `ConvaiManager` is in the scene. Look for earlier errors in the Console.                                                                         |
| Room never connects — no character-connected log      | API key invalid or missing; network issue                         | Verify your API key in **Convai > Account**. Check firewall rules allow WebSocket/HTTPS to `live.convai.com`.                                               |
| `[ChatTranscriptUI] Dependencies not injected...`     | `ConvaiManager` not found at UI startup                           | Ensure `ConvaiManager` is in the scene. Its execution order (-1100) guarantees it runs first.                                                               |
| Character `IsCharacterReady` stays `false`            | Character ID is wrong or character does not exist on your account | Verify the Character ID matches exactly what is shown on your Convai dashboard.                                                                             |
| Mic never opens — character hears nothing             | Push-to-talk mode is on and mic starts muted                      | In `ConvaiRoomManager`, confirm **Mode** is `HandsFree`, or press **T** if using push-to-talk.                                                              |
| Character voice plays but blendshapes do not animate  | `ConvaiLipSyncComponent` not configured or profile ID mismatch    | Add `ConvaiLipSyncComponent` to the character. Verify `_lockedProfileId` matches your character's transport format. Assign target `SkinnedMeshRenderer`(s). |
| Materials appear pink in sample scenes                | Render pipeline mismatch (Built-in vs URP)                        | Convert materials via **Edit > Rendering > Materials > Convert All Built-in Materials to URP**, or reassign URP shaders manually.                           |

## Setup complete

Your scene now has:

* The SDK installed and connected to Convai with a valid API key
* A scene with `ConvaiManager`, `ConvaiRoomManager`, `ConvaiCharacter`, and `ConvaiPlayer`
* Validator passing with zero errors
* A character that connects, becomes ready, and responds to voice input

## Next steps

Continue the getting started path to configure input mode, audio, and UI.

{% content-ref url="configure-conversation-input-mode.md" %}
[Configure conversation input mode](configure-conversation-input-mode.md)
{% endcontent-ref %}

Or explore the Features section to add Actions, Emotion, Long-Term Memory, or Vision to your characters.

{% content-ref url="../features/README.md" %}
[Features](../features/README.md)
{% endcontent-ref %}

Review Core Concepts for a deeper understanding of the session lifecycle and event system.

{% content-ref url="../core-concepts/README.md" %}
[Core Concepts](../core-concepts/README.md)
{% endcontent-ref %}
