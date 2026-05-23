---
title: Core concepts
description: Find explanations for how the Convai Unity SDK works at runtime — connection management, session state, turn-taking, and event-driven scene responses.
last_reviewed: "4.2.0"
---

The Core Concepts section explains the systems that run beneath every Convai character in your scene — the runtime layers that manage connections, the session state machine that governs each character's lifecycle, the turn-taking system that controls who speaks and when, and the event components that let your scene react to what happens at runtime.

Start with **Architecture Deep Dive** if you are new to the SDK internals. Read the other pages when you need to configure a specific system or understand why the SDK behaves a certain way.

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Runtime architecture</strong><br>Runtime layers, interface inventory, and what you can replace.</td><td><a href="runtime-architecture.md">runtime-architecture.md</a></td></tr><tr><td><strong>Session lifecycle</strong><br>State machine, per-character sessions, persistence, and reconnection.</td><td><a href="session-lifecycle.md">session-lifecycle.md</a></td></tr><tr><td><strong>Turn-taking modes</strong><br>Hands-free vs. push-to-talk — every field and policy explained.</td><td><a href="turn-taking-modes.md">turn-taking-modes.md</a></td></tr><tr><td><strong>Event system</strong><br>Relay components, payload types, and subscription patterns.</td><td><a href="event-system.md">event-system.md</a></td></tr></tbody></table>
