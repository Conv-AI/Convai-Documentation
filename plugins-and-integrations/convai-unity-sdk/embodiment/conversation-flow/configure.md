---
title: Configure conversation flow
description: Add the Conversation Flow module to a character, or let Convai auto-create it, then assign a profile to tune its timing.
last_reviewed: "5.0.0-preview"
---

Add `ConvaiConversationFlowController` to a character yourself, or let Convai add it automatically, then assign a `ConvaiConversationFlowProfile` to change how quickly it moves between dialogue states. Use this page once you want direct control over the module's timing instead of relying on its built-in defaults.

***

## Prerequisites

- A `ConvaiCharacter` in your scene.
- Optional but recommended: an embodiment module that reads dialogue state — Gaze, Body Animation, Body Language, or Emotion — already added, so tuning Conversation Flow has a visible effect. Conversation Flow alone changes nothing about how the character looks; it only tracks state for the other modules to read.

{% hint style="info" %}
You rarely need this page for its first step. If your character already has Body Animation with **Auto-Add Conversation Flow** enabled (the default), Convai adds the controller for you the first time it is needed. Gaze and Body Language also request one automatically in Play mode. Skip to [Assign a profile](#assign-a-profile) if that is your situation.
{% endhint %}

***

## Add the controller

{% stepper %}
{% step %}
### Select the character

In the Hierarchy, select the `GameObject` that carries the `ConvaiCharacter` component.
{% endstep %}

{% step %}
### Add the Conversation Flow component

In the Inspector, select **Add Component**, then **Convai > Embodiment > Conversation Flow**. This adds `ConvaiConversationFlowController`.

Convai also adds the shared infrastructure the module needs — an `EmbodimentContext` — automatically. You do not add this yourself.
{% endstep %}

{% step %}
### Leave the profile unassigned to start

With no profile assigned, the component's **Profile** section shows an **Using SDK Defaults** notice and the controller runs on built-in timing values, which work. Assign a profile only once you want to change the pace.
{% endstep %}
{% endstepper %}

***

## Assign a profile

{% stepper %}
{% step %}
### Create a profile asset

Select **Assets > Create > Convai > Embodiment > Conversation Flow Profile**. This creates a `ConvaiConversationFlowProfile` asset.
{% endstep %}

{% step %}
### Assign it to the controller

Select the character and drag the profile asset onto the **Flow Profile** field in the component's **Profile** section.
{% endstep %}

{% step %}
### Tune the timing fields

Open the profile asset and adjust its fields under **Transition**, **Dialogue Beats**, and **Energy** — for example, lower **Thinking Max Hold** to return from the local Thinking presentation to Attending sooner, or raise **Idle Return Delay** to keep the character attentive longer between turns. These settings do not reduce backend response latency. See [Conversation flow reference](reference.md) for every field, its range, and its default.
{% endstep %}
{% endstepper %}

A profile asset can be shared across multiple characters. Editing it changes the timing for every character it is assigned to.

***

## Verify the setup

Enter Play mode, select the character, and expand the **Live** section on the `ConvaiConversationFlowController` component (or open **Convai > Embodiment Editor**, select the **Live** tab). Start a conversation and confirm **State** moves through `Listening`, `Thinking`, and `Speaking` as the conversation progresses, instead of staying on `Idle`.

{% hint style="success" %}
**Expected result:** **State** changes away from `Idle` shortly after you start speaking, and **Time In State** resets on each state change.
{% endhint %}

***

The component's **Live** section also shows **Blend To**, **Blend**, **Energy Level**, **Heard By**, **Ended By**, and **Service Late**. **Heard By** identifies Lip Sync, Voice, or Service Only evidence. **Ended By** identifies Voice, Lip Sync, or Service; **Service Late** reports the observed lag in milliseconds when available. These extra evidence fields belong to the component Inspector, not the Embodiment Editor's Conversation section.

## Troubleshooting

If **State** never leaves `Idle`, or the character lingers in a state longer than the profile's values suggest it should, see [Troubleshoot conversation flow](troubleshooting.md).

***

## Next steps

{% content-ref url="reference.md" %}
[Conversation flow reference](reference.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting.md" %}
[Troubleshoot conversation flow](troubleshooting.md)
{% endcontent-ref %}

{% content-ref url="../embodiment-presets.md" %}
[Embodiment presets](../embodiment-presets.md)
{% endcontent-ref %}
