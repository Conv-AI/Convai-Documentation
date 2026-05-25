---
title: Long-term memory usage examples
description: Four complete long-term memory patterns for Unity — zero-config persistence, authenticated identity, memory seeding, and memory reset.
last_reviewed: "4.2.0"
---

These examples cover the four most common long-term memory integration patterns. Each example is self-contained and shows the full setup, the relevant code, and the expected runtime outcome.

## Pattern 1 — Zero-config persistence

Use `DeviceEndUserIdProvider` (the SDK default) when you do not need per-account memory. No code is required. Enable LTM on the dashboard and the SDK handles identity and storage automatically.

**When to use:** Consumer applications without user accounts, rapid prototypes, or editor-based testing.

**Limitations:** Memory is scoped to the device. Clearing `PlayerPrefs` or reinstalling the application generates a new identity — no memories carry over.

**Setup:**

1. Sign in at [convai.com](https://convai.com), open the character, and toggle **Long-Term Memory** to **On** in the **Memory** tab.
2. Add `ConvaiManager` and `ConvaiCharacter` to your scene with the character ID configured.
3. Enter Play Mode and have a conversation. Stop Play Mode to trigger memory extraction.
4. Re-enter Play Mode and verify the character recalls what was shared.

No `IEndUserIdentityProvider` registration is needed. The SDK uses `DeviceEndUserIdProvider` by default.

**Expected outcome:** The character references facts from previous sessions automatically. The same GUID in `PlayerPrefs["convai.end_user_id"]` is used each session on the same machine.

***

## Pattern 2 — Authenticated identity

Use a custom `IEndUserIdentityProvider` when users log in with accounts. This ensures memories follow a user across devices and reinstalls.

**When to use:** Applications with user authentication — enterprise training platforms, onboarding systems, consumer apps with accounts.

```csharp
using Convai.Domain.Identity;

public class AccountIdentityProvider : IEndUserIdentityProvider
{
    private readonly string _accountId;

    public AccountIdentityProvider(string accountId)
    {
        _accountId = accountId;
    }

    public string GetEndUserId()
    {
        return _accountId;
    }
}
```

Register the provider in `Awake()` before `ConvaiRoomManager.Start()` completes:

```csharp
using Convai.Runtime.Components;
using UnityEngine;

public class IdentityRegistrar : MonoBehaviour
{
    [SerializeField] private ConvaiManager _convaiManager;

    private void Awake()
    {
        string accountId = AuthService.CurrentUser.AccountId;
        _convaiManager.SetEndUserIdentityProvider(new AccountIdentityProvider(accountId));
    }
}
```

Optionally, attach a display name so the editor's Long-Term Memory panel shows a readable label instead of a raw ID:

```csharp
using System.Collections.Generic;
using Convai.Domain.Identity;

public class AccountMetadataProvider : IEndUserMetadataProvider
{
    private readonly string _displayName;

    public AccountMetadataProvider(string displayName)
    {
        _displayName = displayName;
    }

    public IReadOnlyDictionary<string, object> GetEndUserMetadata()
    {
        return new Dictionary<string, object> { { "name", _displayName } };
    }
}
```

```csharp
_convaiManager.SetEndUserMetadataProvider(
    new AccountMetadataProvider(AuthService.CurrentUser.DisplayName));
```

**Expected outcome:** Each user's memories are stored under their account ID. Memories persist across devices and reinstalls. The editor panel shows the user's display name.

***

## Pattern 3 — Memory seeding before a first session

Pre-load facts for a user before their first conversation so the character can reference completed modules, certifications, or onboarding status from the start.

{% hint style="danger" %}
**Do not ship this pattern in a player-facing build.** `ConvaiRestClient` requires your API key. Embedding an API key in a distributed application exposes it to extraction. Run memory seeding from a server-side service or editor tool only.
{% endhint %}

```csharp
using Convai.RestAPI;
using System.Collections.Generic;
using UnityEngine;

public class OnboardingMemorySeeder : MonoBehaviour
{
    // Editor-only / server-side usage only — never ship with an embedded API key
    [ContextMenu("Seed New Employee Memory")]
    private async void SeedEmployeeMemory()
    {
        string characterId = "onboarding-assistant-id";
        string employeeAccountId = "emp-00421";

        var certifications = new List<string>
        {
            "The employee completed Fire Safety Level 1 on 2025-04-10.",
            "The employee completed Hazardous Materials Handling on 2025-04-15.",
            "The employee has not yet completed Confined Space Entry certification."
        };

        using var client = new ConvaiRestClient(ConvaiSettings.Instance.ApiKey);
        var response = await client.Memory.AddAsync(characterId, employeeAccountId, certifications);

        Debug.Log($"Seeded {response.Memories.Count} memory records.");
    }
}
```

**Expected outcome:** On the employee's first conversation with the onboarding assistant, the character already knows their certification status and guides them to the next required module.

***

## Pattern 4 — Reset a user's memory

Clear all stored facts for a user–character pair, then optionally disable LTM. Use this when a user's records are stale or when resetting between test sessions.

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
        Debug.Log("Long-term memory disabled.");
    }
}
```

To remove only the memories while keeping LTM enabled, call `DeleteAllAsync` without the `SetMemoryEnabledAsync` step. To remove a user's records across all characters (not just one), use `client.EndUsers.DeleteAsync(endUserId)` instead. See [Manage end-user records](end-user-management.md).

**Expected outcome:** The next session for this user–character pair starts with no stored context. The character treats the user as a new contact.

***

## Next steps

{% content-ref url="memory-management-api.md" %}
[Memory management API](memory-management-api.md)
{% endcontent-ref %}

{% content-ref url="long-term-memory-scripting-reference.md" %}
[Long-term memory scripting reference](long-term-memory-scripting-reference.md)
{% endcontent-ref %}
