---
description: >-
  Toggle Long-Term Memory on or off per character via the Convai dashboard or
  the CharacterService scripting API, and understand the global scope
  implications.
---

# Enabling Memory on Characters

## Control Which Characters Remember Users

Long-Term Memory is disabled by default (`MemorySettings.IsEnabled = false`). No facts are extracted or stored until you explicitly enable it. You can enable or disable memory through the Convai dashboard or programmatically via `client.Characters`.

{% hint style="danger" %}
**Memory settings apply globally to the character.** Enabling LTM for a character affects every application, SDK version, and deployment that connects to that character ID. If you share a character across development, staging, and production environments, enabling memory in one environment enables it in all of them. Coordinate with your team before enabling on a shared character.
{% endhint %}

***

## Configuration Methods

{% tabs %}
{% tab title="Dashboard" %}
### Enable on the Convai Dashboard

This is the recommended approach for most teams. Changes take effect immediately without requiring a code update or redeployment.

1. Sign in at [convai.com](https://convai.com/).
2. Open the character you want to configure.
3. Select the **Memory** tab in the character's settings sidebar.
4. Toggle **Long-Term Memory** to **On**.
5. Click **Save**.

To disable, repeat the same steps and toggle **Long-Term Memory** to **Off**.
{% endtab %}

{% tab title="Scripting" %}
### Enable via Scripting API

Use `client.Characters` when you need programmatic control — for example, in automated test setups, build pipelines, or runtime admin panels.

#### Check Current State

```csharp
using Convai.RestAPI;
using UnityEngine;

public class MemoryAdmin : MonoBehaviour
{
    private async void Start()
    {
        using var client = new ConvaiRestClient(ConvaiSettings.Instance.ApiKey);

        bool isEnabled = await client.Characters.GetMemoryEnabledAsync("your-character-id");
        Debug.Log($"LTM enabled: {isEnabled}");
    }
}
```

#### Enable Memory

```csharp
using Convai.RestAPI;
using UnityEngine;

public class MemoryAdmin : MonoBehaviour
{
    private async void Start()
    {
        using var client = new ConvaiRestClient(ConvaiSettings.Instance.ApiKey);

        await client.Characters.SetMemoryEnabledAsync("your-character-id", true);
        Debug.Log("Long-Term Memory enabled.");
    }
}
```

#### Disable Memory

```csharp
await client.Characters.SetMemoryEnabledAsync("your-character-id", false);
```
{% endtab %}
{% endtabs %}

***

## Disabling Memory Without Losing Stored Records

{% hint style="warning" %}
Disabling LTM stops new memories from being extracted, but **does not delete existing memory records**. The stored facts remain on Convai and will be re-injected if you re-enable LTM later.

If you want to disable LTM and remove all stored memories, delete the memories first, then disable.
{% endhint %}

To purge all memories for a user–character pair before disabling:

```csharp
using Convai.RestAPI;
using UnityEngine;

public class MemoryReset : MonoBehaviour
{
    [ContextMenu("Purge Memories Then Disable LTM")]
    private async void PurgeAndDisable()
    {
        string characterId = "your-character-id";
        string endUserId = "target-end-user-id";

        using var client = new ConvaiRestClient(ConvaiSettings.Instance.ApiKey);

        // Step 1: Delete all memories for this user–character pair
        await client.Memory.DeleteAllAsync(characterId, endUserId);
        Debug.Log("Memories purged.");

        // Step 2: Disable LTM on the character
        await client.Characters.SetMemoryEnabledAsync(characterId, false);
        Debug.Log("Long-Term Memory disabled.");
    }
}
```

{% hint style="info" %}
`DeleteAllAsync` removes memories for one specific user–character pair. If you need to remove all end-user records across all characters, use `client.EndUsers.DeleteAsync(endUserId)` instead. See [End-User Management](/broken/pages/d6b753fe85c4019237eb5dde8bec8078bf03aa57).
{% endhint %}

***

## Next Steps

{% content-ref url="/broken/pages/8f2ffbc1cb1ac68edf9cb650ee6b4787d16fbd57" %}
[Broken link](/broken/pages/8f2ffbc1cb1ac68edf9cb650ee6b4787d16fbd57)
{% endcontent-ref %}

{% content-ref url="/broken/pages/d6b753fe85c4019237eb5dde8bec8078bf03aa57" %}
[Broken link](/broken/pages/d6b753fe85c4019237eb5dde8bec8078bf03aa57)
{% endcontent-ref %}
