---
title: Inspect and manage long-term memories
description: Inspect a character's memories of an end user in Unity, add test facts, request deletions, and distinguish memory removal from user deactivation.
last_reviewed: "5.0.0-preview"
---

Use the **Long Term Memory** section of **Convai Editor** to inspect records returned by Convai for one character and end user. The window also provides separate controls for memory deletion and end-user deactivation.

## Prerequisites

- Credentials authorized to manage the character and its memory records.
- A character ID and the intended end-user ID. During Play mode, **See What They Remember** on `ConvaiManager` opens this section for the addressed character and reported end user.
- Test data for evaluating edits or deletion.

## Open a character and end user

{% stepper %}
{% step %}
### Open Long Term Memory

Choose **Convai > Convai Editor** from the Unity menu, then select **Long Term Memory** in the window's navigation. It is a section of this window, not a separate top-level menu command.
{% endstep %}
{% step %}
### Choose the character

Use **Character** to choose a scene character, or use **Character ID** for another character. The summary reports its memory settings; **Edit in Inspector** opens the scene character for settings changes.
{% endstep %}
{% step %}
### Select the end user

Use **Search** to filter loaded end users. **Load More** retrieves another page of 50 end users. When offered, **Find Exact ID** looks up the entered identifier directly.

Click an end user to view their memories. Checkboxes select users for **Deactivate Selected** and are separate from the focused user whose memories you are inspecting.
{% endstep %}
{% step %}
### Inspect returned memories

Use **Refresh Memories** to reload the selected pair. **Previous** and **Next** page through memory records, with 25 records requested per page. Read the status text if a request fails; a failed load is not an empty memory store.
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
**Screenshot required before publishing:** Capture the released target version's **Long Term Memory** section with **Character**, **Search**, **Character Memories**, **End User Actions**, and **Memory Deletion Requests** visible. Use test identifiers and non-sensitive facts. The current local panel differs from the audited source, so it is not a valid replacement image.
{% endhint %}

<figure><img src="../../../../.gitbook/assets/TODO-unity-long-term-memory-window.png" alt="Long Term Memory window showing character and end-user selection, memory records, and separate deletion and deactivation controls"><figcaption><p>TODO: Audited Long Term Memory window with test data and identifiers concealed.</p></figcaption></figure>

## Add or remove individual facts

Enter a test fact in **Add memory**, then choose **Add**. Refresh the list to inspect the response rather than assuming one submitted fact creates one record.

Select memory records and use **Delete Selected** to request their deletion. Confirm the selected scope first. **Delete All with This Character** requests deletion for the focused end user and the selected character only.

{% hint style="danger" %}
Memory deletion cannot be undone through this window. Confirm the character and end user before submitting a request. A completed request is not proof that all records have disappeared; use the subsequent check.
{% endhint %}

## Forget an end user or deactivate them

The actions have different scopes:

| Action | Scope and outcome |
|---|---|
| **Delete All with This Character** | Requests deletion of one character's memories for the focused end user. |
| **Forget End User…** | Lists characters owned by the account and requests memory deletion for each. The end user stays active so the result can be checked. |
| **Deactivate End User** | Deactivates the focused end-user record. It does not request memory deletion. |
| **Deactivate Selected** | Deactivates the end users selected by checkbox. It does not request memory deletion. |

The SDK's end-user contract treats deactivation as separate from erasure. If the goal is to delete memories, request and check memory deletion before deactivating the user.

## Verify deletion requests

Under **Memory Deletion Requests**, choose **Check** to query whether memories are still listed. A forget request offers **Deactivate End User** only after its checks find none and the request has covered all owned characters without unresolved failures.

Keep the status text for partial, failed, or canceled requests in view. **Cancel** stops a forget operation between characters; it cannot retract requests already sent. An empty result describes what the API returned, not an independent audit of service storage.

## Troubleshooting

| Symptom | Cause to check | Fix and verification |
|---|---|---|
| An end user is absent from loaded rows | Only part of the list is loaded, or the search has no match | Use **Load More** or **Find Exact ID**; confirm the focused identifier privately. |
| A memory does not appear after a conversation | No record has been returned for this pair yet | Verify identity and settings, then **Refresh Memories**; do not treat stopping Play mode as an extraction command. |
| Records remain after deletion was requested | The requested result is not yet reflected in the list, or part of the request failed | Use **Check** and inspect its status before reporting completion. |
| The wrong character's records are visible | Character selection changed | Re-select the intended character and refresh before editing. |

## Next steps

{% content-ref url="memory-management-api.md" %}
[Memory management API](memory-management-api.md)
{% endcontent-ref %}

{% content-ref url="end-user-management.md" %}
[Manage end-user records](end-user-management.md)
{% endcontent-ref %}
