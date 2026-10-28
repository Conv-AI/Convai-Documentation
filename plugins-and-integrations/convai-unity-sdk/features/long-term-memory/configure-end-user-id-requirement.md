---
title: Configure the end-user ID requirement
description: Choose whether a memory-enabled character requires an end-user identity, preserve its other settings, and check the next connection result.
last_reviewed: "5.0.0-preview"
---

Set **End-User ID** in the character's **Memory** section to declare whether a memory-enabled connection requires an end-user identifier. The setting belongs to the character on Convai and applies across its versions.

## Prerequisites

- Configure the character and [enable its memory](configure-memory-for-a-character.md).
- Decide which [identity provider](end-user-identity.md) your application uses.
- Use an account authorized to edit the character.

## Choose the requirement

The SDK exposes the following contract:

| Choice | Meaning |
|---|---|
| **Required** | A memory-enabled connect without an end-user ID can be refused with `connection.connect_end_user_id_required`. |
| **Optional** | A connect without an end-user ID can proceed without memory. When the service reports that outcome, the SDK exposes `SkippedNoEndUser`. |

A missing or unrecognized stored mode is interpreted as `Required` by the SDK. A successful connection alone does not prove that memory is active.

{% stepper %}
{% step %}
### Open Memory in the character Inspector

Select the GameObject containing `ConvaiCharacter` and expand **Memory**. Wait for the saved character settings to load.
{% endstep %}
{% step %}
### Select Required or Optional

Set **End-User ID** to the intended choice. Confirm the dialog after checking the character ID. The change affects every application that uses the character.
{% endstep %}
{% step %}
### Reconnect and inspect the result

Start a fresh connection with the intended identity source. On `ConvaiManager`, check **End User** and **Memory**. If the connect is refused, use the exact error code to diagnose the cause.
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
**Screenshot required before publishing:** Capture the preview SDK's `ConvaiCharacter` Inspector with **Memory**, **Long-Term Memory**, and **End-User ID** visible. Show **Required** and the neighboring **Optional** choice without exposing account identifiers.
{% endhint %}

<figure><img src="../../../../.gitbook/assets/TODO-unity-character-memory-settings.png" alt="Character Inspector Memory section showing Long-Term Memory and the Required and Optional end-user ID choices"><figcaption><p>TODO: Character memory settings and the end-user ID requirement.</p></figcaption></figure>

## Set the requirement from a script

In a trusted administrative tool, pass the requirement to `UpdateSettingsAsync`. Omitted settings are preserved:

```csharp
using System.Threading;
using System.Threading.Tasks;
using Convai.RestAPI;
using Convai.RestAPI.Internal;

public static class EndUserRequirementSettings
{
    public static Task<MemorySettings> RequireIdentityAsync(
        ConvaiRestClient client,
        string characterId,
        CancellationToken cancellationToken = default)
    {
        return client.Memory.UpdateSettingsAsync(
            characterId,
            endUserIdRequirement: EndUserIdRequirement.Required,
            cancellationToken: cancellationToken);
    }
}
```

Read the settings again with `GetSettingsAsync` and check `EndUserIdRequirement`. Do not publish an account API key in a player build to run this administrative operation.

## Troubleshooting

| Symptom | Cause to check | Fix and verification |
|---|---|---|
| `connection.connect_end_user_id_required` | No identity reached a connect that requires it | Set a nonblank ID before connecting, then reconnect and check the reported **End User**. |
| `SkippedNoEndUser` | The connection proceeded without an end-user ID | Supply a stable identity if memory is needed; check the next response rather than the previous connection. |
| `NotReported` | The response contains no memory status | Check settings and records directly; multi-character and group responses can omit this status. |

## Next steps

{% content-ref url="end-user-identity.md" %}
[End-user identity](end-user-identity.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting-and-diagnostics.md" %}
[Troubleshoot long-term memory](troubleshooting-and-diagnostics.md)
{% endcontent-ref %}
