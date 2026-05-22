---
description: >-
  Replace SDK providers, extend the runtime with custom modules, and diagnose
  latency using built-in telemetry — for deployments where the defaults are not
  enough.
title: Customize and extend the SDK
last_reviewed: "4.2.0"
---

The Convai Unity SDK works out of the box for most training simulations, interactive experiences, and games. This section covers what to reach for when the defaults do not fit your deployment: replacing built-in providers with custom implementations, diagnosing performance issues with built-in telemetry, and adding custom modules to the runtime.

{% hint style="info" %}
These pages assume C# proficiency and familiarity with Unity's component lifecycle. If you are still setting up your first scene, start with the [Getting Started](../getting-started/README.md) section.
{% endhint %}

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Credentials, identity, and storage</strong><br>Replace the SDK's credential, identity, and persistence systems with your own implementations. Essential for CI pipelines, auth-backed identity, and cloud save integration.</td><td><a href="custom-providers/README.md">custom-providers/README.md</a></td></tr><tr><td><strong>Logging, metrics, and retry policy</strong><br>Tune log verbosity per subsystem, read server-side pipeline latency metrics, and configure retry behavior for resilient connections.</td><td><a href="performance-and-optimization.md">performance-and-optimization.md</a></td></tr><tr><td><strong>Runtime module system</strong><br>Understand when to build custom modules, how the module lifecycle works, and which SDK extension points are safe to use.</td><td><a href="extending-the-sdk.md">extending-the-sdk.md</a></td></tr></tbody></table>
