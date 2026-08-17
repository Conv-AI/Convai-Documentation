---
title: Configure memory for a character
description: Toggle Long-Term Memory on or off per character via the Convai dashboard or the CharacterService scripting API, and understand the global scope implications.
last_reviewed: "4.5.0"
---

The Unity 4.5 response model defaults `MemorySettings.IsEnabled` to `false`, and `CharacterService` exposes methods to read or change the service-side setting. You can use the Convai dashboard or `client.Characters`. Whether and when the backend extracts, recalls, retains, or deletes data must be verified with live service calls.

{% hint style="danger" %}
The request is keyed by character ID rather than by Unity scene. Treat the setting as shared across applications that use that character, coordinate before changing a shared character, and confirm the effective scope against the live backend environment.
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

{% tab title="Scripting" %}
Use `client.Characters` when you need programmatic control — for example, in automated test setups, build pipelines, or runtime admin panels.

**Check current state**

```csharp
using Convai.RestAPI;
using Convai.Runtime;
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
using Convai.Runtime;
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
// API usage excerpt: assumes an initialized client from the examples above.
await client.Characters.SetMemoryEnabledAsync("your-character-id", false);
```
{% endtab %}
{% endtabs %}

***

## Disable memory without deleting records

{% hint style="warning" %}
`SetMemoryEnabledAsync(..., false)` and the deletion methods are separate client requests. Unity SDK source does not prove how existing records are retained or later recalled after disabling. Verify that backend behavior in staging before relying on it.

If your workflow also requests deletion, send that request first, verify the live result, and then disable the character setting.
{% endhint %}

To request deletion for a user-character pair before disabling, call `client.Memory.DeleteAllAsync` and inspect the response, then call `SetMemoryEnabledAsync`. `client.EndUsers.DeleteAsync(endUserId)` addresses an end-user record instead. The request shapes are source-verified; confirm deletion scope and completion with a follow-up live query. See [Manage end-user records](end-user-management.md).

See [Long-term memory usage examples](usage-examples.md) for a complete reset pattern.

***

## Next steps

{% content-ref url="end-user-identity.md" %}
[End-user identity](end-user-identity.md)
{% endcontent-ref %}

{% content-ref url="end-user-management.md" %}
[Manage end-user records](end-user-management.md)
{% endcontent-ref %}
