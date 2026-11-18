---
title: Install the project skill
description: Copy the Convai project skill into the location your coding agent scans, then verify that the agent can load the workflow guidance.
last_reviewed: "5.0.0-pre.1"
---

Install a project copy of the `convai-unity-sdk` skill so Claude Code or Codex can discover it. The SDK supplies the original in `AgentSkills/convai-unity-sdk/`.

## Install or update the project copy

1. In Unity, select **Convai > Convai Editor > AI Coding**.
2. Open **Claude Code** or **ChatGPT / Codex**. On **Project skill**, select **Install**. Select **Update** if the row shows **Stale**.
3. If you also use **Project instructions**, select its **Install** or **Update** separately.
4. Open a new agent session in the Unity project and invoke `/convai-unity-sdk` in Claude Code or `$convai-unity-sdk` in Codex. Confirm that the agent can load its task guidance. Verify the tool connection separately with `Convai_GetProjectStatus`.

## Read the project skill status

| State | Meaning | Action |
| --- | --- | --- |
| **Not installed** | No copy in the project. | **Install** |
| **Installed** | The copy matches the source and its stamp. | **Remove** to remove it. |
| **Stale** | The SDK version or packaged skill changed since the copy was made. | **Update** |
| **Locally modified** | The copy differs from its own stamp. | Review your changes before confirming **Replace** or **Remove**. |
| **Unmanaged** | The copy has no valid Convai stamp. | Review your local files before confirming **Replace** or **Remove**. |

Claude Code's copy lives in `.claude/skills/convai-unity-sdk/` and Codex's in `.agents/skills/convai-unity-sdk/`. Each copy has a `.convai-skill.json` stamp that records the SDK and skill versions and the copied files' hashes. If your team commits a project copy, include the stamp with the rest of the folder.

{% content-ref url="supported-coding-agents.md" %}
[Supported coding agents](supported-coding-agents.md)
{% endcontent-ref %}
