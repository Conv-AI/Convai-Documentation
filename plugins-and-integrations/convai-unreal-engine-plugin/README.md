---
title: Convai Unreal Engine plugin
description: "Find installation guides, feature documentation, Blueprint reference, and troubleshooting pages for the Convai Unreal Engine plugin."
---

The Convai Unreal Engine plugin connects Unreal Engine 5 projects to Convai, enabling actors in a scene to hold real-time voice and text conversations, express emotions, animate their faces in sync with speech, and respond to player actions. It is Blueprint-first: every feature is accessible from Blueprint graphs without writing C++. The current release is <code class="expression">space.vars.unreal_plugin_version</code>, supporting Unreal Engine <code class="expression">space.vars.unreal_min_version</code> and later on Win64 and Android.

{% hint style="info" %}
**New to the plugin?** Follow [Getting started](getting-started/) to install, configure your API key, and run your first AI character.
{% endhint %}

### Learn the plugin

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Overview</strong><br>What the plugin is, how its modules are structured, and a map of every feature.</td><td><a href="overview/">overview</a></td></tr><tr><td><strong>Compatibility and requirements</strong><br>UE 5.x version support, platform targets, and character rig compatibility.</td><td><a href="compatibility-and-requirements/">compatibility-and-requirements</a></td></tr><tr><td><strong>Getting started</strong><br>Install the plugin, configure your API key, and add your first AI character.</td><td><a href="getting-started/">getting-started</a></td></tr></tbody></table>

### Features

Each feature is opt-in and builds on the core components.

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Lip sync</strong><br>Drives mouth and facial blendshapes from response audio in real time.</td><td><a href="features/lip-sync/">lip-sync</a></td></tr><tr><td><strong>Emotion</strong><br>Convai infers emotion from conversation and drives blendshape expressions.</td><td><a href="features/emotion/">emotion</a></td></tr><tr><td><strong>Character actions</strong><br>Characters execute typed in-scene commands (Move To, Follow, custom).</td><td><a href="features/character-actions/">character-actions</a></td></tr><tr><td><strong>Dynamic context</strong><br>Push live world state and events into character knowledge at runtime.</td><td><a href="features/dynamic-context/">dynamic-context</a></td></tr><tr><td><strong>Narrative design</strong><br>Trigger scripted conversation branches and sections by name from Blueprint.</td><td><a href="features/narrative-design/">narrative-design</a></td></tr><tr><td><strong>Long-term memory</strong><br>Characters remember each player across sessions using an end-user ID.</td><td><a href="features/long-term-memory/">long-term-memory</a></td></tr><tr><td><strong>Scene metadata</strong><br>Tag level actors so characters are aware of and can act on them.</td><td><a href="features/scene-metadata/">scene-metadata</a></td></tr><tr><td><strong>Vision</strong><br>Stream camera frames to Convai so characters can describe what they see.</td><td><a href="features/vision/">vision</a></td></tr><tr><td><strong>Gaze attention</strong><br>Route the object under the player's crosshair as context to the active character.</td><td><a href="features/gaze-attention/">gaze-attention</a></td></tr></tbody></table>

### Reference

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Blueprint reference</strong><br>Full property, function, and event surface for all components.</td><td><a href="blueprint-reference/">blueprint-reference</a></td></tr><tr><td><strong>The Convai editor window</strong><br>Sign in, browse samples, and export diagnostic logs from within the editor.</td><td><a href="editor-window/">editor-window</a></td></tr><tr><td><strong>Troubleshooting</strong><br>Common failure modes, diagnostic steps, and known issues.</td><td><a href="troubleshooting/">troubleshooting</a></td></tr></tbody></table>

### Latest release

<code class="expression">space.vars.unreal_plugin_version</code> introduces gesture and pointing animations triggered automatically by LLM-issued character actions, `UConvaiObjectComponent` for tagging level actors with live scene properties, gaze-driven attention with silhouette highlight and on-screen cursor, and fuzzy enum matching so minor AI spelling variations no longer drop action parameters. See [Release notes](overview/release-notes.md) for the full changelog.

### Next steps

{% content-ref url="getting-started/" %}
[getting-started](getting-started/)
{% endcontent-ref %}
