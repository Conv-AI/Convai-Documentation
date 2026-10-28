---
title: AI coding assistant
description: Find guides for connecting AI coding agents to Unity through Convai's SDK-aware MCP tools, including setup, supported agents, and troubleshooting.
last_reviewed: "5.0.0-preview"
---

The Convai AI coding assistant integration adds Convai-specific tools to Unity's official MCP server, so a coding agent can inspect, configure, and diagnose Convai components in your project instead of you wiring them by hand. Use it if you already work with a supported coding agent and want that agent to understand Convai rooms, characters, actions, lip sync, embodiment modules such as gaze and emotion, transcripts, and vision. Once connected, you prompt the agent in natural language and review the resulting changes in the Unity Editor.

{% hint style="info" %}
**Before you begin:** The integration requires <code class="expression">space.vars.unity_recommended_version</code> or newer and a compatible `com.unity.ai.assistant` package. See [AI coding assistant quick start](quick-start.md) for the full prerequisite check and setup walkthrough.
{% endhint %}

## What the integration adds

Unity's official MCP server, provided by the `com.unity.ai.assistant` package, gives a coding agent generic tools for GameObjects, scripts, assets, and scene operations, but no knowledge of Convai components. The Convai Unity SDK adds 47 SDK-aware tools (contract version 10) with a `Convai.*` name prefix — for example `Convai.ConfigureCharacter`, `Convai.ConfigureLipSync`, `Convai.ConfigureGaze`, `Convai.DiagnoseConversation`, and `Convai.ConfigureConversationTargeting` — that read and mutate only Convai components such as `ConvaiManager`, characters, actions, lip sync, embodiment modules (gaze, body animation, body language, emotion), transcripts, narrative sections, and which character in a multi-character room the player is addressing. Unity MCP tools continue to own generic GameObjects, scripts, and scene operations. Convai tools never accept or return API keys. Scene-authoring tools use Unity Undo and leave scenes unsaved. `Convai.SetCharacterMemorySettings` instead changes settings on the Convai service for every app using that character; it previews by default and has no Unity Undo.

## Supported coding agents

The **Claude Code** and **ChatGPT / Codex** cards install a project copy of the `convai-unity-sdk` skill, with optional project instructions. **Other AI Clients** installs instructions for Cursor, Gemini, and VS Code Copilot. See [Supported coding agents](supported-coding-agents.md) for paths and [Install the project skill](install-project-skill.md) for update behavior.

## Connect a coding agent to your project

Open **Convai > Convai Editor > AI Coding**. **Setup Health** checks Unity, Unity AI Assistant, the packaged skill, and the tool catalog. Three additional read-only rows report Claude MCP configuration, the ChatGPT / Codex app, and the Unity plugin for Codex. Use **Open Unity MCP Server Settings** to configure the client connection in Unity, then install the project skill or instructions for that client. A detected client installation does not establish a live connection. Follow the [quick start](quick-start.md) to verify a read-only tool call from your agent.

## What you can ask a connected agent to do

With a coding agent connected, prompt it in natural language instead of wiring components manually. Typical requests include:

* Build a conversation scene with a player and a character
* Add chat UI to display the conversation transcript
* Switch between push-to-talk and hands-free conversation input
* Add objects to the scene for a character to reference
* Enable vision so a character can see the scene
* Configure gaze, body animation, body language, or emotion for a character
* Add a second character to a room and configure how the SDK decides which one the player is addressing
* Configure a group conversation for an enabled preview deployment
* Read a character's long-term memory settings, or preview an explicitly requested change

The agent uses Convai tools for Convai components and Unity's own MCP tools for generic GameObjects, scripts, and scene operations, then reports which instance IDs it changed. See [MCP tools reference](mcp-tools-reference.md) for the complete list of Convai tools available to the agent.

## AI coding assistant pages

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>AI coding assistant quick start</strong><br>Connect a coding agent to your Unity project and verify the setup end to end.</td><td><a href="quick-start.md">quick-start.md</a></td></tr><tr><td><strong>Supported coding agents</strong><br>Find the exact instruction file path and install behavior for each of the five supported agents.</td><td><a href="supported-coding-agents.md">supported-coding-agents.md</a></td></tr><tr><td><strong>MCP tools reference</strong><br>Reference every Convai tool exposed to a coding agent, including its purpose and default enabled state.</td><td><a href="mcp-tools-reference.md">mcp-tools-reference.md</a></td></tr><tr><td><strong>Troubleshoot AI coding assistant setup</strong><br>Fix setup, tool registration, and agent connection failures.</td><td><a href="troubleshooting.md">troubleshooting.md</a></td></tr><tr><td><strong>Install the project skill</strong><br>Install, update, or replace a Claude Code or Codex project skill.</td><td><a href="install-project-skill.md">install-project-skill.md</a></td></tr></tbody></table>
