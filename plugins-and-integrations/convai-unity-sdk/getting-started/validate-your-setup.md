---
title: Validate your setup
description: >-
  Check a Convai character with the Troubleshooter window and confirm required
  components are present before entering Play Mode.
last_reviewed: "5.0.0-preview"
---

Before entering Play Mode, check your character with the Convai Troubleshooter and the scene-wide validator. The two answer different questions: the Troubleshooter reports what would stop a module from working on the selected character, while the validator confirms the basic scene wiring — `ConvaiManager`, `ConvaiCharacter`, `ConvaiPlayer`, and the Character ID field — is in place. Run both.

## Check a character with the Troubleshooter

Open **Convai > Troubleshooter**. The window arrives with your currently selected character loaded, or lists every `ConvaiCharacter` in the scene when you switch to **This Scene** mode.

For the selected character, the Troubleshooter reports findings one row per module. Each finding shows a severity and, when there is something to do about it, a fix button, a **Show Me** button that selects the object it is about, or an **Open** button that opens the relevant editor window. Use **Re-check** after making a change, or **Fix Everything That Can Be Fixed** to apply every one-click fix at once.

Not every row offers the same help. Actions rows come with fixes you can apply from the window. Rows for the embodiment modules — Gaze, Body Animation, Body Language, Emotion, and the embodiment setup itself — report what they find but carry no fix or locate button, so act on those in each module's own editor window. A row appears only when the module has something to say about the character, so a character without a module contributes no row for it.

Actions applies to every `ConvaiCharacter`, so even a freshly wired character with no other modules shows an Actions row. On a character with no actions configured yet, that row is informational: it tells you the character will talk but not act, not that something is broken.

The Troubleshooter checks module setup, not the raw scene wiring. Missing `ConvaiManager` or an empty Character ID are caught by the scene validator below.

## Run the scene validator

The Scene Validator inspects your scene for missing components, empty required fields, and common misconfigurations. Run it at any point during development, not only at the end.

In the Unity Editor menu bar, select **GameObject > Convai > Validate Scene Setup**.

If TextMesh Pro resources are missing, the validator first offers an **Import** action in **TextMesh Pro Resources Missing**. After the resource check, it reports **ERRORS (must fix)**, **WARNINGS**, and **How to fix**, or a **Validation Passed** dialog.

## Validator checks

### Errors — must fix

These prevent the scene from connecting to Convai.

| Error                                          | Cause                                                                                                                         | Fix                                                                    |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------ |
| `Missing ConvaiManager`              | SDK is not initialized                                                                                                        | Run **GameObject > Convai > Setup Required Components**               |
| `Missing ConvaiRoomManager`          | Room connection component missing                                                                                            | Run **GameObject > Convai > Setup Required Components**               |
| TextMesh Pro Essential Resources not imported  | Convai's UI prefabs and fonts reference TextMesh Pro's runtime shader and default font, which Unity imports per project rather than shipping in the package. A scene containing Convai UI throws on open without them. | Select **Window > TextMeshPro > Import TMP Essential Resources**      |
| `No ConvaiCharacter components found in scene`            | No characters registered                                                                                                     | Add `ConvaiCharacter` to your NPC GameObject                          |
| `ConvaiCharacter on '<object>' has no Character ID`          | Required field is empty                                                                                                       | Enter the Character ID from your Convai dashboard                     |
| `No ConvaiPlayer component found in scene`               | Player component missing                                                                                                     | Select the player object and choose **Add Component > Convai > Convai Player**               |
| Two or more characters use the same Character ID | Ownership, participant, and audio routing would collide | Give each character its own dashboard Character ID |

### Warnings — recommended

Warnings need interpretation before connecting. Some describe configuration that cannot produce the intended session.

| Warning                                      | Cause                                                                          | Fix                                                    |
| -------------------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------ |
| API key not configured                       | `ConvaiSettings.HasApiKey` returns false                                       | Open **Convai > Settings > Credentials** and enter your API key       |
| Video mode active but no vision source found | The room's `ConvaiRoomManager` hierarchy has no `IVisionPublisher` component, no `IVisionFrameSource` component, or both, while the room's effective connection type is `Video` | Add a vision publisher and a frame source component, or switch to `Audio` mode |
| Only one of the scene's characters is active | Connecting starts a single-character room without a roster | Enable the intended roster before connecting, or turn off Auto Connect and connect once all members are active |
| Group conversation configuration warnings | An enabled group component fails its setup checks | Follow [group conversation troubleshooting](../features/group-conversation/troubleshooting.md), then validate again |

