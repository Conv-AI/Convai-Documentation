---
title: AI coding assistant quick start
description: >-
  Open AI Coding Setup, accept the Unity MCP terms, install a coding agent's
  instructions, and verify Convai's MCP tools are ready.
last_reviewed: "4.4.0"
---

Convai extends Unity's MCP server with SDK-aware tools so a coding agent such as Codex, Claude Code, or Cursor can configure Convai components directly in your project. Use this quick start the first time you connect an agent to a project that already has the Convai Unity SDK installed. At the end, your agent has managed instructions installed and the AI Coding Setup window reports every Convai tool as registered.

## Prerequisites

* Unity <code class="expression">space.vars.unity_recommended_version</code> or later — Convai's AI coding tools require Unity 6000 or newer.
* The Convai Unity SDK installed in the project. See [Install the Convai Unity SDK](../getting-started/installation.md).
* A compatible Unity AI Assistant package (`com.unity.ai.assistant`, version `2.13.0-pre.2` or later, below `3.0.0`). Install it manually, or install it from inside this walkthrough.
* A supported coding agent installed on your machine, such as Codex CLI, Claude Code, or Cursor. See [Supported coding agents](supported-coding-agents.md) for the full list.

## Open AI Coding Setup

{% stepper %}
{% step %}
### Open the Convai AI Coding Setup window

In the Unity Editor menu bar, select **Convai > AI Coding Setup**.

The window reports four readiness checks: **Unity 6000+**, **Unity AI Assistant**, **Packaged Convai skill**, and **Convai tools**. A checkmark next to a row means it is ready; an exclamation mark means it needs attention.
{% endstep %}

{% step %}
### Accept the Unity MCP terms

Unity may prompt you to accept the Unity AI Assistant and MCP server terms of service the first time the feature activates in this project. Accept the prompt so Unity's MCP server and Convai's tools can register.
{% endstep %}

{% step %}
### Resolve any row that shows a warning

Each unready row has a **Fix** button. Click **Fix** next to **Unity AI Assistant** to install `com.unity.ai.assistant@2.14.0-pre.1` through Package Manager — Unity recompiles and the row updates automatically. Click **Fix** next to **Packaged Convai skill** or **Convai tools** to refresh package assets and re-register Convai's tools without reinstalling the Assistant package.
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
**Fix** buttons are disabled while Unity is compiling, updating packages, or in Play Mode. Exit Play Mode first — repair never exits Play Mode for you.
{% endhint %}

## Install your coding agent's managed instructions

{% stepper %}
{% step %}
### Choose your coding agent

Scroll to **Managed project instructions**. Convai lists each supported agent with the file it manages — for example `AGENTS.md` for Codex, `CLAUDE.md` for Claude Code, and `.cursor/rules/convai-unity-sdk.mdc` for Cursor. See [Supported coding agents](supported-coding-agents.md) for the complete list and per-agent notes.
{% endstep %}

{% step %}
### Install the managed instructions

Click **Install** next to your agent. Convai writes a sentinel-delimited block, marked by `<!-- BEGIN CONVAI UNITY SDK -->` and `<!-- END CONVAI UNITY SDK -->`, into that agent's file without disturbing any existing content. The button changes to **Update** once the block exists, and **Remove** becomes available to delete it later.
{% endstep %}
{% endstepper %}

The managed instructions direct your agent to read `Packages/com.convai.convai-sdk-for-unity/AIAssistantSkills/convai-unity-sdk/SKILL.md` and its linked references, use Unity's generic MCP tools for GameObjects, scripts, and scenes, and use Convai's tools for SDK configuration and diagnosis.

## Verify the tool count

The **Convai tools** row in the AI Coding Setup window reads `20/20 registered` once Unity's MCP registry has registered all twenty Convai tools under tool contract version 4. If the count is lower or the row lists a missing or unexpected tool name, click **Fix** next to **Convai tools** to refresh the registry and recompile.

{% hint style="success" %}
Setup is complete when all four rows show a checkmark and **Convai tools** reads `20/20 registered`.
{% endhint %}

## Prompt the agent to build your scene

With managed instructions installed and the tool count verified, prompt your agent in plain language. Convai's tools handle SDK-specific configuration; your agent's Unity MCP tools handle generic GameObjects, scripts, and scene operations.

| Task | Example prompt |
|---|---|
| Build a scene | "Set up a training-simulation room with a Convai Player and a Convai Character named Instructor." |
| Add the chat UI | "Add the shipped chat UI to the scene so the transcript is visible during the conversation." |
| Switch push-to-talk or hands-free | "Switch the room to Push to Talk input mode." |
| Add objects | "Add a red fire extinguisher GameObject next to the workbench." |
| Enable vision | "Turn on vision for the Instructor character so it can see the workbench." |

Vision setup is not one of Convai's twenty foundation tools, so your agent configures it by editing `ConvaiRoomManager` and adding `ConvaiVisionPublisher` directly. See [Vision quick start](../features/vision/quick-start.md) for the exact fields it sets.

## What to try next

Prompt your agent for two or three of the tasks above in your own project, and check the resulting scene in the Hierarchy before entering Play Mode.

{% content-ref url="supported-coding-agents.md" %}
[Supported coding agents](supported-coding-agents.md)
{% endcontent-ref %}

{% content-ref url="mcp-tools-reference.md" %}
[MCP tools reference](mcp-tools-reference.md)
{% endcontent-ref %}

{% content-ref url="troubleshooting.md" %}
[Troubleshoot AI coding assistant setup](troubleshooting.md)
{% endcontent-ref %}
