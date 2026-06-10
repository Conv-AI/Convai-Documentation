---
title: Long-term memory usage examples
description: Apply Unreal long-term memory patterns for returning learners, shared devices, first sessions, and fresh-start reset flows.
last_reviewed: "4.0.0-beta.21"
---

Use these patterns after [Long-term memory quick start](long-term-memory-quick-start.md) is working. Each example focuses on which identity values to set on the chatbot component before `StartSession`. For assignment steps, see [End-user identity](end-user-identity.md).

## Returning learner in a training simulation

A safety training simulation should remember that a learner has already completed a valve inspection module.

**Setup:**

- LTM is enabled for the training character.
- The learner has a saved `SpeakerID`.

**Blueprint flow:**

1. Load `SpeakerID` from the learner's `SaveGame` or account profile.
2. Set `UConvaiChatbotComponent.EndUserID` and `UConvaiPlayerComponent.EndUserID` to the saved value.
3. Call `StartSession` on the chatbot component.

**Expected outcome:** The character can refer to facts learned in earlier sessions for the same learner and character.

## First-time player profile

A new player starts the application with no stored identity.

**Setup:**

- The project has collected a display name, such as `Alex`.
- No saved `SpeakerID` exists for the profile.

**Blueprint flow:**

1. Call **Convai Create Speaker ID** with **Speaker Name** set to the display name.
2. On **On Success**, save the returned `SpeakerID`.
3. Set both components' `EndUserID` to the saved value.
4. Call `StartSession`.

For the full create workflow, see [Speaker ID management](speaker-id-management.md).

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
2. Set `UConvaiChatbotComponent.EndUserID` and `UConvaiPlayerComponent.EndUserID` to the account ID.
3. Optionally set `EndUserMetadata` on both components with the same JSON string:

```json
{"name": "Jordan Kim", "department": "Facilities"}
```

4. Call `StartSession`.

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

{% content-ref url="troubleshoot-long-term-memory.md" %}
[Troubleshoot long-term memory](troubleshoot-long-term-memory.md)
{% endcontent-ref %}

{% content-ref url="ltm-blueprint-reference.md" %}
[LTM Blueprint reference](ltm-blueprint-reference.md)
{% endcontent-ref %}