The validator derives **API key not configured** from `ConvaiSettings.HasApiKey` alone; it does not check `ConvaiSettings.HasValidAuthConfig`, which accounts for the project's `AuthMode`. A project running in Auth Token mode is not required to have an API key, so this warning can appear even when authentication is correctly configured. If your project uses Auth Token mode, treat this warning as expected and verify your setup on the [Authentication](../authentication/README.md) pages instead of adding an API key.

{% hint style="success" %}
When the validator has no errors and you have addressed its relevant warnings, enter Play Mode to test the connection. The validator does not prove account access or runtime behavior.
{% endhint %}

## Play mode startup checklist

After the validator passes, enter Play Mode and watch the Console for these log lines in order.

* [ ] `[ConvaiRuntime] Started successfully` — SDK initialized all internal services
* [ ] `[RoomConnectionRuntimeAdapter] Room connection succeeded (mode=create).` — the room connected
* [ ] If a chat transcript UI is present, it starts showing messages once the conversation starts — it logs nothing on a successful connection, so watch the UI itself rather than the Console
* [ ] Character `IsCharacterReady` becomes `true` within 30 seconds — Convai has acknowledged the character

{% hint style="info" %}
Wait for `IsCharacterReady` or `OnCharacterReady` before sending the first message. A connected room and a ready character are separate states. Check the Console when readiness times out; do not assume a fixed response delay.
{% endhint %}

To check `IsCharacterReady` at runtime:

```csharp
using Convai.Runtime.Components;
using UnityEngine;

public class CharacterReadinessNotice : MonoBehaviour
{
    [SerializeField] private ConvaiCharacter character;

    private void OnEnable()
    {
        if (character == null) return;
        character.OnCharacterReady += HandleReady;
        if (character.IsCharacterReady) HandleReady();
    }

    private void OnDisable()
    {
        if (character != null) character.OnCharacterReady -= HandleReady;
    }

    private void HandleReady() => Debug.Log("Character is ready to converse.");
}
```

## Troubleshooting

| Symptom                                               | Likely cause                                                      | Fix                                                                                                                                                         |
| ----------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `[ConvaiRuntime] Started successfully` not in Console | `ConvaiManager` missing or failed to bootstrap                    | Check that `ConvaiManager` is in the scene. Look for earlier errors in the Console.                                                                         |
| Room never connects — no character-connected log      | API key invalid or missing; network issue                         | Verify your API key in **Convai > Settings > Credentials**. Check firewall rules allow WebSocket/HTTPS to `live.convai.com`.                                               |
| Nothing connects and the Console shows no error       | **Starts Connected** on `ConvaiRoomManager` (or **Connect On Start** on its profile) is off, which also blocks every character's **Auto Connect** | Turn **Starts Connected** on. When **Room Setup Source** is **Profile Asset**, the Room Manager shows the profile's value read-only, so turn **Connect On Start** on in the profile instead. Or call `ConnectAsync` or `StartConversationAsync` from your own code. |
| Chat transcript UI shows no messages                  | Required UI references are not assigned on `ChatTranscriptUI`     | Check the Console for `chatContainer is not assigned - messages will not display` or `scrollRect is not assigned - auto-scroll will not work`, and assign the missing reference in the Inspector. |
| Character `IsCharacterReady` stays `false`            | Character ID is wrong or character does not exist on your account | Verify the Character ID matches exactly what is shown on your Convai dashboard.                                                                             |
| Mic never opens — character hears nothing             | Push-to-talk mode is on and mic starts muted                      | In `ConvaiRoomManager`, set **Conversation > How The Player Talks** to **Hands Free**, or use the configured **Push To Talk Key**.                                                              |
| Character voice plays but blendshapes do not animate  | `ConvaiLipSyncComponent` not configured or profile ID mismatch    | Add `ConvaiLipSyncComponent` to the character. Choose the matching **Profile** and assign meshes in **Renderers**; use **Auto-Find** and the map validator to check the mapping. |
| Materials appear pink in sample scenes                | Render pipeline mismatch (Built-in vs URP)                        | Convert materials via **Edit > Rendering > Materials > Convert All Built-in Materials to URP**, or reassign URP shaders manually.                           |

## Setup complete

Your scene now has:

* The SDK installed and connected to Convai with a valid API key
* A scene with `ConvaiManager`, `ConvaiRoomManager`, `ConvaiCharacter`, and `ConvaiPlayer`
* The scene validator and the Troubleshooter both reporting zero errors
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
