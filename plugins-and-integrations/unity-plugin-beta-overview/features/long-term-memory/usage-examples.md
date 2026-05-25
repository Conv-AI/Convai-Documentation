---
description: >-
  Complete, working code for four common Long-Term Memory scenarios: automatic
  persistence, account-scoped identity, memory seeding before first session, and
  targeted resets.
---

# Usage Examples

## Long-Term Memory in Practice

This page provides complete, working code for the most common Long-Term Memory scenarios. Each example is self-contained and can be dropped into a MonoBehaviour. The scenarios use a safety training simulation context — an instructor NPC that guides trainees through procedural assessments — but the same patterns apply to any application domain.

## Example 1: Zero-Config Automatic Persistence

Long-Term Memory works out of the box for the majority of projects. No scripting is needed.

**Scenario:** A fire safety training module where the instructor character remembers each trainee's name and progress between sessions.

**What to do:**

{% stepper %}
{% step %}
**Enable memory on the character**

In the Convai dashboard, navigate to your character → **Memory → Memory Settings** → enable **Long-Term Memory**. See [Enabling Memory on Characters](enabling-memory-on-characters.md) for the full walkthrough.
{% endstep %}

{% step %}
**Set up your scene as normal**

Add `ConvaiManager` and `ConvaiCharacter` to your scene with a valid character ID. No additional components or configuration are required for Long-Term Memory.
{% endstep %}

{% step %}
**Run the simulation**

Enter Play Mode. The `DeviceEndUserIdProvider` sends a stable device identifier automatically on every session connect. After the first conversation, the backend stores whatever facts it extracted. On every subsequent session, those memories are injected before the first response.
{% endstep %}
{% endstepper %}

**There is nothing to implement.** The identity provider is registered automatically, and the session connect flow sends `end_user_id` without any additional setup.

{% hint style="info" %}
In the Unity Editor, all Play Mode sessions share one `end_user_id` — a GUID persisted in `PlayerPrefs`. Start Play Mode, converse, stop, then start again to verify that the character recalls the previous exchange.
{% endhint %}

***

## Example 2: Custom Identity Provider for Authenticated Users

**Scenario:** A corporate onboarding simulation where employees sign in with company credentials. Memories must follow the account, not the device, so the experience transfers when employees switch machines.

```csharp
using System;
using System.Collections.Generic;
using Convai.Domain.Identity;
using Convai.Runtime.Components;
using UnityEngine;

// --- Identity provider ---
// Returns the server-assigned account ID, which is stable across devices and re-logins.

public class EmployeeIdentityProvider : IEndUserIdentityProvider
{
    private readonly string _accountId;

    public EmployeeIdentityProvider(string accountId)
    {
        _accountId = accountId;
    }

    public string GetEndUserId() => _accountId;
}

// --- Metadata provider ---
// Attaches name and department to the end-user record.
// The "name" key is displayed in the editor's Long-Term Memory tab.

public class EmployeeMetadataProvider : IEndUserMetadataProvider
{
    private readonly string _name;
    private readonly string _department;

    public EmployeeMetadataProvider(string name, string department)
    {
        _name = name;
        _department = department;
    }

    public IReadOnlyDictionary<string, object> GetEndUserMetadata()
    {
        return new Dictionary<string, object>
        {
            { "name", _name },
            { "department", _department }
        };
    }
}

// --- Scene setup ---

public class OnboardingSessionSetup : MonoBehaviour
{
    [SerializeField] private ConvaiManager _convaiManager;

    // Call this after your authentication layer resolves the signed-in employee.
    // Must be called BEFORE ConvaiManager opens a session.
    public void OnEmployeeSignedIn(string accountId, string fullName, string department)
    {
        _convaiManager.SetEndUserIdentityProvider(
            new EmployeeIdentityProvider(accountId));

        _convaiManager.SetEndUserMetadataProvider(
            new EmployeeMetadataProvider(fullName, department));
    }
}
```

**Key points:**

* `SetEndUserIdentityProvider` and `SetEndUserMetadataProvider` must be called **before** the first session connect. Calling them after a session is already open has no effect until the session restarts.
* Use the server-assigned account ID from your authentication system as `accountId`. Avoid email addresses or display names — they can change.
* To read back the `end_user_id` your provider returns (for use with `MemoryService`), call `provider.GetEndUserId()` directly on the same provider instance.

***

## Example 3: Seeding Memories Before a First Session

**Scenario:** A hazardous materials assessment where the instructor character must know the trainee's prior certification history before the first conversation begins.

Rather than waiting for the AI to extract this information naturally over multiple sessions, you inject it programmatically before the trainee enters the experience.

{% hint style="danger" %}
This example calls `ConvaiRestClient` directly with your API key. **Never ship this code in a player-facing build.** The API key would be embedded in the application and could be extracted. Run memory seeding from a server-side script, an editor tool, or an admin-only build.
{% endhint %}

