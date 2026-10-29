---
title: Long-term memory quick start
description: Enable memory for a test character, verify the identity sent by Unity, and inspect returned memories before testing recall in another session.
last_reviewed: "5.0.0-preview"
---

We will enable memory for a test character, check the connection's end-user identity, and inspect the returned records before trying another conversation. A successful response from a character alone does not establish that a specific memory was saved.

## Prerequisites

- A working Convai scene with `ConvaiManager` and a `ConvaiCharacter` whose **Character ID** is configured.
- Credentials authorized to manage that test character.
- A stable identity source. The default `DeviceEndUserIdProvider` uses a persisted identifier in the Editor; account-based applications should [supply their own identity](end-user-identity.md).

## Enable memory for a character

{% stepper %}
{% step %}
### Enable Long-Term Memory in the Inspector

Select the character and open **Memory**. Turn on **Long-Term Memory**, then confirm the change for the test character. Leave **End-User ID** on **Required** for this walkthrough.

The [settings guide](configure-end-user-id-requirement.md) shows the controls. Changes affect every application using that character, so use a separate character for this test.
{% endstep %}
{% step %}
### Check the connected identity

Enter Play mode, wait for the connection, and select `ConvaiManager`. In its **Live** section, **End User** should show an ID rather than `None`, and **Memory** should read `On for this conversation`. `Off: no end-user ID was sent` means the identity is missing; fix it before continuing. `Not reported (memory off, or a multi-character room)` needs a direct settings and records check.

Use **Copy End-User ID** only in your private debugging workflow. Do not include the identifier in screenshots or shared logs.
{% endstep %}
{% step %}
### Share a test fact and inspect records

Tell the character a non-sensitive test fact, such as `My name is Jordan, and I work the night shift.` Then choose **See What They Remember** in the manager's **Live** section, which offers it while connected when an end-user ID was sent and the addressed character has a Character ID, or choose **Convai > Convai Editor**, then select **Long Term Memory** and select the same character and end user.

Choose **Refresh** in the **Memories** pane and inspect the returned records. A record may not appear immediately. Do not stop Play mode on the assumption that stopping triggers extraction.
{% endstep %}
{% step %}
### Reconnect with the same identity

Stop and restart Play mode. Confirm that the identity matches the previous connection, then ask about the test fact without restating it. Compare the response with the records you inspected.
{% endstep %}
{% endstepper %}

## Verify the result

The setup check is complete when the character setting is enabled, the intended end-user identity reaches the connection, and the memory list returns the expected test record. Test recall separately: a saved record and a generated answer are different observations.

If the record is absent, use [Troubleshoot long-term memory](troubleshooting-and-diagnostics.md). Do not treat a delayed list update or a single answer as evidence that the whole memory pipeline is working or broken.

## Identity in the Editor and player builds

| Context | Default identity source |
|---|---|
| Unity Editor | A GUID stored under `convai.end_user_id` in `PlayerPrefs` for that project/environment. |
| Player build with a usable device ID | `SystemInfo.deviceUniqueIdentifier`. |
| Player build without a usable device ID | A GUID persisted in `PlayerPrefs`. |

Deleting the persisted fallback can create a different ID. Device identifiers also have platform-specific lifetimes. For identity that follows a signed-in person, use an application account ID rather than relying on installation or device behavior.

## Next steps

{% content-ref url="long-term-memory-window.md" %}
[Inspect and manage long-term memories](long-term-memory-window.md)
{% endcontent-ref %}

{% content-ref url="end-user-identity.md" %}
[End-user identity](end-user-identity.md)
{% endcontent-ref %}
