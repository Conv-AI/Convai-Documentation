---
title: Notification system reference
last_reviewed: "5.0.0-pre.1"
description: Look up notification asset fields, controller timing, error matching, and services for showing automatic and application-defined alerts.
---

Reference for the ScriptableObject assets and the controller component that make up the notification system. For setup instructions and triggering notifications from code, see [Notification system](./).

## `SONotification`

Each notification is a `ScriptableObject` asset containing the content to display.

**Create:** Right-click in the Project window → **Create → Convai → Notification System → Notification**

**Fields:**

| Field                 | Type     | Description                                                                                                      |
| --------------------- | -------- | ---------------------------------------------------------------------------------------------------------------- |
| `icon`                | `Sprite` | Sprite shown in the notification icon slot. Optional — leave empty for no icon                                   |
| `notificationTitle`   | `string` | Title text shown in bold                                                                                         |
| `notificationMessage` | `string` | Body text. Supports multi-line content                                                                           |
| `Id`                  | `string` | Stable string identifier used for error mapping and deduplication cooldowns. Defaults to the asset name if empty |

**Fluent setters for an existing asset:**

| Method                       | Return type      | Description                      |
| ---------------------------- | ---------------- | -------------------------------- |
| `SetTitle(string title)`     | `SONotification` | Set the notification title       |
| `SetMessage(string message)` | `SONotification` | Set the notification body text   |
| `SetIcon(Sprite newIcon)`    | `SONotification` | Set the notification icon sprite |

Methods return and modify the same object. Pass the notification asset directly to the service.

## `UINotificationController`

Manages the pool of reusable `UINotification` elements and controls the slide animation for each notification.

**Inspector fields:**

| Field                        | Type             | Default | Description                                                  |
| ---------------------------- | ---------------- | ------- | ------------------------------------------------------------ |
| `uiNotificationPrefab`       | `UINotification` | —       | `UINotification` prefab to pool                              |
| `spacing`                    | `int`            | `100`   | Vertical pixel spacing between stacked notifications         |
| `activeNotificationPos`      | `Vector2`        | —       | Anchored position where visible notifications appear         |
| `deactivatedNotificationPos` | `Vector2`        | —       | Anchored position where hidden notifications wait off-screen |
| `activeDuration`             | `float`          | `4.0`   | Seconds a notification remains visible before sliding out    |
| `slipDuration`               | `float`          | `0.3`   | Seconds for slide-in and slide-out animations                |
| `delay`                      | `float`          | `0.3`   | Extra time held at the end of each slide              |
| `slipAnimationCurve`         | `AnimationCurve` | —       | Easing curve for the slide animation                         |

The script default for `spacing` is `100`; the shipped controller prefab uses `110`. Its active position is `(0, -100)` and hidden position is `(500, -100)`.

**Concurrency and queuing:** the controller pools three items. A request joins the queue while a slide animation is active, even if another item is free. Queued requests are reconsidered after the full cycle finishes. A fresh request during the visible hold can start immediately if a pooled item is free.

**Animation sequence:** move in for `slipDuration + delay` → remain active for `activeDuration` → move out for `slipDuration + delay`. The position reaches its endpoint after `slipDuration` and holds for `delay`. The controller also fades its canvas in over `0.35` seconds and out over `0.2` seconds.

`Notify(SONotification)` queues an asset; `ClearAll()` stops animations, clears the queue, and hides the pooled notifications.

## `SONotificationErrorMap`

Maps session error code strings to `SONotification` assets using an ordered rule list. The built-in runtime bridge loads the packaged `Resources/SONotificationErrorMap` automatically. There is no Inspector replacement field on `NotificationHandler`.

**Create:** Right-click → **Create → Convai → Notification System → Session Error Map**

Use an explicit map only in a notification bridge you own. Do not add a second resource with the same name or a second automatic bridge alongside the runtime host without accounting for duplicate handling.

**Fields:**

| Field   | Type                                 | Description                                                               |
| ------- | ------------------------------------ | ------------------------------------------------------------------------- |
| `Rules` | `List<SessionErrorNotificationRule>` | Ordered list of error-to-notification rules. The first matching rule wins |

### `SessionErrorNotificationRule`

| Field          | Type                    | Description                                                                    |
| -------------- | ----------------------- | ------------------------------------------------------------------------------ |
| `ErrorPattern` | `string`                | The error code string to match against the session error                       |
| `MatchType`    | `SessionErrorMatchType` | `Exact` — full string equality. `Prefix` — error code starts with this pattern |
| `Notification` | `SONotification`        | `SONotification` asset to display when this rule matches                       |

Rules use ordinal, case-insensitive matching and run top-to-bottom. A rule with a missing notification or blank pattern does not match; neither does a blank error code. Place specific exact rules before a broad prefix. `SessionErrorMatchType` belongs to `Convai.Shared.Notifications`.

**Example rule configuration:**

| ErrorPattern  | MatchType | Notification                   |
| ------------- | --------- | ------------------------------ |
| `connection.auth_failed` | `Exact`   | `Notification_AuthError`       |
| `connection.rate_limited`  | `Exact`   | `Notification_RateLimit`       |
| `connection.` | `Prefix`  | `Notification_ConnectionError` |

## Service and handler

`IConvaiNotificationService` is in `Convai.Shared.Notifications`. Resolve it with `ConvaiManager.TryGetNotificationService`.

| Member | Purpose |
| --- | --- |
| `RequestNotification(SONotification)` | Raise a request; no service-level cooldown |
| `DismissNotification()` | Raise a dismissal request |
| `OnNotificationRequested` | `Action<SONotification>` event |
| `OnNotificationDismissed` | `Action` event |

`NotificationHandler` displays the requested asset through its child `UINotificationController` or instantiates the assigned `notificationControllerPrefab` when needed. The runtime error bridge checks the notification setting and applies a 10-second per-ID cooldown. Application code can check the preference before requesting an alert.

## Next steps

{% content-ref url="./" %}
[.](./)
{% endcontent-ref %}

{% content-ref url="../customizing-ui-components.md" %}
[Customizing UI components](../customizing-ui-components.md)
{% endcontent-ref %}
