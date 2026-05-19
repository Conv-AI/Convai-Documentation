---
description: >-
  Replace SDK providers, extend the runtime with custom modules, and diagnose
  latency using built-in telemetry — for deployments where the defaults are not
  enough.
---

# Advanced Topics

### When the Defaults Are Not Enough

The Convai Unity SDK works out of the box for most training simulations, interactive experiences, and games. This section covers what to reach for when the defaults do not fit your deployment: replacing built-in providers with custom implementations, diagnosing performance issues with built-in telemetry, and extending the SDK with your own modules.

{% hint style="info" %}
These pages assume C# proficiency and familiarity with Unity's component lifecycle. If you are still setting up your first scene, start with the [Getting Started](/broken/pages/f1798a7c5eb3edd97ea7659e7aa40726a177589d) section.
{% endhint %}

***

**Not sure which page to start with?**

* **CI pipelines, secrets management, or custom auth?** → Start with [Custom Providers](/broken/pages/be49190eb0e42d157b6f4017641dff424ef12088).
* **Latency too high, logs too noisy, connections flaky?** → Start with [Performance and Optimization](/broken/pages/d6c8058e5ce6a5a88384ae5c2ef7035c98b775d9).
* **Need to add new runtime behaviors that hook into the SDK lifecycle?** → Start with [Extending the SDK](/broken/pages/dc04d300e62705a43ddd6cf9a6f820244872960b).

***

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Custom Providers</strong><br>Replace the SDK's credential, identity, and persistence systems with your own implementations. Essential for CI pipelines, auth-backed identity, and cloud save integration.</td><td><a href="/broken/pages/be49190eb0e42d157b6f4017641dff424ef12088">Broken link</a></td></tr><tr><td><strong>Performance and Optimization</strong><br>Tune log verbosity per subsystem, read server-side pipeline latency metrics, and configure retry behavior for resilient connections.</td><td><a href="/broken/pages/d6c8058e5ce6a5a88384ae5c2ef7035c98b775d9">Broken link</a></td></tr><tr><td><strong>Extending the SDK</strong><br>Add custom modules that participate in the runtime lifecycle, share services with other modules, and integrate tightly with the SDK's event and agent systems.</td><td><a href="/broken/pages/dc04d300e62705a43ddd6cf9a6f820244872960b">Broken link</a></td></tr></tbody></table>
