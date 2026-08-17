---
title: Validate your setup
description: >-
  Check a Convai character with the Troubleshooter window and confirm required
  components are present before entering Play Mode.
last_reviewed: "4.6.0"
---

Before entering Play Mode, check your character with the Convai Troubleshooter and the scene-wide validator. The two answer different questions: the Troubleshooter reports what would stop a module from working on the selected character, while the validator checks project resources and the basic scene wiring. Run both.

## Check a character with the Troubleshooter

Open **Convai > Troubleshooter**. The window arrives with your currently selected character loaded, or lists every `ConvaiCharacter` in the scene when you switch to **This Scene** mode.

For the selected character, the Troubleshooter reports findings one row per module. Each finding shows a severity and, when there is something to do about it, a fix button, a **Show Me** button that selects the object it is about, or an **Open** button that opens the relevant editor window. Use **Re-check** after making a change, or **Fix Everything That Can Be Fixed** to apply every one-click fix at once.

Not every row offers the same help. Actions rows come with fixes you can apply from the window. Rows for the embodiment modules — Gaze, Body Animation, Body Language, Emotion, and the embodiment setup itself — report what they find but carry no fix or locate button, so act on those in each module's own editor window. A row appears only when the module has something to say about the character, so a character without a module contributes no row for it.

Actions applies to every `ConvaiCharacter`, so even a freshly wired character with no other modules shows an Actions row. On a character with no actions configured yet, that row is informational: it tells you the character will talk but not act, not that something is broken.

The Troubleshooter checks module setup, not the raw scene wiring. Missing manager, room, character, or player components and empty Character IDs are caught by the scene validator below.

## Run the scene validator

The Scene Validator inspects your scene for missing components, empty required fields, and common misconfigurations. Run it at any point during development, not only at the end.

In the Unity Editor menu bar, select **GameObject > Convai > Validate Scene Setup**.

A dialog appears with a list of **Errors** (must fix), **Warnings** (recommended), and **Next Steps** (suggested actions).

## Validator checks

### Errors — must fix

These prevent the scene from connecting to Convai.

| Error | Cause | Fix |
| --- | --- | --- |
| Missing `ConvaiManager` | SDK entry point is absent | Run **GameObject > Convai > Setup Required Components** |
| Missing `ConvaiRoomManager` | Room service component is absent | Run **GameObject > Convai > Setup Required Components** |
| TextMesh Pro Essential Resources are not imported | Shipped Convai UI fonts and shaders cannot resolve | Accept the import prompt, or use **Window > TextMeshPro > Import TMP Essential Resources** |
| No `ConvaiCharacter` components found | No characters are registered | Add `ConvaiCharacter` to an NPC GameObject |
| A `ConvaiCharacter` has no Character ID | A required character field is empty | Enter the Character ID from your Convai dashboard |
| No `ConvaiPlayer` component found | The local player is not registered | Add `ConvaiPlayer` to an explicit player GameObject |

### Warnings — recommended

These do not block connection but may affect functionality.

| Warning | Cause | Fix |
| --- | --- | --- |
| API key not configured | `ConvaiSettings.HasApiKey` is `false` | Open **Convai > Settings > Credentials** and enter your API key |
| Video mode lacks its vision pipeline | `ConvaiRoomManager.EffectiveConnectionType` is `Video`, but its hierarchy lacks an `IVisionPublisher`, an `IVisionFrameSource`, or both | Configure the Vision module under the room manager, or switch the connection type to `Audio` |

**Ready for Play Mode:** The validator shows zero errors, and you have reviewed each warning.

{% hint style="warning" %}
The SDK <code class="expression">space.vars.unity_sdk_version</code> scene validator checks `ConvaiSettings.HasApiKey` without considering Auth Token mode. A correctly configured Auth Token project can therefore retain the **API key not configured** warning. For that mode, verify the auth-token provider or endpoint manually and do not treat this warning alone as a failed setup.
{% endhint %}

## Play mode startup checklist

After the validator passes, enter Play Mode and watch the Console for these log lines in order.

* [ ] `[ConvaiRuntime] Started successfully` — SDK initialized all internal services
* [ ] `[RoomConnectionRuntimeAdapter] Character <character-id> connected successfully (mode=create).` — character connected to Convai
* [ ] If a chat transcript UI is present, it starts showing messages once the conversation starts — it logs nothing on a successful connection, so watch the UI itself rather than the Console
* [ ] Character `IsCharacterReady` becomes `true` within 30 seconds — Convai has acknowledged the character

{% hint style="info" %}
Readiness can arrive after the room transport connects. If it does not arrive within `CharacterReadyTimeoutSeconds` (default: 30 seconds), the SDK reports a timeout. In a multi-character preview room, the initial membership gates connection while secondary memberships can remain `Starting` or become `Failed`.
{% endhint %}

To check `IsCharacterReady` at runtime:

```csharp
using Convai.Runtime.Components;
using UnityEngine;

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
| Room never connects — no character-connected log      | API key invalid or missing; network issue                         | Verify your API key in **Convai > Settings > Credentials**. Check firewall rules allow WebSocket/HTTPS to `live.convai.com`.                                               |
| Chat transcript UI shows no messages                  | Required UI references are not assigned on `ChatTranscriptUI`     | Assign its chat container and scroll view references in the Inspector, then check the Console for the component's exact diagnostic. |
| Character `IsCharacterReady` stays `false`            | Character ID is wrong or character does not exist on your account | Verify the Character ID matches exactly what is shown on your Convai dashboard.                                                                             |
| Mic never opens — character hears nothing             | Push-to-talk mode is on and mic starts muted                      | In `ConvaiRoomManager`, confirm **Mode** is `HandsFree`, or press **T** if using push-to-talk.                                                              |
| Character voice plays but blendshapes do not animate  | `ConvaiLipSyncComponent` not configured or profile ID mismatch    | Add `ConvaiLipSyncComponent` to the character. Verify `_lockedProfileId` matches your character's transport format. Assign target `SkinnedMeshRenderer`(s). |
| Materials appear pink in sample scenes                | Render pipeline mismatch (Built-in vs URP)                        | Convert materials via **Edit > Rendering > Materials > Convert All Built-in Materials to URP**, or reassign URP shaders manually.                           |

## Setup complete

Your scene now has:

* The SDK installed and connected to Convai with a valid API key or configured Auth Token flow
* A scene with `ConvaiManager`, `ConvaiRoomManager`, `ConvaiCharacter`, and `ConvaiPlayer`
* The scene validator and the Troubleshooter both reporting zero errors, with any remaining warnings reviewed for the selected authentication mode
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
