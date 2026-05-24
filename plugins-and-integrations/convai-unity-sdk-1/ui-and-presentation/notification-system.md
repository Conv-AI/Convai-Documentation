---
title: Notification system
description: >-
  Add toast-style alerts that automatically display session error notifications
  and let you trigger custom in-scene alerts from code using ScriptableObject
  notification assets.
last_reviewed: "4.2.0"
---

The notification system displays transient, toast-style popups in your scene. It handles session error alerts automatically — when Convai reports a connection or authentication error, the system maps the error code to a notification asset and queues it for display. You can also trigger custom notifications from code at any point during a session.

Up to three notifications appear on screen simultaneously. Additional notifications queue internally and display as space becomes available.

For field-level reference on `SONotification`, `SONotificationGroup`, `UINotificationController`, and `SONotificationErrorMap`, see [Notification system reference](notification-system-reference.md).

## How the notification system works

The following diagram shows the system's data flow:

```mermaid
graph TD
    A[IConvaiNotificationService] -->|RequestNotification| B[NotificationHandler]
    B -->|resolves via SONotificationGroup| C[UINotificationController]
    C -->|pool of 3| D[UINotification]
    E[Session error] -->|SONotificationErrorMap| A
    F[Your script] -->|RequestNotification| A
    G[Runtime settings\nNotificationsEnabled=false] -->|RuntimeSettingsNotificationApplier| A
```

`IConvaiNotificationService` is the single entry point for all notification requests. `NotificationHandler` resolves the notification asset by ID using `SONotificationGroup`, then passes it to `UINotificationController`, which manages a pool of reusable `UINotification` elements. Session errors route through `SONotificationErrorMap` to map error codes to notification assets automatically.

## Add the notification system to your scene

{% stepper %}
{% step %}
### Create your notification assets

Create one `SONotification` asset per alert type. Give each a unique `Id` string that matches what your error map or scripts reference.
{% endstep %}

{% step %}
### Create and populate a notification group

Create an `SONotificationGroup` asset. Add all your `SONotification` assets to its `soNotifications` array. Save to `Assets/Resources/SONotificationGroup.asset`.
{% endstep %}

{% step %}
### Add the NotificationSystem prefab

Drag `NotificationSystem.prefab` into your scene. Find it at `Prefabs/Notifications/NotificationSystem.prefab` in the <code class="expression">space.vars.sdk_package_id</code> package. This prefab contains both `NotificationHandler` and `UINotificationController`.

In `NotificationHandler`'s Inspector, assign your `SONotificationGroup` asset to the `notificationGroup` field.

{% hint style="warning" %}
**Screenshot required before publishing:** Capture the Unity Inspector with the `NotificationHandler` component selected. The image must show the `notificationGroup` field with an `SONotificationGroup` asset assigned.
{% endhint %}

<figure><img src="../../../.gitbook/assets/TODO-notification-handler-inspector.png" alt="Unity Inspector showing the NotificationHandler component with the notificationGroup field assigned to an SONotificationGroup asset"><figcaption><p>TODO: Replace with screenshot showing NotificationHandler Inspector with notificationGroup assigned.</p></figcaption></figure>
{% endstep %}

{% step %}
### Configure timing (optional)

Adjust `UINotificationController` Inspector fields to match your project's visual pacing. The defaults are suitable starting points for most scenarios.

When setup is correct, triggering a notification causes the panel to slide in from `activeNotificationPos`. The slide-in animation runs for `slipDuration` seconds (default `0.3`s).
{% endstep %}
{% endstepper %}

## Trigger notifications from code

Access `IConvaiNotificationService` through `ConvaiManager`:

