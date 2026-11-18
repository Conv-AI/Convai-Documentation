---
title: Conversation flow
description: Understand what the Conversation Flow module tracks in a conversation and why every other embodiment module depends on its timing.
last_reviewed: "5.0.0-pre.1"
---

Conversation Flow is the embodiment module that decides a character's dialogue state — idle, listening, thinking, or speaking — and every other embodiment module reads that state instead of tracking its own version of it. You rarely add it by hand: Convai adds a controller automatically the moment another module needs a dialogue state to read. This page explains what the module owns and why the modules that depend on it behave the way they do.

***

## What Conversation Flow owns

`ConvaiConversationFlowController` (`SDK/Modules/ConversationFlow/Components/ConvaiConversationFlowController.cs`) is the character's single authored source of truth for its dialogue state. It exposes a `Current` reading and a `Changed` event; no other embodiment module redefines or infers its own version of this state. See [Dialogue state](../../core-concepts/dialogue-state.md) for what each of the eight states means and when the character enters it.

***

## How a speaking turn ends

Conversation Flow ends the local speaking performance from the service state or from playback on the device. Body Animation and other embodiment modules use the same dialogue state.

When local endings are enabled, the controller uses two sources of playback evidence.

- **LipSync playback.** If the playback witness reports that the response has finished, Conversation Flow ends the speaking performance immediately. Frames still ahead of the playhead keep it in the speaking state through a pause.
- **Voice audibility.** Without a conclusive LipSync reading, the controller can wait for silence. The default hold is `0.4` seconds. If sound resumes during the hold, the speaking performance continues.

A service end or interruption takes effect immediately. With no local evidence or with local ending disabled, Conversation Flow follows the service state. This timing governs local presentation. Use character and manager events for the conversation lifecycle. See [Conversation flow reference](reference.md#fixed-behavior).

***

## Why every other module reads it

Without a dialogue state to read, Gaze, Body Animation, Body Language, and Emotion cannot tell listening apart from speaking, and fall back to their neutral behavior: eye contact stops differentiating a listening beat from a thinking pause, and gesture and expression intensity stop scaling with speaking energy. Conversation Flow is what turns those otherwise-neutral behaviors into ones that track the actual shape of a conversation.

***

## Convai adds it automatically when needed

A character does not need an authored `ConvaiConversationFlowController` to get one. Body Animation's **Auto-Add Conversation Flow** setting (enabled by default) asks Convai to provision the controller the moment the character needs a dialogue state and none exists yet. Emotion does the same, but only when one of its dialogue-driven touches is actually turned on — its listening lift, thinking look, or reaction accents — since none of them ship enabled by default. Gaze and Body Language also request a controller when none exists, provisioning it in Play mode. When Convai adds one, the Console logs once, naming the character:

```text
[ConvaiConversationFlowController] Added to '<character name>' because an embodiment module on this character needs the dialogue state. Add the component yourself if you want to configure it.
```

An auto-added controller behaves exactly like one you add yourself — see [Configure conversation flow](configure.md) to tune or replace it.

{% hint style="info" %}
The contract behind `Current`, `IConversationFlowSource`, is internal to the package. Read the controller's `Current` property and subscribe to `Changed` directly — do not implement the interface yourself.
{% endhint %}

***

## Explore conversation flow

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Configure conversation flow</strong><br>Add the controller, or rely on auto-creation, then assign a profile to tune its timing.</td><td><a href="configure.md">configure.md</a></td></tr><tr><td><strong>Conversation flow reference</strong><br>The controller's public API, the dialogue-state reading it returns, and every profile field.</td><td><a href="reference.md">reference.md</a></td></tr><tr><td><strong>Troubleshoot conversation flow</strong><br>Diagnose a state stuck on Idle, timing that feels wrong, and multi-character conflicts.</td><td><a href="troubleshooting.md">troubleshooting.md</a></td></tr></tbody></table>

***

## Next steps

{% content-ref url="../../core-concepts/dialogue-state.md" %}
[Dialogue state](../../core-concepts/dialogue-state.md)
{% endcontent-ref %}

{% content-ref url="../../core-concepts/character-embodiment.md" %}
[Character embodiment](../../core-concepts/character-embodiment.md)
{% endcontent-ref %}

{% content-ref url="../how-embodiment-works.md" %}
[How embodiment works](../how-embodiment-works.md)
{% endcontent-ref %}
