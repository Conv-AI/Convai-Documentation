---
title: Convai AgentSkills
description: Reference for the 17 shipped skill documents that teach a connected coding agent how each Convai feature in the plugin behaves.
last_reviewed: "4.0.0-beta.27"
---

Convai AgentSkills are 17 skill assets bundled in the plugin's own `Content/Skills/` folder, each one shipped guidance that teaches a connected coding agent how a Convai feature behaves before it calls a Convai Toolset action or a generic Unreal MCP tool. They are not files a user edits — each skill is a binary `.uasset` that ships with the plugin, carrying a Description and Instructions field an agent reads, not a text file in the project.

{% hint style="info" %}
Requires **Unreal Engine 5.8 or later** and an **Editor** build. Packages built for engine versions below the toolset floor do not contain `Content/Skills/` at all.
{% endhint %}

## How an agent reaches the skills

An agent lists and reads AgentSkills through the engine's `ToolsetRegistry` plugin, using the toolset `ToolsetRegistry.AgentSkillToolset`: it calls `ListSkills` to see what is available, then `GetSkills` to read the ones relevant to the task at hand. `Resources/AgentPrimer/ConvaiAgentPrimer.md` — the primer a coding agent's context file can carry — instructs the agent to list and read the skills this way before building anything Convai-related, and names `ConvaiQuickStart`, `ConvaiActions`, `ConvaiSceneObjects`, `ConvaiDynamicContext`, and `ConvaiPlayerAndInput` as the ones to read first.

To confirm an agent can see the skills, ask it to list its available MCP tools and call `ListSkills` — a working setup returns all 17 skill names.

## All 17 skills

| Skill | Covers |
|---|---|
| `ConvaiQuickStart` | The fast setup path: talking, following or moving a character, and adding custom actions |
| `ConvaiProjectSetup` | Setting up a project for Convai — installing and wiring the plugin |
| `ConvaiMetahumanSetup` | Turning a MetaHuman character into a Convai character |
| `ConvaiCharacterReference` | The chatbot and player components and their configuration |
| `ConvaiConversation` | Conversation and session lifecycle |
| `ConvaiActions` | Configuring character actions on a chatbot |
| `ConvaiCustomActions` | Authoring custom action handlers in a Blueprint event graph |
| `ConvaiSimpleAnimationActions` | Simple built-in animation actions |
| `ConvaiDynamicContext` | Live events, response policy, delivery, and flushing for dynamic context |
| `ConvaiSceneObjects` | Tracked properties and movement awareness on scene objects |
| `ConvaiGazeAttention` | The gaze attention system |
| `ConvaiNarrativeDesign` | Narrative design sections and triggers |
| `ConvaiPlayerAndInput` | Microphone and session setup, and the player speaking lifecycle |
| `ConvaiVision` | The vision feature |
| `ConvaiFaceAndAnimation` | Face sync and lip sync configuration |
| `ConvaiExpressiveness` | Character emotion and expressiveness |
| `ConvaiRestAndAudioUtilities` | REST and audio utility helpers |

## Next steps

{% content-ref url="README.md" %}
[AI coding assistant](README.md)
{% endcontent-ref %}

{% content-ref url="quick-start.md" %}
[AI coding assistant quick start](quick-start.md)
{% endcontent-ref %}

{% content-ref url="convai-toolset-reference.md" %}
[Convai Toolset reference](convai-toolset-reference.md)
{% endcontent-ref %}
