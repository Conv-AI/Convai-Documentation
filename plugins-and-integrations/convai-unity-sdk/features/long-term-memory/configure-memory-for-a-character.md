---
title: Configure memory for a character
description: Explains how to turn long-term memory on or off for a character from the dashboard or from script, and what its global scope means for shared characters.
last_reviewed: "4.6.0"
---

Long-term memory is disabled by default (`MemorySettings.IsEnabled = false`). No facts are extracted or stored until you explicitly enable it. You can enable or disable memory through the Convai dashboard, the Unity Inspector (SDK 5.0), or a script.

A second setting, the end-user ID requirement, decides what happens when a connect sends no end-user ID while memory is on. **Required** is the default: the connect is refused with HTTP 400 ("Missing end_user_id"). **Optional** lets the connect through, but nothing from that conversation is remembered. The SDK sends a device-based end-user ID by default, so this only matters when your identity provider can return nothing.

{% hint style="danger" %}
**Memory settings apply globally to the character.** Enabling LTM for a character affects every application, SDK version, and deployment that connects to that character ID. If you share a character across development, staging, and production environments, enabling memory in one environment enables it in all of them. Coordinate with your team before enabling on a shared character.
{% endhint %}

***

## Enable or disable memory

{% tabs %}
{% tab title="Dashboard" %}
This is the recommended approach for most teams. Changes take effect immediately without requiring a code update or redeployment.

1. Sign in at [convai.com](https://convai.com).
2. Open the character you want to configure.
3. Select the **Memory** tab in the character's settings sidebar.
4. Toggle **Long-Term Memory** to **On**.
5. Click **Save**.

To disable, repeat the same steps and toggle **Long-Term Memory** to **Off**.
{% endtab %}

{% tab title="Inspector" %}
{% hint style="info" %}
Requires Convai Unity SDK 5.0.
{% endhint %}

Select the GameObject with the **Convai Character** component and open its **Memory** section. It needs an API key in **Project Settings → Convai SDK**.

1. Turn on **Long-Term Memory**. The Inspector asks you to confirm, because the change applies to every app that uses the character.
2. Choose **End-User ID**: **Required** or **Optional**.

**Manage Memories…** opens the Long Term Memory panel for this character. In Play Mode, the **Convai Manager** Inspector shows the end user the service confirmed and whether this conversation is remembered, and **See What They Remember** opens the panel for the character you are talking to.
{% endtab %}

{% tab title="Scripting" %}
{% hint style="info" %}
Requires Convai Unity SDK 5.0.
{% endhint %}

Use `client.Memory` when you need programmatic control, for example in automated test setups, build pipelines, or admin tools. `UpdateSettingsAsync` changes only what you pass and keeps the character's other memory settings.

```csharp
using Convai.RestAPI;
using Convai.RestAPI.Internal;
using UnityEngine;

public class MemoryAdmin : MonoBehaviour
{
    private async void Start()
    {
        using var client = new ConvaiRestClient(ConvaiSettings.Instance.ApiKey);

        MemorySettings current = await client.Memory.GetSettingsAsync("your-character-id");
        Debug.Log($"LTM enabled: {current.IsEnabled}, end-user ID: {current.EndUserIdRequirement}");

        MemorySettings updated = await client.Memory.UpdateSettingsAsync(
            "your-character-id",
            enabled: true,
            endUserIdRequirement: EndUserIdRequirement.Optional);
        Debug.Log($"LTM enabled: {updated.IsEnabled}");
    }
}
```

Pass only `enabled` to switch memory on or off, or only `endUserIdRequirement` to change the requirement.

**SDK 4.x.** `client.Characters.GetMemoryEnabledAsync` and `SetMemoryEnabledAsync` read and set the on/off switch. `ConvaiRestClient.Characters` is marked `[Obsolete]`, so this code compiles with a `CS0618` warning. In 4.x, `SetMemoryEnabledAsync` also resets the end-user ID requirement to Required; if you use Optional, set it again on the dashboard after calling it. In SDK 5.0 both methods are obsolete and keep the other settings.

```csharp
bool isEnabled = await client.Characters.GetMemoryEnabledAsync("your-character-id");
await client.Characters.SetMemoryEnabledAsync("your-character-id", true);
```
{% endtab %}
{% endtabs %}

***

## Characters on a pinned version

A character that connects through a pinned version (in SDK 5.0, **Character Version** set to a specific release) takes memory on or off from that version's saved settings. Switching memory on or off for the character doesn't change a pinned version. The end-user ID requirement is read from the live character, so it applies to every version at once.

***

## Disable memory without deleting records

{% hint style="warning" %}
Disabling LTM stops new memories from being extracted, but **does not delete existing memory records**. The stored facts remain on Convai and will be re-injected if you re-enable LTM later.

If you want to disable LTM and remove all stored memories, delete the memories first, then disable.
{% endhint %}

To purge all memories for a user–character pair before disabling, use `client.Memory.DeleteAllAsync`, then turn memory off. `DeleteAllAsync` removes memories for one user–character pair. `client.EndUsers.DeleteAsync(endUserId)` deactivates the end user but leaves their memories stored, so run `DeleteAllAsync` for each character first. See [Manage end-user records](end-user-management.md).

See [Long-term memory usage examples](usage-examples.md) for a complete reset pattern.

***

## Next steps

{% content-ref url="end-user-identity.md" %}
[End-user identity](end-user-identity.md)
{% endcontent-ref %}

{% content-ref url="end-user-management.md" %}
[Manage end-user records](end-user-management.md)
{% endcontent-ref %}
