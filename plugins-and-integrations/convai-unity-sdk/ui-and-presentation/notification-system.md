# notification system

The notification system displays transient, toast-style popups in your scene. It handles session error alerts automatically — when Convai reports a connection or authentication error, the system maps the error code to a notification asset and queues it for display. You can also trigger custom notifications from code at any point during a session.

Up to three notifications can appear on screen simultaneously. Additional notifications queue and display as space becomes available.

***

## System Overview

```mermaid
graph TD
    A[IConvaiNotificationService] -->|RequestNotification| B[NotificationHandler]
    B -->|resolves via SONotificationGroup| C[UINotificationController]
    C -->|pool of 3| D[UINotification]
    E[Session error] -->|SONotificationErrorMap| A
    F[Your script] -->|RequestNotification| A
    G[Runtime settings\nNotificationsEnabled=false] -->|RuntimeSettingsNotificationApplier| A
```

`IConvaiNotificationService` is the single entry point for all notification requests. `NotificationHandler` resolves the notification asset by ID using `SONotificationGroup`, then passes it to `UINotificationController`, which manages a pool of reusable `UINotification` elements. Session errors are routed through `SONotificationErrorMap` to map error codes to notification assets automatically.

***

## `SONotification` — Notification Asset

Each notification is a ScriptableObject asset containing the content to display.

**Create:** Right-click in the Project window → **Create → Convai → Notification System → Notification**

| Field                 | Description                                                                                                      |
| --------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `icon`                | `Sprite` shown in the notification icon slot. Optional — leave empty for no icon                                 |
| `notificationTitle`   | Title text shown in bold                                                                                         |
| `notificationMessage` | Body text. Supports multi-line content                                                                           |
| `Id`                  | Stable string identifier used for error mapping and deduplication cooldowns. Defaults to the asset name if empty |

**Fluent setters for runtime creation:**

```csharp
var notification = ScriptableObject.CreateInstance<SONotification>();
notification
    .SetTitle("Scenario Complete")
    .SetMessage("All required steps have been completed. Proceed to debrief.")
    .SetIcon(successIcon);
```

***

## `SONotificationGroup` — Notification Registry

`SONotificationGroup` groups all notification assets your scene recognizes. `NotificationHandler` loads one group from `Resources/SONotificationGroup` automatically.

**Create:** Right-click → **Create → Convai → Notification System → Notification Group**

| Field             | Description                                      |
| ----------------- | ------------------------------------------------ |
| `soNotifications` | Array of all `SONotification` assets to register |

**Lookup methods:**

```csharp
if (SONotificationGroup.GetGroup(out SONotificationGroup group))
{
    if (group.TryGetById("scenario-complete", out SONotification notification))
    {
        // use notification
    }
}
```

{% hint style="danger" %}
The group asset must be saved to `Assets/Resources/SONotificationGroup.asset`. The path string used at runtime is `"SONotificationGroup"` — no file extension, no subdirectory. If the asset is missing, `NotificationHandler` logs `"[NotificationHandler] SONotificationGroup asset could not be resolved."` and no notifications display.
{% endhint %}

***

## Adding the Notification System to Your Scene

{% stepper %}
{% step %}
**Create Your Notification Assets**

Create one `SONotification` asset per alert type. Give each a unique `Id` string that matches what your error map or scripts reference.
{% endstep %}

{% step %}
**Create and Populate a Notification Group**

Create an `SONotificationGroup` asset. Add all your `SONotification` assets to its `soNotifications` array. Save to `Assets/Resources/SONotificationGroup.asset`.
{% endstep %}

{% step %}
**Add the NotificationSystem Prefab**

Drag `Packages/com.convai.convai-sdk-for-unity/Prefabs/Notifications/NotificationSystem.prefab` into your scene. This prefab contains both `NotificationHandler` and `UINotificationController`.

In `NotificationHandler`'s Inspector, assign your `SONotificationGroup` asset to the `notificationGroup` field.
{% endstep %}

{% step %}
**(Optional) Configure Timing**

