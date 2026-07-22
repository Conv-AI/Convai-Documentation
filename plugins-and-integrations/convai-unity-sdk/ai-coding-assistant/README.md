---
title: AI coding assistant
description: Find guides for connecting AI coding agents to Unity through Convai's SDK-aware MCP tools, including setup, supported agents, and troubleshooting.
last_reviewed: "4.4.0"
---

The Convai AI coding assistant integration adds Convai-specific tools to Unity's official MCP server, so a coding agent can inspect, configure, and diagnose Convai components in your project instead of you wiring them by hand. Use it if you already work with a supported coding agent and want that agent to understand Convai rooms, characters, actions, lip sync, transcripts, and vision. Once connected, you prompt the agent in natural language and review the resulting changes in the Unity Editor.

{% hint style="info" %}
**Before you begin:** The integration requires <code class="expression">space.vars.unity_recommended_version</code> or newer and a compatible `com.unity.ai.assistant` package. See [Set up your first coding agent](quick-start.md) for the full prerequisite check and setup walkthrough.
{% endhint %}

## What the integration adds

Unity's official MCP server, provided by the `com.unity.ai.assistant` package, gives a coding agent generic tools for GameObjects, scripts, assets, and scene operations, but no knowledge of Convai components. The Convai Unity SDK adds 20 SDK-aware tools with a `Convai.*` name prefix — for example `Convai.ConfigureCharacter`, `Convai.ConfigureLipSync`, and `Convai.DiagnoseConversation` — that read and mutate only Convai components such as `ConvaiManager`, characters, actions, lip sync, transcripts, and narrative sections. Unity MCP tools continue to own generic GameObjects, scripts, and scene operations. Convai tools never accept or return API keys, and mutating Convai tools use Unity's Undo system instead of saving scenes automatically.

## Supported coding agents

The integration supports five coding agents: Codex, Claude Code, Cursor, Gemini, and VS Code Copilot. Installing support for an agent writes a managed Convai instruction block into that agent's own instructions file — `AGENTS.md` for Codex, `CLAUDE.md` for Claude Code, `.cursor/rules/convai-unity-sdk.mdc` for Cursor, `GEMINI.md` for Gemini, and `.github/copilot-instructions.md` for VS Code Copilot — pointing the agent at the packaged `convai-unity-sdk` skill. See [Supported coding agents](supported-coding-agents.md) for the exact file paths and per-agent install behavior.

## Connect a coding agent to your project

Open **Convai > AI Coding Setup** in the Unity Editor menu to start. This opens the **AI Coding** section of the Convai Editor window, whose **Setup Health** card checks <code class="expression">space.vars.unity_recommended_version</code> or newer, a compatible `com.unity.ai.assistant` package, the packaged Convai skill, and the 20-tool contract, with inline **Fix** buttons for any check that fails. Open **Project Settings > AI > Unity MCP Server** — directly, or through the **Open Unity MCP Server Settings** button in the same section — to accept Unity's terms for the MCP Server feature and confirm which MCP clients are connected to your project. Then click **Install** next to a supported coding agent in the **Managed Project Instructions** card to write its managed instruction block. See [Set up your first coding agent](quick-start.md) for the full walkthrough.

## What you can ask a connected agent to do

With a coding agent connected, prompt it in natural language instead of wiring components manually. Typical requests include:

* Build a conversation scene with a player and a character
* Add chat UI to display the conversation transcript
* Switch between push-to-talk and hands-free conversation input
* Add objects to the scene for a character to reference
* Enable vision so a character can see the scene

The agent uses Convai tools for Convai components and Unity's own MCP tools for generic GameObjects, scripts, and scene operations, then reports which instance IDs it changed. See [MCP tools reference](mcp-tools-reference.md) for the complete list of Convai tools available to the agent.

## AI coding assistant pages

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Set up your first coding agent</strong><br>Connect a coding agent to your Unity project and verify the setup end to end.</td><td><a href="quick-start.md">quick-start.md</a></td></tr><tr><td><strong>Supported coding agents</strong><br>Find the exact instruction file path and install behavior for each of the five supported agents.</td><td><a href="supported-coding-agents.md">supported-coding-agents.md</a></td></tr><tr><td><strong>MCP tools reference</strong><br>Reference every Convai tool exposed to a coding agent, including its purpose and default enabled state.</td><td><a href="mcp-tools-reference.md">mcp-tools-reference.md</a></td></tr><tr><td><strong>Troubleshoot the AI coding assistant</strong><br>Fix setup, tool registration, and agent connection failures.</td><td><a href="troubleshooting.md">troubleshooting.md</a></td></tr></tbody></table>
