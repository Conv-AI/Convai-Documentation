# custom scene setup

This page walks you through setting up a new scene with a Convai AI character from scratch. By the end, your scene will have the minimum required components for a character to receive voice input and respond.

## Minimum Required Hierarchy

Every working Convai scene needs these three things:

```
[Manager GameObject]  → ConvaiManager + ConvaiRoomManager
[NPC GameObject]      → ConvaiCharacter + ConvaiAudioOutput + AudioSource
[Player GameObject]   → ConvaiPlayer
```

The setup wizard creates the first and third automatically. You add the NPC components yourself.

***

{% stepper %}
{% step %}
**Add the Required Manager Components**

In the Unity Editor menu bar, select **GameObject > Convai > Setup Required Components**.

Unity creates a **ConvaiManager** GameObject with `ConvaiManager` and `ConvaiRoomManager` attached, and a **ConvaiPlayer** GameObject with `ConvaiPlayer` attached. Both appear in the Hierarchy.

{% hint style="info" %}
`ConvaiRoomManager` always lives on the same GameObject as `ConvaiManager`. Do not move it to a separate GameObject.
{% endhint %}
{% endstep %}

{% step %}
**Add ConvaiCharacter to Your NPC**

In the Hierarchy, select the NPC GameObject you want to make conversational. In the Inspector, click **Add Component** and add `ConvaiCharacter`.
{% endstep %}

{% step %}
**Add AudioSource and ConvaiAudioOutput**

On the same NPC GameObject, add `AudioSource`, then add `ConvaiAudioOutput`.

All three components — `ConvaiCharacter`, `ConvaiAudioOutput`, and `AudioSource` — should now appear on the same GameObject in the Inspector.
{% endstep %}

{% step %}
**Set the Character ID**

In the `ConvaiCharacter` component, set the **Character ID** field to the ID of your character from the [Convai dashboard](https://convai.com/).

{% hint style="warning" %}
The Character ID field is required. If it is empty, the character cannot connect to Convai and the Scene Validator will report an error.
{% endhint %}
{% endstep %}

{% step %}
**Validate the Scene**

In the menu bar, select **GameObject > Convai > Validate Scene Setup**.

A dialog appears listing errors, warnings, and recommended next steps.

**Errors (must fix):**

| Error                                 | Fix                                          |
| ------------------------------------- | -------------------------------------------- |
| No `ConvaiManager` found              | Run **Setup Required Components**            |
| No `ConvaiCharacter` found            | Add `ConvaiCharacter` to your NPC GameObject |
| `ConvaiCharacter` has no Character ID | Set the Character ID from your dashboard     |
| No `ConvaiPlayer` found               | Run **Setup Required Components**            |

**Warnings:**

| Warning                | Fix                                          |
| ---------------------- | -------------------------------------------- |
| API key not configured | Open **Convai > Account** and enter your key |

When the validator reports no errors, the scene is ready for Play Mode.
{% endstep %}

{% step %}
**Enter Play Mode**

Press **Play**. The Unity Console logs:

* `[ConvaiRuntime] Started successfully` — SDK initialized
* `[ConvaiRoomManager] session-connected` — room connection active

Speak into your microphone. The character responds within a few seconds.
{% endstep %}
{% endstepper %}

***

## Usage Examples

## Example 1: Safety Training Simulation

**Scenario:** An industrial safety trainer NPC responds to trainee questions about equipment procedures.

**Setup:**

* NPC GameObject: `SafetyTrainer` with `ConvaiCharacter`, `ConvaiAudioOutput`, `AudioSource`
* Character ID: ID of your safety trainer character from the Convai dashboard
* `ConvaiCharacter._characterName`: `"Safety Trainer"`
* `ConvaiCharacter._enableRemoteAudio`: `true`

**Expected outcome:** Trainees speak to the NPC and receive voice responses about safety procedures. The character name appears in the transcript UI.

***

## Example 2: Multiple Characters in One Scene

**Scenario:** A medical training simulation with two characters — a supervising doctor and a nurse.

**Setup:**

* Two separate NPC GameObjects, each with `ConvaiCharacter`, `ConvaiAudioOutput`, `AudioSource`
* Each `ConvaiCharacter` has its own unique Character ID
* Only one `ConvaiManager` and one `ConvaiPlayer` in the scene

**Expected outcome:** Both characters are discovered and registered automatically. Conversation switches between them based on which character the player addresses.

{% hint style="info" %}
Each character maintains an independent session. Character A and Character B do not share context unless your Convai character configuration explicitly links them.
{% endhint %}

***

## Next Steps

With your scene set up and validated, configure how the player speaks to the character.

{% content-ref url="/broken/pages/bf1d5170d716a087ac55effdac818850ed2ee846" %}
[Broken link](/broken/pages/bf1d5170d716a087ac55effdac818850ed2ee846)
{% endcontent-ref %}