```csharp
using System;
using System.Collections.Generic;
using System.Threading;
using Convai.RestAPI;
using Convai.RestAPI.Internal;
using UnityEngine;

public class TraineeMemorySeeder : MonoBehaviour
{
    [SerializeField] private string _characterId;

    private ConvaiRestClient _client;

    private void Awake()
    {
        _client = new ConvaiRestClient(ConvaiSettings.Instance.ApiKey);
    }

    private void OnDestroy()
    {
        _client?.Dispose();
    }

    // Call this after authentication resolves the trainee's account ID,
    // before the trainee enters the simulation scene.
    public async void SeedTraineeHistory(
        string endUserId,
        TraineeCertificationRecord record,
        CancellationToken cancellationToken = default)
    {
        try
        {
            var facts = new List<string>
            {
                $"The trainee completed Module 1 (fire safety) with a score of {record.Module1Score}%.",
                $"The trainee answered incorrectly on fire extinguisher classification (Module 1, Question 4).",
                $"The trainee has completed {record.CompletedModules} of {record.TotalModules} required modules."
            };

            AddMemoriesResponse response = await _client.Memory.AddAsync(
                _characterId,
                endUserId,
                facts,
                metadata: null,
                cancellationToken);

            Debug.Log($"Seeded {response.Memories.Count} memory records for trainee {endUserId}.");
        }
        catch (Exception e)
        {
            Debug.LogError($"[LTM] Failed to seed memories: {e.Message}");
        }
    }
}

[System.Serializable]
public class TraineeCertificationRecord
{
    public int Module1Score;
    public int CompletedModules;
    public int TotalModules;
}
```

**Key points:**

* The `endUserId` passed here must be **identical** to what your session's identity provider returns for the same trainee. If you are using a custom provider (see Example 2), use the same account ID.
* The server deduplicates overlapping facts. If the character already has a memory about Module 1 from a previous session, the returned `Event` will be `"UPDATE"` rather than `"ADD"`.
* To get the current `end_user_id` from the default provider: `new DeviceEndUserIdProvider().GetEndUserId()` (call on the main thread).

***

## Example 4: Resetting a User for a Fresh Simulation Run

**Scenario:** A re-certification workflow where a trainee must repeat a full safety module as if for the first time. All prior memories must be cleared so the instructor does not reference previous attempts.

```csharp
using System;
using System.Threading;
using Convai.RestAPI;
using Convai.RestAPI.Internal;
using UnityEngine;

public class SimulationResetManager : MonoBehaviour
{
    [SerializeField] private string _characterId;

    private ConvaiRestClient _client;

    private void Awake()
    {
        _client = new ConvaiRestClient(ConvaiSettings.Instance.ApiKey);
    }

    private void OnDestroy()
    {
        _client?.Dispose();
    }

    // Clears all memories for this trainee on this character only.
    // The end-user record (identity and metadata) is preserved.
    public async void ResetTraineeMemory(
        string endUserId,
        CancellationToken cancellationToken = default)
    {
        try
        {
            MemoryDeleteAllResponse response = await _client.Memory.DeleteAllAsync(
                _characterId,
                endUserId,
                cancellationToken);

            Debug.Log($"Memory reset complete — user: {response.EndUserId}, character: {response.CharacterId}.");
        }
        catch (Exception e)
        {
            Debug.LogError($"[LTM] Failed to reset memory: {e.Message}");
        }
    }

    // Removes the end-user record and ALL memories across ALL characters.
    // Use only when decommissioning the trainee account entirely.
    public async void DeleteTraineeRecord(
        string endUserId,
        CancellationToken cancellationToken = default)
    {
        try
        {
            EndUserDeleteResponse response = await _client.EndUsers.DeleteAsync(
                endUserId,
                cancellationToken);

            Debug.Log($"Trainee record deleted: {response.Deleted}");
        }
        catch (Exception e)
        {
            Debug.LogError($"[LTM] Failed to delete trainee: {e.Message}");
        }
    }
}
```

**Choosing the right reset method:**

| Goal                                                          | Method                                                 |
| ------------------------------------------------------------- | ------------------------------------------------------ |
| Clear memories for this character only; preserve user record  | `MemoryService.DeleteAllAsync(characterId, endUserId)` |
| Remove the user record and all memories across all characters | `EndUsersService.DeleteAsync(endUserId)`               |

{% hint style="danger" %}
Both deletion methods are **irreversible**. The API provides no confirmation or undo. Implement a confirmation step in your application UI before calling either method.
{% endhint %}

***

## Conclusion

These four patterns cover the full range of Long-Term Memory use cases: automatic persistence with no code, account-scoped identity for authenticated users, programmatic memory seeding before first contact, and targeted resets for re-running experiences. If something is not working as expected, see [Troubleshooting & Diagnostics ](troubleshooting-and-diagnostics.md)for a step-by-step diagnostic guide.
