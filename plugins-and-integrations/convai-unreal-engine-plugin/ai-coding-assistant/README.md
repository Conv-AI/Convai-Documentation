---
title: AI coding assistant
description: Connect a supported coding agent to the Unreal Editor so it can set up Convai characters and read Convai's skill library for you.
last_reviewed: "4.0.0-beta.27"
---

The Convai Unreal Engine plugin registers the Convai Toolset with the engine's own Model Context Protocol (MCP) plugin, adding seven Convai-specific editor actions and a library of Convai skill documents that a connected coding agent can read and call. Use this section once the Convai plugin is installed and you want a coding agent such as Claude Code or Cursor to set up Convai characters, players, and actions inside your Unreal project instead of you wiring them by hand.

{% hint style="info" %}
**Before you begin:** AI coding support requires **Unreal Engine 5.8 or later** and only exists in **Editor** builds — the `ConvaiToolset` module throws a build error on any non-Editor target. On UE 5.0–5.7 the plugin still compiles, but the AI coding tooling is not present. See [AI coding assistant quick start](quick-start.md) for the full setup walkthrough.
{% endhint %}

## What the Convai Toolset adds

The engine's `ModelContextProtocol` plugin already gives a connected coding agent generic MCP tools for editing a project. The Convai Toolset adds seven AI-callable editor actions on top of that — `SetupConvaiCharacter`, `SetupConvaiPlayer`, `SetupConvaiPawnMovement`, `AddNavMeshVolumeForCurrentLevel`, `SetBlueprintPropertyAndPropagate`, `AddConvaiAction`, and `CreateConvaiActionHandler` — registered with the engine's `ToolsetRegistry` plugin. See [Convai Toolset reference](convai-toolset-reference.md) for what each action does and its parameters.

The plugin also ships 17 skill documents under `Content/Skills/` in the plugin's own content, which an agent lists and reads through the toolset's `AgentSkillToolset` (`ListSkills` and `GetSkills`). These documents describe Convai workflows such as project setup, MetaHuman setup, actions, and dynamic context, so an agent can look up how a feature works before calling a toolset action. See [Convai AgentSkills](convai-agent-skills.md) for the full list.

## Supported coding agents

Setup supports five agents: `Claude Code`, `Cursor`, `VS Code`, `Gemini`, and `Codex`. Each agent gets its own project-root context file — for example `CLAUDE.md` for Claude Code — with a sentinel-delimited Convai primer block when you choose to add one. See [Supported coding agents](supported-coding-agents.md) for the exact file and per-agent behavior.

## Connect a coding agent to your project

Open the Convai editor window, click the **Settings** icon, and select **Set Up AI Coding (MCP)**. Choose an agent, set the setup options, and restart the editor when prompted. See [AI coding assistant quick start](quick-start.md) for the full walkthrough and verification steps.

## Not the same as a character's own MCP connections

This section covers a coding agent calling Convai's editor tools while you build a project in the Unreal Editor. It is a different subject from [MCP Servers](../../../convai-playground/character-customization/mcp-servers.md), which covers a Convai character calling an external MCP server during a live conversation with a player.

## AI coding assistant pages

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>AI coding assistant quick start</strong><br>Open Set Up AI Coding (MCP), pick an agent, and verify the setup end to end.</td><td><a href="quick-start.md">quick-start.md</a></td></tr><tr><td><strong>Supported coding agents</strong><br>Find the context file, terminal support, and agent-specific options for each of the five supported agents.</td><td><a href="supported-coding-agents.md">supported-coding-agents.md</a></td></tr><tr><td><strong>Convai Toolset reference</strong><br>Reference for the seven AI-callable editor actions and their parameters.</td><td><a href="convai-toolset-reference.md">convai-toolset-reference.md</a></td></tr><tr><td><strong>Convai AgentSkills</strong><br>Reference for the 17 shipped skill documents and how an agent lists and reads them.</td><td><a href="convai-agent-skills.md">convai-agent-skills.md</a></td></tr></tbody></table>