```csharp
using Convai.Runtime.Components;
using Convai.Runtime.Presentation.Views.Notifications;
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
The notification service enforces a **10-second cooldown** per notification `Id`. Duplicate requests within 10 seconds are silently discarded. This prevents error floods from filling the screen. The cooldown resets automatically after 10 seconds.
{% endhint %}

## Automatic error-to-notification mapping

Session errors automatically trigger notifications via `SONotificationErrorMap`. This asset maps error code strings to `SONotification` assets using an ordered rule list. The **first matching rule wins**.

**Create:** Right-click → **Create → Convai → Notification System → Session Error Map**

Save to `Assets/Resources/SONotificationErrorMap.asset` for automatic loading.

For the complete `SessionErrorNotificationRule` field reference, see [Notification system reference](notification-system-reference.md).

**Example rule configuration:**

| ErrorPattern | MatchType | Notification |
| --- | --- | --- |
| `AUTH_FAILED` | `Exact` | `Notification_AuthError` |
| `CONNECTION_` | `Prefix` | `Notification_ConnectionError` |
| `RATE_LIMIT` | `Exact` | `Notification_RateLimit` |

Rules are evaluated top-to-bottom. Place more specific rules above broader prefix matches.

## Respect the notifications runtime setting

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

## Usage examples

### Corporate onboarding — step completion alerts

A corporate onboarding simulation notifies the trainee each time they complete a required dialogue checkpoint with the AI HR representative:

* Create an `SONotification` asset with `Id = "checkpoint-complete"`, a checkmark icon, and the message "Checkpoint complete. Move to the next topic."
* Call `service.RequestNotification(checkpointNotification)` from the checkpoint evaluation handler
* The notification appears for 4 seconds and dismisses without interrupting the ongoing conversation
* The 10-second cooldown prevents duplicate notifications if the evaluation logic fires multiple times

At runtime, each checkpoint completion produces a brief confirmation that appears and clears without pausing the dialogue.

### Connection error in firewall-restricted environments

A training simulation running on a corporate network requires informative error messages when the connection fails:

* Create an `SONotificationErrorMap` with a rule: `ErrorPattern = "CONNECTION_"`, `MatchType = Prefix`
* Set `Notification` to an asset with the message "Connection failed. Please contact IT support at ext. 4400."
* The error map fires automatically on any `CONNECTION_` prefixed error — no additional code required

At runtime, any connection failure produces a clear, actionable notification instead of a silent failure.

### Multi-scenario reset — dismiss all on scenario change

A multi-scenario simulation clears any lingering notifications when transitioning between scenarios:

```csharp
public void TransitionToNextScenario()
{
    if (ConvaiManager.ActiveManager.TryGetNotificationService(out var service))
        service.DismissNotification();

    LoadNextScenario();
}
```

At runtime, calling `DismissNotification()` immediately clears the screen before the next scenario loads, ensuring stale alerts do not appear in the wrong context.

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| No notifications appear; console shows `"[NotificationHandler] SONotificationGroup asset could not be resolved."` | Group asset not in `Resources/` | Save to `Assets/Resources/SONotificationGroup.asset` |
| Console shows `"[NotificationHandler] No UINotificationController found and no prefab set."` | `NotificationSystem.prefab` not in scene or `notificationControllerPrefab` not assigned | Add the prefab to the scene or assign a controller prefab in `NotificationHandler` Inspector |
| Console shows `"[NotificationHandler] Notification service not available; notifications will be deferred until services initialize."` | Notification triggered before `ConvaiManager` finishes initialization | Delay notification calls until `ConvaiManager.IsInitialized` is `true` |
| Console shows `"[NotificationHandler] No notification registered in the notification group for id: {id}"` | Notification `Id` in script does not match any asset in `SONotificationGroup` | Check the `Id` field on the `SONotification` asset and update the group |
| Console shows `"[NotificationHandler] UINotificationController is null, cannot display notification."` | Controller reference lost or not found in scene | Verify `NotificationSystem.prefab` is in the scene |
| Notification requested but not shown; no console errors | 10-second cooldown active for this notification | Wait 10 seconds or use a different notification asset with a unique `Id` |
| Notifications disabled after Settings Panel interaction | User toggled **Notifications** off | Re-enable via Settings Panel or `IConvaiRuntimeSettingsService.Apply(new ConvaiRuntimeSettingsPatch { NotificationsEnabled = true })` |
| 4th notification not showing immediately | Max 3 concurrent — 4th is queued | Expected behavior — it displays as soon as an active notification dismisses |

## Next steps

With the notification system in place, you can surface connection errors, scenario events, and custom alerts without interrupting the AI conversation. To give users control over whether notifications appear, wire the Settings Panel. To restyle the notification visuals, see Customizing UI Components.

{% content-ref url="settings-panel.md" %}
[Settings Panel](settings-panel.md)
{% endcontent-ref %}

{% content-ref url="customizing-ui-components.md" %}
[Customizing UI components](customizing-ui-components.md)
{% endcontent-ref %}

{% content-ref url="notification-system-reference.md" %}
[Notification system reference](notification-system-reference.md)
{% endcontent-ref %}
