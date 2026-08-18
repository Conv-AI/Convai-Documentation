---
title: Supported coding agents
description: Reference for the five coding agents AI coding setup supports, including each agent's context file, terminal support, and options.
last_reviewed: "4.0.0-beta.27"
---

`EConvaiMcpAgent` lists five coding agents that **Set Up AI Coding (MCP)** can configure: `Claude Code`, `Cursor`, `VS Code`, `Gemini`, and `Codex`. Use this reference to find the exact context file, terminal behavior, and agent-specific options for each one.

## Agents and context files

| Agent | Context file | Location | Terminal configuration | CLI command |
|---|---|---|---|---|
| `Claude Code` | `CLAUDE.md` | Project root | Available | `claude` |
| `Cursor` | `.cursor/rules/convai.mdc` | `.cursor/rules/` directory | Not available (GUI app) | — |
| `VS Code` | `.github/copilot-instructions.md` | `.github/` directory | Not available (GUI app) | — |
| `Gemini` | `GEMINI.md` | Project root | Available | `gemini` |
| `Codex` | `AGENTS.md` | Project root | Available; also has the auto-approve option below | `codex` |

`Claude Code`, `Codex`, and `Gemini` are CLI agents — the setup dialog's terminal option is only enabled for these three, and it writes the exact `claude`, `codex`, or `gemini` command as the terminal's startup line. `Cursor` and `VS Code` are GUI apps, so the terminal option is disabled when either is selected.

## How the primer is written to the context file

When you enable **Add Convai instructions to the agent's context file**, the plugin copies the Convai primer from `Resources/AgentPrimer/ConvaiAgentPrimer.md` into the agent's context file, wrapped between two sentinel comments:

```html
<!-- >>> Convai primer (managed by Convai; edits between sentinels are overwritten) -->
...primer content...
<!-- <<< Convai primer -->
```

Re-running setup with the same agent finds the existing sentinel-delimited block and replaces only what is between the sentinels, so content you add outside the block is preserved. If the context file does not yet contain a Convai block, the write mode you choose in the dialog decides what happens:

| Write mode | Behavior | Default |
|---|---|---|
| Append | Adds the sentinel-delimited block to the end of the file, preserving any existing content. | Yes |
| Replace | Overwrites the file with only the sentinel-delimited block. | No |

## Codex auto-approve

`Codex` has one option no other agent has: **Let Codex run unattended with no approval prompts (bypasses Codex's sandbox)**, off by default. Enabling it changes the terminal launch line from `codex` to `codex --dangerously-bypass-approvals-and-sandbox`, so Codex executes every command with no approval prompt and no sandbox. This option only appears when `Codex` is the selected agent, and it has no effect unless the terminal option is also enabled.

## Next steps

{% content-ref url="README.md" %}
[AI coding assistant](README.md)
{% endcontent-ref %}

{% content-ref url="quick-start.md" %}
[AI coding assistant quick start](quick-start.md)
{% endcontent-ref %}

{% content-ref url="convai-agent-skills.md" %}
[Convai AgentSkills](convai-agent-skills.md)
{% endcontent-ref %}
