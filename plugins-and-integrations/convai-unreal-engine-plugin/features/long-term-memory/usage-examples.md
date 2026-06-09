---
title: Long-term memory usage examples
description: Apply Unreal long-term memory patterns for returning learners, shared devices, first sessions, and fresh-start reset flows.
last_reviewed: "4.0.0-beta.21"
---

Use these patterns after [Long-term memory quick start](quick-start.md) is working. Each example focuses on which identity values to set before `StartSession`.

## Returning learner in a training simulation

A safety training simulation should remember that a learner has already completed a valve inspection module.

**Setup:**

- Long-term memory (LTM) is enabled for the training character.
- The learner has a saved `SpeakerID`.

**Blueprint flow:**

{% stepper %}
{% step %}
### Load saved values

Load `SpeakerID` from the learner's `SaveGame` or account profile.
{% endstep %}

{% step %}
### Assign identity

Set `UConvaiChatbotComponent.EndUserID` to the saved `SpeakerID`.

Call **Set End User ID** on `UConvaiPlayerComponent` with the same value.
{% endstep %}

{% step %}
### Connect

Call `StartSession` after the identity values are assigned.
{% endstep %}
{% endstepper %}

**Expected outcome:** The character can refer to facts learned in earlier sessions for the same learner and character.

## First-time player profile

A new player starts the application with no stored identity.

**Setup:**

- The project has collected a display name, such as `Alex`.
- No saved `SpeakerID` exists for the profile.

**Blueprint flow:**

1. Call **Convai Create Speaker ID** with **Speaker Name** set to the display name.
2. Optionally set **Device Id** to a stable device or account identifier.
3. On **On Success**, save the returned `SpeakerID`.
4. Assign that `SpeakerID` to the chatbot and player components.
5. Call `StartSession`.

**Expected outcome:** Convai creates a distinct memory scope for this player and character pair. Future launches should reuse the saved `SpeakerID`.

## Shared classroom device

Several learners use the same machine during guided practice. Device fallback would merge their memory, so each learner needs an explicit identity.

**Setup:**

- Each learner selects or signs into a profile before interacting with the character.
- Each profile stores its own `SpeakerID`.

**Blueprint flow:**

1. On profile selection, load that profile's `SpeakerID`.
2. Set the chatbot and player `EndUserID` values before `StartSession`.
3. Keep each profile's `SpeakerID` separate from other profiles on the same device.

**Expected outcome:** The character remembers each learner separately, even though all learners use the same device.

## Account-backed identity

An enterprise onboarding app already has a user account ID and does not need a Speaker ID record.

**Setup:**

- The account system provides a stable user ID, such as `employee-1042`.
- The account ID does not change across devices.

**Blueprint flow:**

1. Load the signed-in user's account ID.
2. Assign it directly to `UConvaiChatbotComponent.EndUserID`.
3. Call **Set End User ID** on `UConvaiPlayerComponent` with the same value.
4. Set `EndUserMetadata` on the chatbot component and call **Set End User Metadata** on `UConvaiPlayerComponent` with the same JSON string, such as:

```json
{"name": "Jordan Kim", "department": "Facilities"}
```

5. Call `StartSession`.

**Expected outcome:** Memory follows the account identity instead of the local device.

## Fresh start for a new scenario attempt

A learner repeats an assessment and should begin a fresh conversation, while keeping the same long-term identity.

**Setup:**

- The learner keeps the same `SpeakerID` or account ID.
- The project should not resume the previous conversation session.

**Blueprint flow:**

{% tabs %}
{% tab title="Blueprint" %}
Call **Reset Conversation** on the **Convai Chatbot** component, then call `StartSession`.
{% endtab %}

{% tab title="C++" %}
```cpp
// Illustrative — replace ChatbotComponent with your project's chatbot reference.
ChatbotComponent->ResetConversation();
ChatbotComponent->StartSession();
```
{% endtab %}
{% endtabs %}

**Expected outcome:** The next connection starts from a fresh local conversation link. The player's identity remains the same, so character-level long-term memory can continue to accumulate for that user.

## Remove a test identity

During development, remove test identities created by repeated Speaker ID experiments.

**Blueprint flow:**

1. Call **Convai List Speaker IDs**.
2. Find the test `SpeakerID`.
3. Call **Convai Delete Speaker ID** with that value.
4. Clear the local saved `SpeakerID`.

{% hint style="danger" %}
Deleting a Speaker ID removes the user record and associated long-term memory records for that user across characters. Use this for confirmed test data or user-requested deletion flows.
{% endhint %}

**Expected outcome:** The test `SpeakerID` is removed from Convai and the local saved identity is cleared.

## Next steps

{% content-ref url="end-user-identity.md" %}
[End-user identity](end-user-identity.md)
{% endcontent-ref %}

{% content-ref url="speaker-id-management.md" %}
[Speaker ID management](speaker-id-management.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot long-term memory](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}

{% content-ref url="ltm-blueprint-reference.md" %}
[LTM Blueprint reference](ltm-blueprint-reference.md)
{% endcontent-ref %}
