---
title: Long-term memory usage examples
description: Choose a memory workflow for local testing, signed-in accounts, seeded facts, or a controlled reset, using stable identities and verified results.
last_reviewed: "5.0.0-preview"
---

Choose the pattern that matches your application's identity and administration model. These examples use the 5.0 identity snapshot and memory settings API; they do not prove backend extraction, retention, or recall timing.

## Test with the default identity

For a local test, enable memory on a test character and connect without a custom identity provider. The Editor reads or creates a GUID in `PlayerPrefs["convai.end_user_id"]`. A player build uses a valid `SystemInfo.deviceUniqueIdentifier`, falling back to the saved GUID when that value is unavailable.

Reconnect with the same resolved identity. Inspect **End User** and **Memory** on `ConvaiManager` in Play mode, then use **See What They Remember** to inspect returned records. Verify recall separately with a fresh conversation. Device identifiers and preference storage have platform-specific lifetimes; use an account ID when identity must survive device or installation changes.

Follow [Long-term memory quick start](quick-start.md) for the complete test.

## Use an authenticated account

Turn off **Starts Connected** on `ConvaiRoomManager` while sign-in is pending; it also blocks each character's **Auto Connect**. After your authentication flow finishes, install a provider using `SetEndUserIdentityProvider` and, if needed, `SetEndUserMetadataProvider`; then connect. The SDK copies and validates identity and metadata for that connection attempt.

Use the complete `AccountIdentityInstaller` example in [End-user identity](end-user-identity.md). Your authentication layer supplies the actual account identifier. Do not generate a fresh ID per scene load or treat the room's participant `PlayerID` as the memory identity.

If the user signs out or changes accounts, disconnect and establish the next connection using the new provider values. Changing a provider does not migrate stored memory records.

## Seed a test user's facts

Call `client.Memory.AddAsync` from a trusted administrative tool, using the intended character and end-user pair. Inspect the result and list records again before testing the conversation. The complete helper in [Memory management API](memory-management-api.md#add-and-retrieve-facts) adds a test onboarding fact without exposing account credentials in a player script.

A successful add response verifies that request's result. It does not guarantee that every later response will mention the fact or that repeated inputs will produce a specific deduplication event.

## Reset a memory test deliberately

Use this sequence when resetting a known test pair:

1. Disconnect the test session so that it is not producing further interactions during the reset.
2. Request `client.Memory.DeleteAllAsync(characterId, endUserId)`.
3. List the same pair again and check for remaining records. A request response alone is insufficient.
4. If needed, disable memory separately with `client.Memory.UpdateSettingsAsync(characterId, enabled: false)`. This does not delete records.
5. Re-enable memory and reconnect only when ready to start another test.

For all owned characters, use **Forget End User…** in the [Long Term Memory window](long-term-memory-window.md). Check each deletion request and coverage before deactivation. `client.EndUsers.DeleteAsync` deactivates an end user; it must not replace the memory-deletion steps above.

## Next steps

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot long-term memory](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
{% content-ref url="long-term-memory-scripting-reference.md" %}
[Long-term memory scripting reference](long-term-memory-scripting-reference.md)
{% endcontent-ref %}
