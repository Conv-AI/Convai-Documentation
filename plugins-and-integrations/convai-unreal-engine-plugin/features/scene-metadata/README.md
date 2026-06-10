---
title: Scene metadata
description: Find guides, reference pages, and examples for giving Convai characters awareness of objects in your Unreal Engine level.
last_reviewed: "4.0.0-beta.21"
---

Scene metadata is how you give Convai characters awareness of the objects in your level. Add a `UConvaiObjectComponent` to any `Actor` — a door, a crate, a terminal — and every character in the level will know that object exists, what it is called, and what it does. Characters use this information when players ask about the environment around them.

For runtime mutations — adding objects, removing actors, setting conversation partners, and controlling attention — use the environment API on `UConvaiChatbotComponent`. See [Managing the environment at runtime](managing-the-environment-at-runtime.md) for the full method reference.

When the player looks at tagged objects, the [Gaze attention](../gaze-attention/README.md) system can promote them to the chatbot's current focus automatically. Complete scene metadata setup first, then follow [Gaze attention quick start](../gaze-attention/gaze-attention-quick-start.md).

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>How scene metadata works</strong><br>Understand object identity, tracked properties, proximity state, and the runtime sync pipeline.</td>
<td><a href="how-scene-metadata-works.md">how-scene-metadata-works.md</a></td>
</tr>
<tr>
<td><strong>Scene metadata quick start</strong><br>Tag a world actor with the Convai Object Component and test whether a character can use it in conversation.</td>
<td><a href="scene-metadata-quick-start.md">scene-metadata-quick-start.md</a></td>
</tr>
<tr>
<td><strong>Scene metadata component reference</strong><br>Full property, function, and event reference for the Convai Object Component.</td>
<td><a href="scene-metadata-component-reference.md">scene-metadata-component-reference.md</a></td>
</tr>
<tr>
<td><strong>Managing the environment at runtime</strong><br>Add, remove, and update world actors in a chatbot's environment during gameplay.</td>
<td><a href="managing-the-environment-at-runtime.md">managing-the-environment-at-runtime.md</a></td>
</tr>
<tr>
<td><strong>Scene metadata usage examples</strong><br>Complete setups for medical training, industrial safety drills, military simulations, and runtime environment updates.</td>
<td><a href="scene-metadata-usage-examples.md">scene-metadata-usage-examples.md</a></td>
</tr>
<tr>
<td><strong>Troubleshoot scene metadata</strong><br>Diagnose and fix common problems with scene objects not being recognized or tracked properties failing to update.</td>
<td><a href="troubleshoot-scene-metadata.md">troubleshoot-scene-metadata.md</a></td>
</tr>
</tbody>
</table>
