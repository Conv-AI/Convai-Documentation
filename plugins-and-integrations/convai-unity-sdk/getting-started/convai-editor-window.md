---
title: The Convai Editor window
description: >-
  Navigate the Convai Editor to project settings, character configuration,
  AI coding tools, memory management, and optional diagnostic sections.
last_reviewed: "5.0.0-preview"
---

Open **Convai > Convai Editor** to access the SDK's project tools. **Convai > Settings** opens the same window directly to Settings. The navigation shows sections enabled in the installed build.

## Navigation

| Section | Use it for |
| --- | --- |
| Welcome | Entry points for setting up and learning the SDK. |
| Account | Account information for the configured credentials. |
| Settings | Project credentials, setup health, runtime defaults and diagnostics. |
| AI Coding | Inspect Unity MCP availability and install the project skill for supported coding assistants. |
| Config Assets | Create and inspect reusable character and room profiles. |
| Long Term Memory | Manage end users and memories; requires API-key access. |
| Live Diagnostics | Runtime diagnostics; appears when inspector developer visibility is enabled. |
| Contact Us | Support and contact links. |

**Server Animation** appears only when `CONVAI_ENABLE_SERVER_ANIMATION` is compiled in. **Updates** appears only with `CONVAI_ENABLE_UPDATES_SECTION`. Their absence is not a failed installation.

<figure><img src="../../../.gitbook/assets/unity-ai-coding.png" alt="Convai Editor navigation with AI Coding selected and assistant installation cards"><figcaption><p>The AI Coding section checks the project integration and exposes assistant-specific setup.</p></figcaption></figure>

## Choose the right configuration surface

Use **Settings** for project-wide credentials and defaults. Use a character's Inspector for its identity, audio and session settings. Use the room manager for conversation input, microphone policy, vision and reconnect behavior. Config Assets provide reusable settings when the corresponding component selects **Profile Asset**.

The Editor window does not replace scene validation or a live connection check. Start with [Validate your setup](validate-your-setup.md) after configuring a scene.

## Related tasks

{% content-ref url="project-settings-reference.md" %}
[Project Settings reference](project-settings-reference.md)
{% endcontent-ref %}

{% content-ref url="../ai-coding-assistant/install-project-skill.md" %}
[Install the project skill](../ai-coding-assistant/install-project-skill.md)
{% endcontent-ref %}

{% content-ref url="../features/long-term-memory/long-term-memory-window.md" %}
[Long Term Memory window](../features/long-term-memory/long-term-memory-window.md)
{% endcontent-ref %}
