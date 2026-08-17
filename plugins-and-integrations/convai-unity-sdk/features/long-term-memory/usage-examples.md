---
title: Long-term memory usage examples
description: Four complete long-term memory patterns for Unity — zero-config persistence, authenticated identity, memory seeding, and memory reset.
last_reviewed: "4.5.0"
---

These examples cover four common long-term memory integration patterns. The code is source-checked against Unity SDK 4.5. Extraction, recall, deduplication, and deletion outcomes still require live backend verification.

## Pattern 1 — Zero-config persistence

Use `DeviceEndUserIdProvider` (the SDK default) when you do not need per-account memory. No code is required. Enable LTM on the dashboard and the SDK handles identity and storage automatically.

**When to use:** Consumer applications without user accounts, rapid prototypes, or editor-based testing.

**Limitations:** The default identity is environment-specific. The Editor uses a PlayerPrefs GUID. A player build prefers `SystemInfo.deviceUniqueIdentifier` and falls back to a PlayerPrefs GUID only when that value is invalid. Device-ID stability is platform-dependent, so use account identity for cross-device or reinstall continuity.

**Setup:**

1. Sign in at [convai.com](https://convai.com), open the character, and toggle **Long-Term Memory** to **On** in the **Memory** tab.
2. Add `ConvaiManager` and `ConvaiCharacter` to your scene with the character ID configured.
3. Enter Play Mode and have a conversation, then stop Play Mode to end the client session.
4. Re-enter Play Mode and run a live recall check after the backend's expected processing window.

No `IEndUserIdentityProvider` registration is needed. The SDK uses `DeviceEndUserIdProvider` by default.

**Live validation:** In the Editor, confirm that `PlayerPrefs["convai.end_user_id"]` stays unchanged between runs, then check whether the second session recalls the expected fact.

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

Disable automatic connection, then register the provider in `Start()` before your application calls `ConnectAsync()`:

```csharp
using Convai.Runtime.Components;
using UnityEngine;

public class IdentityRegistrar : MonoBehaviour
{
    [SerializeField] private ConvaiManager _convaiManager;
    [SerializeField] private string _accountId;
    [SerializeField] private string _displayName;

    private void Start()
    {
        if (_convaiManager == null || string.IsNullOrWhiteSpace(_accountId))
        {
            Debug.LogError("Assign a ConvaiManager and a stable account ID.");
            return;
        }

        _convaiManager.SetEndUserIdentityProvider(
            new AccountIdentityProvider(_accountId));
        _convaiManager.SetEndUserMetadataProvider(
            new AccountMetadataProvider(_displayName));
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

**Live validation:** Confirm that both devices send the same account ID, then query the end-user record and run a second-session recall check. Confirm that the backend returns the `"name"` metadata before relying on the editor label.

***

## Pattern 3 — Memory seeding before a first session

Pre-load facts for a user before their first conversation so the character can reference completed modules, certifications, or onboarding status from the start.

{% hint style="danger" %}
**Do not ship this pattern in a player-facing build.** `ConvaiRestClient` requires your API key. Embedding an API key in a distributed application exposes it to extraction. Run memory seeding from a server-side service or editor tool only.
{% endhint %}

```csharp
using Convai.RestAPI;
using Convai.Runtime;
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

**Live validation:** Query the records returned by `AddAsync`, then start a staging conversation and check whether the service recalls the seeded facts. Deduplication and conversational use are backend behavior.

***

## Pattern 4 — Reset a user's memory

Clear all stored facts for a user–character pair, then optionally disable LTM. Use this when a user's records are stale or when resetting between test sessions.

```csharp
using Convai.RestAPI;
using Convai.Runtime;
using UnityEngine;

public class MemoryReset : MonoBehaviour
{
    [ContextMenu("Purge Memories Then Disable LTM")]
    private async void PurgeAndDisable()
    {
        string characterId = "your-character-id";
        string endUserId = "target-end-user-id";

        using var client = new ConvaiRestClient(ConvaiSettings.Instance.ApiKey);

        // Step 1: Request deletion for this user-character pair
        await client.Memory.DeleteAllAsync(characterId, endUserId);
        Debug.Log("Memory deletion request completed.");

        // Step 2: Disable LTM on the character
        await client.Characters.SetMemoryEnabledAsync(characterId, false);
        Debug.Log("Long-term memory disabled.");
    }
}
```

To request deletion for the user-character pair while keeping LTM enabled, call `DeleteAllAsync` without `SetMemoryEnabledAsync`. `client.EndUsers.DeleteAsync(endUserId)` addresses an end-user record instead. Verify actual deletion scope and completion with follow-up live queries. See [Manage end-user records](end-user-management.md).

**Live validation:** List records after the request and start another staging session. Do not promise an empty conversational context until both checks confirm the backend outcome.

***

## Next steps

{% content-ref url="memory-management-api.md" %}
[Memory management API](memory-management-api.md)
{% endcontent-ref %}

{% content-ref url="long-term-memory-scripting-reference.md" %}
[Long-term memory scripting reference](long-term-memory-scripting-reference.md)
{% endcontent-ref %}
