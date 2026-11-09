---
title: Notification system
last_reviewed: "5.0.0-preview"
description: Add toast-style alerts for session errors and in-scene events, enable notifications, and register the assets your scene displays.
---

The notification system displays toast-style alerts from registered `SONotification` assets. Notifications are disabled in the project runtime defaults, so adding the prefab alone does not show alerts. This guide assumes a scene with an initialized `ConvaiManager`.

## Add the notification system

{% stepper %}
{% step %}
### Add the shipped prefab

Drag `Prefabs/Notifications/NotificationSystem.prefab` from the <code class="expression">space.vars.sdk_package_id</code> package into your scene. It supplies `NotificationHandler` and the notification controller.

The prefab already references the packaged `SONotificationGroup`, which contains six notifications. Keep that assignment for the standard alerts. `NotificationHandler` uses `Resources/SONotificationGroup` only when its serialized group is empty.
{% endstep %}
{% step %}
### Enable notifications

Enable **Notifications** in the runtime settings panel, or set the project default in **Convai → Settings → Runtime Defaults**. Saved runtime overrides take precedence over project defaults. You can also apply `ConvaiRuntimeSettingsPatch.NotificationsEnabled = true` from code.
{% endstep %}
{% step %}
### Register custom alerts

Create an asset with **Create → Convai → Notification System → Notification**. Set its title, message, optional icon, and a unique ID. An empty serialized ID falls back to the asset name.

For a custom alert set, create a project-owned notification group, include every notification your scene needs, and assign it to `NotificationHandler.notificationGroup`. Keep any standard alerts that the error map still references. Do not create another resource with the same `SONotificationGroup` resource name as the packaged asset; explicit assignment avoids an ambiguous resource lookup.
{% endstep %}
{% step %}
### Test an alert

Assign one registered asset to the component below and invoke `ShowAlert()` from a scene button. Confirm that its title and message appear, then clear after the animation cycle. `DismissAll()` clears visible and queued alerts.
{% endstep %}
{% endstepper %}

## Trigger notifications from code

The example resolves the service at the moment you request an alert:

```csharp
using Convai.Runtime.Components;
using Convai.Runtime.Presentation.Views.Notifications;
using UnityEngine;

public class ScenarioNotifier : MonoBehaviour
{
    [SerializeField] private SONotification alert;

    public void ShowAlert()
    {
        var manager = ConvaiManager.ActiveManager;
        if (manager != null && alert != null &&
            manager.TryGetNotificationService(out var service))
            service.RequestNotification(alert);
    }

    public void DismissAll()
    {
        var manager = ConvaiManager.ActiveManager;
        if (manager != null && manager.TryGetNotificationService(out var service))
            service.DismissNotification();
    }
}
```

The handler resolves the requested notification's ID to the asset registered in its group. Creating an unregistered notification at runtime does not bypass this lookup. To change content at runtime, take care with the registered asset: the fluent setters mutate the shared `ScriptableObject`, including its Editor asset state.

## Automatic error notifications

The runtime notification bridge maps session errors through the packaged `Resources/SONotificationErrorMap` asset. Its 19 ordered rules choose the first matching notification. For example, exact `connection.auth_failed` and `connection.rate_limited` rules should precede a broader `connection.` prefix rule.

The bridge suppresses repeated automatic notifications with the same ID for 10 seconds. Direct `IConvaiNotificationService.RequestNotification` calls do not have that cooldown; add application-level deduplication if your event can fire repeatedly.

The built-in runtime host owns its bridge. There is no `NotificationHandler` Inspector field for replacing the host's error map. Creating a second `Resources/SONotificationErrorMap` asset risks an ambiguous load. A separately constructed bridge can receive an explicit map, but adding one alongside the built-in bridge can duplicate alerts. For a custom error presentation, subscribe to session errors and own that presentation deliberately; see [Connection and API issues](../../troubleshooting/connection-and-api-issues.md).

## Visibility and timing

When notifications are disabled, the runtime settings applier dismisses existing alerts and the handler drops subsequent requests. Re-enabling notifications does not replay those dropped requests.

`UINotificationController` pools three items. Requests queue while a slide animation is running, even if a pooled item is free. Queued requests are reconsidered after a complete slide-in, visible hold, and slide-out cycle. A fresh request during the visible hold can start immediately if a pooled item is free. See [Notification system reference](notification-system-reference.md) for exact timing fields.

## Troubleshooting

| Symptom | Cause | Fix and verification |
| --- | --- | --- |
| No alert appears | Notifications are disabled by default or a saved override | Enable Notifications; request a registered alert again |
| `SONotificationGroup asset could not be resolved.` | Neither an assigned group nor a resource fallback exists | Assign your group; retry the alert |
| `No notification registered in the notification group for id:` | The request's ID is absent from the assigned group | Add the asset with that exact ID; retry |
| A custom alert shows different text | ID resolution selects the registered asset | Inspect the group asset matching that ID and request it directly |
| An automatic error does not repeat immediately | The bridge's 10-second cooldown applies | Wait for the cooldown and reproduce the error |
| A direct custom alert repeats | The raw service does not deduplicate | Gate the calling event or add your own cooldown; reproduce it twice |
| An alert starts later than expected | A notification animation cycle is in progress | Wait through the cycle and confirm the queued alert appears |

## Next steps

{% content-ref url="notification-system-reference.md" %}
[Notification system reference](notification-system-reference.md)
{% endcontent-ref %}
