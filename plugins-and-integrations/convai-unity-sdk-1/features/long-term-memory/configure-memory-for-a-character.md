---
title: Configure memory for a character
description: Toggle Long-Term Memory on or off per character via the Convai dashboard or the CharacterService scripting API, and understand the global scope implications.
last_reviewed: "4.2.0"
---

Long-term memory is disabled by default (`MemorySettings.IsEnabled = false`). No facts are extracted or stored until you explicitly enable it. You can enable or disable memory through the Convai dashboard or programmatically via `client.Characters`.

{% hint style="danger" %}
**Memory settings apply globally to the character.** Enabling LTM for a character affects every application, SDK version, and deployment that connects to that character ID. If you share a character across development, staging, and production environments, enabling memory in one environment enables it in all of them. Coordinate with your team before enabling on a shared character.
{% endhint %}

***

## Enable or disable memory

{% tabs %}
{% tab title="Dashboard" %}
This is the recommended approach for most teams. Changes take effect immediately without requiring a code update or redeployment.

1. Sign in at [convai.com](<code class="expression">space.vars.dashboard_url</code>).
2. Open the character you want to configure.
3. Select the **Memory** tab in the character's settings sidebar.
4. Toggle **Long-Term Memory** to **On**.
5. Click **Save**.

To disable, repeat the same steps and toggle **Long-Term Memory** to **Off**.
{% endtab %}

{% tab title="Scripting" %}
Use `client.Characters` when you need programmatic control — for example, in automated test setups, build pipelines, or runtime admin panels.

**Check current state**

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

**Enable memory**

```csharp
using Convai.RestAPI;
using UnityEngine;

public class MemoryAdmin : MonoBehaviour
{
    private async void Start()
    {
        using var client = new ConvaiRestClient(ConvaiSettings.Instance.ApiKey);

        await client.Characters.SetMemoryEnabledAsync("your-character-id", true);
        Debug.Log("Long-term memory enabled.");
    }
}
```

**Disable memory**

```csharp
await client.Characters.SetMemoryEnabledAsync("your-character-id", false);
```
{% endtab %}
{% endtabs %}

***

## Disable memory without deleting records

{% hint style="warning" %}
Disabling LTM stops new memories from being extracted, but **does not delete existing memory records**. The stored facts remain on Convai and will be re-injected if you re-enable LTM later.

If you want to disable LTM and remove all stored memories, delete the memories first, then disable.
{% endhint %}

To purge all memories for a user–character pair before disabling, use `client.Memory.DeleteAllAsync` followed by `SetMemoryEnabledAsync`. `DeleteAllAsync` removes memories for one specific user–character pair. To remove all end-user records across all characters instead, use `client.EndUsers.DeleteAsync(endUserId)`. See [Manage end-user records](end-user-management.md).

See [Long-term memory usage examples](usage-examples.md) for a complete reset pattern.

***

## Next steps

{% content-ref url="end-user-identity.md" %}
[End-user identity](end-user-identity.md)
{% endcontent-ref %}

{% content-ref url="end-user-management.md" %}
[Manage end-user records](end-user-management.md)
{% endcontent-ref %}
