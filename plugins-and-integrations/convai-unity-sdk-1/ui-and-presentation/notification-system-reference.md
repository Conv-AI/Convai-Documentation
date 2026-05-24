---
title: Notification system reference
description: Reference for SONotification, SONotificationGroup, UINotificationController, and SONotificationErrorMap — fields, methods, and configuration options.
last_reviewed: "4.2.0"
---

Reference for the ScriptableObject assets and the controller component that make up the notification system. For setup instructions and triggering notifications from code, see [Notification system](notification-system.md).

## `SONotification`

Each notification is a `ScriptableObject` asset containing the content to display.

**Create:** Right-click in the Project window → **Create → Convai → Notification System → Notification**

**Fields:**

| Field | Type | Description |
| --- | --- | --- |
| `icon` | `Sprite` | Sprite shown in the notification icon slot. Optional — leave empty for no icon |
| `notificationTitle` | `string` | Title text shown in bold |
| `notificationMessage` | `string` | Body text. Supports multi-line content |
| `Id` | `string` | Stable string identifier used for error mapping and deduplication cooldowns. Defaults to the asset name if empty |

**Fluent setters for runtime creation:**

| Method | Return type | Description |
| --- | --- | --- |
| `SetTitle(string title)` | `SONotification` | Set the notification title |
| `SetMessage(string message)` | `SONotification` | Set the notification body text |
| `SetIcon(Sprite newIcon)` | `SONotification` | Set the notification icon sprite |

Methods return `this`, enabling chaining:

```csharp
var notification = ScriptableObject.CreateInstance<SONotification>();
notification
    .SetTitle("Scenario Complete")
    .SetMessage("All required steps have been completed. Proceed to debrief.")
    .SetIcon(successIcon);
```

## `SONotificationGroup`

`SONotificationGroup` registers all `SONotification` assets the scene recognizes. `NotificationHandler` resolves notification IDs against this group at runtime.

**Create:** Right-click → **Create → Convai → Notification System → Notification Group**

**Fields:**

| Field | Type | Description |
| --- | --- | --- |
| `soNotifications` | `SONotification[]` | All `SONotification` assets available to the notification system |

**Static lookup methods:**

| Method | Return type | Description |
| --- | --- | --- |
| `GetGroup(out SONotificationGroup group)` | `bool` | Loads the group from `Resources/SONotificationGroup`. Returns `false` if the asset is missing |
| `TryGetById(string notificationId, out SONotification notification)` | `bool` | Finds a notification by its `Id` field. Returns `false` if no match |

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

## `UINotificationController`

Manages the pool of reusable `UINotification` elements and controls the slide animation for each notification.

**Inspector fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `uiNotificationPrefab` | `UINotification` | — | `UINotification` prefab to pool |
| `spacing` | `int` | `100` | Vertical pixel spacing between stacked notifications |
| `activeNotificationPos` | `Vector2` | — | Anchored position where visible notifications appear |
| `deactivatedNotificationPos` | `Vector2` | — | Anchored position where hidden notifications wait off-screen |
| `activeDuration` | `float` | `4.0` | Seconds a notification remains visible before sliding out |
| `slipDuration` | `float` | `0.3` | Seconds for slide-in and slide-out animations |
| `delay` | `float` | `0.3` | Delay seconds before the slide animation begins |
| `slipAnimationCurve` | `AnimationCurve` | — | Easing curve for the slide animation |

**Concurrency and queuing:** Up to 3 notifications display simultaneously. When a 4th notification is requested while 3 are active, it queues and displays as soon as one of the active notifications dismisses.

**Animation sequence per notification:** slide in (`slipDuration`) → visible for `activeDuration` → delay (`delay`) → slide out (`slipDuration`) → next queued notification starts.

## `SONotificationErrorMap`

Maps session error code strings to `SONotification` assets using an ordered rule list. Load from `Resources/SONotificationErrorMap` automatically, or assign manually.

**Create:** Right-click → **Create → Convai → Notification System → Session Error Map**

Save to `Assets/Resources/SONotificationErrorMap.asset` for automatic loading.

**Fields:**

| Field | Type | Description |
| --- | --- | --- |
| `Rules` | `List<SessionErrorNotificationRule>` | Ordered list of error-to-notification rules. The first matching rule wins |

### `SessionErrorNotificationRule`

| Field | Type | Description |
| --- | --- | --- |
| `ErrorPattern` | `string` | The error code string to match against the session error |
| `MatchType` | `SessionErrorMatchType` | `Exact` — full string equality. `Prefix` — error code starts with this pattern |
| `Notification` | `SONotification` | `SONotification` asset to display when this rule matches |

Rules are evaluated top-to-bottom. Place more specific rules above broader prefix matches.

**Example rule configuration:**

| ErrorPattern | MatchType | Notification |
| --- | --- | --- |
| `AUTH_FAILED` | `Exact` | `Notification_AuthError` |
| `CONNECTION_` | `Prefix` | `Notification_ConnectionError` |
| `RATE_LIMIT` | `Exact` | `Notification_RateLimit` |

## Next steps

{% content-ref url="notification-system.md" %}
[Notification system](notification-system.md)
{% endcontent-ref %}

{% content-ref url="customizing-ui-components.md" %}
[Customizing UI components](customizing-ui-components.md)
{% endcontent-ref %}
