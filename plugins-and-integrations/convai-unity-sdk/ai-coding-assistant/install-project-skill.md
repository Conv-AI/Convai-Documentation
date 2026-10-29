---
title: Install the project skill
description: Install and update the Convai Unity SDK project skill for Claude Code or Codex, preserving local changes and checking the client connection.
last_reviewed: "5.0.0-preview"
---

Install a project copy of `convai-unity-sdk` so Claude Code or ChatGPT / Codex can find the SDK's scene setup and diagnosis guidance. The project skill is separate from the Unity MCP connection and from optional instruction files.

## Before you begin

Install the SDK and resolve the four readiness checks in the [AI coding quick start](quick-start.md). The packaged skill must exist before it can be copied. Configure the client connection in **Project Settings > AI > Unity MCP Server**.

## Install or update

1. Open **Convai > Convai Editor > AI Coding**.
2. Find the **Claude Code** or **ChatGPT / Codex** card and inspect **Project skill**.
3. Use the action for its state:

| State | Action | Effect |
|---|---|---|
| Not installed | Install | Copy the packaged skill and references into the client directory. |
| Installed | Reinstall | Refresh an unchanged managed copy. |
| Stale | Update | Replace an unchanged older copy with the current packaged content. |
| Locally modified | Replace | Confirm replacement of a copy changed since installation. Preserve any wanted edits first. |
| Unmanaged | Replace | Confirm replacement of a directory without a valid Convai installation stamp. |

Claude Code uses `.claude/skills/convai-unity-sdk/`; Codex uses `.agents/skills/convai-unity-sdk/`. The `.convai-skill.json` stamp tracks the installed source and content. Do not edit the stamp to hide a local modification.

4. Optionally install or update **Project instructions**. Once the skill is installed, the managed block names it. Updating that block preserves other instructions in the file. The row reads **Installed** for any managed block, including one written by an earlier SDK build, so click **Update** to replace it with the current text.
5. Click **Refresh**, reconnect your client if needed, and ask it to read the installed skill and call `Convai.GetProjectStatus`.

{% hint style="info" %}
The project skill and the managed instructions update separately for each client. Updating the skill does not update an existing instruction block. Copies that predate the current rule tell the agent to wait for an explicit request before entering or exiting Play Mode, saving a scene, or baking a NavMesh. The current rule has the agent do these when the task needs them, unless you restrict them. See [Play Mode, scene saves, and NavMesh bakes](README.md#play-mode-scene-saves-and-navmesh-bakes).
{% endhint %}

## Verify

**Project skill** should read **Installed**. A successful status call with contract version `11` establishes that this 5.0 preview's tools are reachable; the skill's Installed status alone does not. Ask the client to run `Convai.InspectScene` before any target-specific configuration.

If you installed project instructions, open the client's instruction file and check that the block between `<!-- BEGIN CONVAI UNITY SDK -->` and `<!-- END CONVAI UNITY SDK -->` contains the sentence `Enter or exit Play Mode, save the scenes you changed, and bake a NavMesh whenever the task needs it`. A block without it is from an earlier SDK build.

Use **Remove** on the relevant row to remove the managed skill copy or instruction block. They are separate operations; removing instructions does not disconnect Unity MCP or uninstall the SDK.

## Next steps

See [Supported coding agents](supported-coding-agents.md) for managed file paths and [Troubleshooting](troubleshooting.md) for unreadable instructions, relay detection, and registration failures.