Adjust `UINotificationController` Inspector fields to match your project's visual pacing. The defaults are good starting points for most scenarios.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
When the setup is correct, triggering a notification causes the panel to slide in from `activeNotificationPos` with a fade-in animation within 0.35 seconds.
{% endhint %}

***

## `UINotificationController` Inspector Reference

| Field                        | Default | Description                                                  |
| ---------------------------- | ------- | ------------------------------------------------------------ |
| `uiNotificationPrefab`       | —       | `UINotification` prefab to pool                              |
| `spacing`                    | `100`   | Vertical pixel spacing between stacked notifications         |
| `activeNotificationPos`      | —       | Anchored position where visible notifications appear         |
| `deactivatedNotificationPos` | —       | Anchored position where hidden notifications wait off-screen |
| `activeDuration`             | `4.0`   | Seconds a notification remains visible before sliding out    |
| `slipDuration`               | `0.3`   | Seconds for slide-in and slide-out animations                |
| `delay`                      | `0.3`   | Delay seconds before the slide animation begins              |
| `slipAnimationCurve`         | —       | Easing curve for the slide animation                         |

**Concurrency and queuing:** Up to `3` notifications display simultaneously. When a 4th notification is requested while 3 are active, it queues internally and displays as soon as one of the active notifications dismisses.

**Animation sequence per notification:** fade in (0.35s) → visible for `activeDuration` → delay (`delay`) → slide out (`slipDuration`) → next queued notification starts.

***

## Triggering Notifications from Code

Access `IConvaiNotificationService` through `ConvaiManager`:

```csharp
using Convai.Runtime.Components;
using Convai.SharedUnity;
using UnityEngine;

public class ScenarioNotifier : MonoBehaviour
{
    [SerializeField] private SONotification _stepCompleteNotification;
    [SerializeField] private SONotification _failureNotification;

    public void NotifyStepComplete()
    {
        if (ConvaiManager.ActiveManager.TryGetNotificationService(out var service))
            service.RequestNotification(_stepCompleteNotification);
    }

    public void NotifyFailure()
    {
        if (ConvaiManager.ActiveManager.TryGetNotificationService(out var service))
            service.RequestNotification(_failureNotification);
    }

    public void DismissAll()
    {
        if (ConvaiManager.ActiveManager.TryGetNotificationService(out var service))
            service.DismissNotification();
    }
}
```

`DismissNotification()` clears all currently displayed notifications immediately, including any animations in progress.

{% hint style="info" %}
The notification service includes a **10-second cooldown** per notification `Id`. If the same notification is requested multiple times within 10 seconds, duplicate requests are silently discarded. This prevents error floods from filling the screen. The cooldown resets automatically after 10 seconds.
{% endhint %}

***

## Error → Notification Mapping

Session errors automatically trigger notifications via `SONotificationErrorMap`. This asset maps error code strings to `SONotification` assets using an ordered rule list. The **first matching rule wins**.

**Create:** Right-click → **Create → Convai → Notification System → Session Error Map**

Save to `Assets/Resources/SONotificationErrorMap.asset` for automatic loading.

### `SessionErrorNotificationRule` Fields

| Field          | Default | Description                                                                    |
| -------------- | ------- | ------------------------------------------------------------------------------ |
| `ErrorPattern` | —       | The error code string to match against the session error                       |
| `MatchType`    | `Exact` | `Exact` — full string equality. `Prefix` — error code starts with this pattern |
| `Notification` | —       | `SONotification` to display when this rule matches                             |

**Example rule table:**

| ErrorPattern  | MatchType | Notification                   |
| ------------- | --------- | ------------------------------ |
| `AUTH_FAILED` | `Exact`   | `Notification_AuthError`       |
| `CONNECTION_` | `Prefix`  | `Notification_ConnectionError` |
| `RATE_LIMIT`  | `Exact`   | `Notification_RateLimit`       |

Rules are evaluated top-to-bottom. Place more specific rules above broader prefix matches.

***

## Runtime Settings Integration

The notification system respects the **Notifications** toggle in the built-in Settings Panel. When the user disables notifications:

