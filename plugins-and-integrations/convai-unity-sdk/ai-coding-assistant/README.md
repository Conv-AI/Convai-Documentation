---
title: AI coding assistant
description: Connect a coding agent to an open Unity project and use Convai tools to inspect, configure, and diagnose conversational characters.
last_reviewed: "5.0.0-pre.1"
---

The Convai Unity SDK adds project-specific tools to Unity CLI MCP, Unity's Model Context Protocol server. Use a connected coding agent to inspect, configure, and diagnose Convai rooms, characters, Actions, LipSync, and embodiment in the open Unity Editor.

<table data-view="cards">
<thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead>
<tbody>
<tr><td><strong>AI coding assistant quick start</strong><br>Install Pipeline, connect a client, and verify a tool call.</td><td><a href="quick-start.md">quick-start.md</a></td></tr>
<tr><td><strong>Supported coding agents</strong><br>Find the connection and project instruction options for your client.</td><td><a href="supported-coding-agents.md">supported-coding-agents.md</a></td></tr>
<tr><td><strong>Install the project skill</strong><br>Copy the SDK's workflow guidance to a location your agent discovers.</td><td><a href="install-project-skill.md">install-project-skill.md</a></td></tr>
<tr><td><strong>MCP tools reference</strong><br>Look up tool names, inputs, results, and operating limits.</td><td><a href="mcp-tools-reference.md">mcp-tools-reference.md</a></td></tr>
<tr><td><strong>Troubleshoot AI coding assistant setup</strong><br>Resolve missing Pipeline commands, client configuration, or skill files.</td><td><a href="troubleshooting.md">troubleshooting.md</a></td></tr>
</tbody>
</table>

## How the pieces fit together

| Piece | Responsibility |
| --- | --- |
| Unity CLI MCP (`unity mcp`) with the `com.unity.pipeline` package | Connects the client to the open Editor and exposes Unity's general-purpose commands and the SDK's `Convai_*` tools. |
| Project skill and managed instructions | Give the agent the SDK workflows and project rules. Install or update each from **Convai > Convai Editor > AI Coding**. |
| Standalone Convai Unity coding-agent plugin | Offers a separate setup skill for preparing a new or existing project and packages a particular SDK skill snapshot. Install the SDK separately in Unity and check tool compatibility against the project you open. [Convai Unity coding-agent plugin repository](https://github.com/Conv-AI/convai-unity-agent-plugin) |

## Play Mode, scene saves, and NavMesh bakes

Convai scene-authoring tools preview by default. They apply changes through Unity Undo in Edit Mode and leave scenes open for you or your agent to save. The project skill tells the agent to save scenes it changes, enter or exit Play Mode, and bake a NavMesh when the task calls for those steps and your instructions allow them. For a diagnosis-only task, the agent can reproduce the issue in Play Mode and report the findings.

Live-room tools that change runtime state require Play Mode and an explicit `dryRun=false`. Convai tools never accept or return API keys. Transcript text requires a separate opt-in on tools that can inspect it.
