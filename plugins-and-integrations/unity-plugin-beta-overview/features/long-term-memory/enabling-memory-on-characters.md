---
description: >-
  Enable or disable Long-Term Memory per character using the Convai dashboard or
  the CharacterService scripting API. Off by default — opt in explicitly.
---

# Enabling Memory on Characters

## Enabling and Disabling Memory on a Character

Long-Term Memory is an opt-in capability controlled at the character level. A character with memory disabled will not accumulate or recall any facts, regardless of how many sessions it participates in. This page explains how to toggle memory on or off — via the Convai dashboard for the typical workflow, or via the `CharacterService` scripting API when you need programmatic control.

## Memory Is Off by Default

Every character starts with memory disabled (`MemorySettings.IsEnabled = false`). Nothing is stored or retrieved until you explicitly enable it. This default is intentional: memory changes the character's behaviour in ways that may not suit every deployment, and enabling it affects all sessions for that character globally — not just one scene or build.

{% hint style="warning" %}
Memory settings are **character-scoped, not project-scoped**. Enabling memory for a character affects every application, SDK version, and deployment that connects to that character ID. If the character is shared across multiple projects or teams, coordinate before enabling.
{% endhint %}

## Enabling via the Convai Dashboard

The recommended approach for most projects is to enable memory through the character settings page on the Convai dashboard. No code is required, and the change takes effect immediately for all subsequent sessions. For a detailed walkthrough of the dashboard UI, see the [Memory Settings documentation](https://docs.convai.com/api-docs/convai-playground/character-customization/memory#memory-settings).

{% stepper %}
{% step %}
**Open your character in the Convai dashboard**

Sign in at [convai.com](https://convai.com) and select the character you want to configure.
{% endstep %}

{% step %}
**Navigate to Memory Settings**

In the character editor, select the **Memory** section from the left panel, then open the **Memory Settings** tab.
{% endstep %}

{% step %}
**Enable Long-Term Memory**

Toggle **Long-Term Memory** on. The change is applied server-side immediately — no SDK update or recompile required.
{% endstep %}
{% endstepper %}

## Enabling via the Scripting API

Use `CharacterService` when you need to enable or disable memory from code — for example, during an editor tool, an admin script, or an automated test suite.

### Setting Up ConvaiRestClient

All programmatic character operations go through `ConvaiRestClient`, which must be authenticated with your API key.

```csharp
using System;
using Convai.RestAPI;
using UnityEngine;

public class MemoryConfigurator : MonoBehaviour
{
    private ConvaiRestClient _client;

    private void Awake()
    {
        _client = new ConvaiRestClient(ConvaiSettings.Instance.ApiKey);
    }

    private void OnDestroy()
    {
        _client?.Dispose();
    }
}
```

{% hint style="info" %}
`ConvaiSettings` is the ScriptableObject that stores your project's Convai API key. Configure it once under **Tools → Convai → Configuration**. `ConvaiSettings.Instance` loads it at runtime from the `Resources` folder automatically.
{% endhint %}

{% hint style="info" %}
`ConvaiRestClient` implements `IDisposable`. Always dispose it when you are finished, or manage it as a long-lived singleton rather than creating a new instance per call.
{% endhint %}

{% hint style="info" %}
**Finding your Character ID:** The character ID is the value in the **Character ID** field on your `ConvaiCharacter` component in the Inspector. It also appears on the character's page in the [Convai dashboard](https://convai.com).
{% endhint %}

### Checking Whether Memory Is Enabled

```csharp
using System;
using System.Threading;
using UnityEngine;

public async void CheckMemoryState(string characterId)
{
    try
    {
        bool isEnabled = await _client.Characters.GetMemoryEnabledAsync(characterId);
        Debug.Log($"Memory enabled for {characterId}: {isEnabled}");
    }
    catch (Exception e)
    {
        Debug.LogError($"[LTM] Failed to read memory state: {e.Message}");
    }
}
```

`GetMemoryEnabledAsync` reads the `memory_settings.enabled` flag from the character record. It returns `false` when the character has never had memory configured, matching the default state.

### Enabling Memory

```csharp
public async void EnableMemory(string characterId, CancellationToken cancellationToken = default)
{
    try
    {
        await _client.Characters.SetMemoryEnabledAsync(characterId, enabled: true, cancellationToken);
        Debug.Log($"Memory enabled for character {characterId}.");
    }
    catch (Exception e)
    {
        Debug.LogError($"[LTM] Failed to enable memory: {e.Message}");
    }
}
```

### Disabling Memory

```csharp
public async void DisableMemory(string characterId, CancellationToken cancellationToken = default)
{
    try
    {
        await _client.Characters.SetMemoryEnabledAsync(characterId, enabled: false, cancellationToken);
        Debug.Log($"Memory disabled for character {characterId}.");
    }
    catch (Exception e)
    {
        Debug.LogError($"[LTM] Failed to disable memory: {e.Message}");
    }
}
```

{% hint style="warning" %}
Disabling memory does **not** delete the stored memories. Existing memory records remain in the partition and will be recalled if memory is re-enabled later. To remove all stored memories for a specific user before disabling, call `MemoryService.DeleteAllAsync` first.
{% endhint %}

## API Reference

All methods are on `ConvaiRestClient.Characters` (`CharacterService`).

| Method                  | Signature                                                            | Returns      |
| ----------------------- | -------------------------------------------------------------------- | ------------ |
| `GetMemoryEnabledAsync` | `(string characterId, CancellationToken ct = default)`               | `Task<bool>` |
| `SetMemoryEnabledAsync` | `(string characterId, bool enabled, CancellationToken ct = default)` | `Task`       |

## Conclusion

Memory is controlled at the character level and is off by default. Enable it through the Convai dashboard for the simplest workflow, or use `CharacterService` when you need to toggle it from code. Once memory is enabled, the SDK accumulates facts automatically during every session. The next page, [Memory Management API](memory-management-api.md), covers how to read, add, and delete individual memory records programmatically.