* Any currently displayed notification dismisses immediately
* Subsequent `RequestNotification` calls are silently ignored
* The log records: `"Cannot send notification because notifications are disabled in runtime settings."`

To toggle notifications from script:

```csharp
if (ConvaiManager.ActiveManager.TryGetRuntimeSettingsService(out var settings))
{
    settings.Apply(new ConvaiRuntimeSettingsPatch { NotificationsEnabled = false });
}
```

***

## Usage Examples

### Corporate Onboarding — Step Completion Alerts

A corporate onboarding simulation notifies the trainee each time they complete a required dialogue checkpoint with the AI HR representative:

* Create an `SONotification` asset with `Id = "checkpoint-complete"`, a checkmark icon, and the message "Checkpoint complete. Move to the next topic."
* Call `service.RequestNotification(checkpointNotification)` from the checkpoint evaluation handler
* The notification appears for 4 seconds and dismisses without interrupting the ongoing conversation
* The 10-second cooldown prevents duplicate notifications if the evaluation logic fires multiple times

### Connection Error Alert — Firewall-Restricted Environment

A training simulation running on a corporate network needs informative error messages when the connection fails, instead of the default silent failure:

* Create an `SONotificationErrorMap` with a rule: `ErrorPattern = "CONNECTION_"`, `MatchType = Prefix`
* Set `Notification` to an asset with the message "Connection failed. Please contact IT support at ext. 4400."
* The error map fires automatically on any `CONNECTION_` prefixed error — no additional code required

### Session Reset — Dismiss All on Scenario Change

A multi-scenario simulation clears any lingering notifications when transitioning between scenarios:

```csharp
public void TransitionToNextScenario()
{
    if (ConvaiManager.ActiveManager.TryGetNotificationService(out var service))
        service.DismissNotification();

    // Continue with scene/scenario transition
    LoadNextScenario();
}
```

***

## Troubleshooting

| Symptom                                                                                                                               | Likely Cause                                                                            | Fix                                                                                                                                   |
| ------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| No notifications appear; console shows `"[NotificationHandler] SONotificationGroup asset could not be resolved."`                     | Group asset not in `Resources/`                                                         | Save the asset to `Assets/Resources/SONotificationGroup.asset`                                                                        |
| Console shows `"[NotificationHandler] No UINotificationController found and no prefab set."`                                          | `NotificationSystem.prefab` not in scene or `notificationControllerPrefab` not assigned | Add the prefab to the scene or assign a controller prefab in `NotificationHandler` Inspector                                          |
| Console shows `"[NotificationHandler] Notification service not available; notifications will be deferred until services initialize."` | Notification triggered before `ConvaiManager` finishes initialization                   | Delay notification calls until `ConvaiManager.IsInitialized` is `true`                                                                |
| Console shows `"[NotificationHandler] No notification registered in the notification group for id: {id}"`                             | Notification `Id` in script does not match any asset in `SONotificationGroup`           | Check the `Id` field on the `SONotification` asset and update the group                                                               |
| Console shows `"[NotificationHandler] UINotificationController is null, cannot display notification."`                                | Controller reference lost or not found in scene                                         | Verify `NotificationSystem.prefab` is in the scene and `NotificationHandler` found the controller                                     |
| Notification requested but not shown; no console errors                                                                               | 10-second cooldown active for this notification                                         | Wait 10 seconds or use a different notification asset with a unique `Id`                                                              |
| Notifications disabled after Settings Panel interaction                                                                               | User toggled **Notifications** off                                                      | Re-enable via Settings Panel or `IConvaiRuntimeSettingsService.Apply(new ConvaiRuntimeSettingsPatch { NotificationsEnabled = true })` |
| 4th notification not showing immediately                                                                                              | Max 3 concurrent — 4th is queued                                                        | Expected behavior — it will display as soon as an active notification dismisses                                                       |

***

## Next Steps

{% content-ref url="/broken/pages/5b9ad404d6290ca7355a75ec12b6e2f1a9ea1ceb" %}
[Broken link](/broken/pages/5b9ad404d6290ca7355a75ec12b6e2f1a9ea1ceb)
{% endcontent-ref %}
