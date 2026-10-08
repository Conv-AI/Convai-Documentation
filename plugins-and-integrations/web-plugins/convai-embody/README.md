---
title: Convai Embody
description: Find the setup guides, API reference, and design notes for Convai Embody, which renders a talking 3D body for a Convai character on the web.
---

Convai Embody renders a Convai character as a 3D body in a web page and drives its lip sync, gaze, breathing, and blinking while the character talks. It is built on the [Convai Web SDK](../convai-web-sdk/README.md) and uses one connection for both, so a page needs a credential and a character ID and nothing else. The current release is <code class="expression">space.vars.embody_version</code>.

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Add a 3D character to a React app</strong><br>Install the package, render a character, and confirm that it speaks with lip sync.</td>
<td><a href="add-a-3d-character-to-a-react-app.md">add-a-3d-character-to-a-react-app.md</a></td>
</tr>
<tr>
<td><strong>Add a 3D character to a three.js scene</strong><br>Use the framework-free API in an existing three.js renderer and render loop.</td>
<td><a href="add-a-3d-character-to-a-three-js-scene.md">add-a-3d-character-to-a-three-js-scene.md</a></td>
</tr>
<tr>
<td><strong>Add a chat widget to a character</strong><br>Let users type and talk to the character through the same connection.</td>
<td><a href="add-a-chat-widget-to-a-character.md">add-a-chat-widget-to-a-character.md</a></td>
</tr>
<tr>
<td><strong>React API reference</strong><br>Props, defaults, and return values for the React components and hooks.</td>
<td><a href="react-api-reference.md">react-api-reference.md</a></td>
</tr>
<tr>
<td><strong>createCharacter reference</strong><br>Options and the returned character handle for the framework-free API.</td>
<td><a href="createcharacter-reference.md">createcharacter-reference.md</a></td>
</tr>
<tr>
<td><strong>How Convai Embody works</strong><br>How a character ID becomes a body, and why motion runs in a fixed order.</td>
<td><a href="how-convai-embody-works.md">how-convai-embody-works.md</a></td>
</tr>
</tbody>
</table>
