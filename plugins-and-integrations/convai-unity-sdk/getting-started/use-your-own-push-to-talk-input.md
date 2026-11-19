---
title: Use your own push-to-talk input
description: >-
  Connect a UI button, rebound key, or XR control to push-to-talk while taking
  ownership of input and handling release, focus loss, and cleanup.
last_reviewed: "5.0.0-preview"
---

Call `ConvaiPushToTalkController.Press()` when your control is pressed and `Release()` when it is released. First acquire input ownership from the manager so its built-in keyboard and XR bindings do not also drive the same controller.

## Connect a UI button

{% stepper %}
{% step %}
### Configure the scene for push-to-talk

Follow [Configure conversation input mode](configure-conversation-input-mode.md), and confirm the connected character accepts player input. Keep **Allow Microphone** enabled. A controller refuses presses while disconnected, preparing, finishing a capture or otherwise blocked.
{% endstep %}

{% step %}
### Add the input adapter

Add this script to a UI button with pointer events. Assign the scene's `ConvaiManager`. Use one adapter as the owner of this button's press and release pair.

```csharp
using System;
using Convai.Runtime.Components;
using UnityEngine;
using UnityEngine.EventSystems;

public sealed class TalkButton : MonoBehaviour,
    IPointerDownHandler, IPointerUpHandler
{
    [SerializeField] private ConvaiManager _manager;
    private IDisposable _inputLease;
    private ConvaiPushToTalkController _controller;
    private bool _ownsPress;

    private void OnEnable()
    {
        if (_manager != null)
            _inputLease = _manager.AcquirePushToTalkInput();
    }

    public void OnPointerDown(PointerEventData eventData)
    {
        if (_manager == null || _inputLease == null || _ownsPress) return;
        // A scene that started hands-free may only create it after a mode change.
        _controller = _manager.GetComponent<ConvaiPushToTalkController>();
        if (_controller == null) return;
        _ownsPress = _controller.Press();
        if (!_ownsPress)
            Debug.LogWarning(_controller.BlockedReason, this);
    }

    public void OnPointerUp(PointerEventData eventData) => EndPress();

    private void OnApplicationFocus(bool focused)
    {
        if (!focused) EndPress();
    }

    private void OnApplicationPause(bool paused)
    {
        if (paused) EndPress();
    }

    private void OnDisable()
    {
        EndPress();
        _inputLease?.Dispose();
        _inputLease = null;
        _controller = null;
    }

    private void EndPress()
    {
        if (_ownsPress && _controller != null && _controller.IsPressed)
            _controller.Release();
        _ownsPress = false;
    }
}
```

For a rebound keyboard or XR binding, call the same press and release methods from that input system's callbacks. `ConvaiPushToTalkInputReader` is an internal SDK helper, not a component to add to the scene.
{% endstep %}

{% step %}
### Verify input ownership

While the adapter is enabled, the built-in **Push To Talk Key** must not start a turn. Press and release the UI button to speak. Disable the adapter, then press the built-in key again; a new key-down should work. A key already held when ownership returns does not start a turn.
{% endstep %}
{% endstepper %}

## Follow the SDK state

The lease only disables built-in input. The SDK can still end capture when the app loses focus or pauses, the target or mode changes, the room disconnects, player speech is held, or the controller is disabled. Use `IsPressed` and `StateChanged` to draw the control's actual state.

`Press(true)` keeps an accepted press through focus loss when your input source can reliably observe release outside the application. It does not bypass pause, disconnect or the other release conditions. Ordinary UI buttons should use `Press()`.

Leases are counted and belong to one manager. Dispose each lease on the main thread, after releasing your own press. A new manager in a new scene needs a new lease. Multiple leases suppress built-in input; they do not coordinate competing custom input owners.

A successful `Release()` starts turn finalization. It does not mean a reply has arrived. For commit, wait and retry states, see [Push-to-talk lifecycle](../core-concepts/push-to-talk-lifecycle.md) and the [Push-to-talk API](../scripting-reference/push-to-talk-api.md).
