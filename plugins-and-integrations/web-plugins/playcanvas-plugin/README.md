---
title: PlayCanvas Plugin
description: Add a talking Convai character to a PlayCanvas scene from a template built on the Convai Web SDK or Convai Embody, with Japanese F as the default.
cover: ../../../.gitbook/assets/playcanvas cover.jpg
coverY: 0
---

Add a talking Convai character to a PlayCanvas scene. Two templates on GitHub give you a working scene with MetaHuman lip sync, idle and talking animation, and a chat widget. Both use Japanese F, a MetaHuman-rig character, by default. Pick the template that matches where the character's 3D model comes from.

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Start from the Web SDK template</strong><br>Ship the character's model with your app and drive it with the Convai Web SDK.</td>
<td><a href="start-from-the-web-sdk-template.md">start-from-the-web-sdk-template.md</a></td>
</tr>
<tr>
<td><strong>Start from the Convai Embody template</strong><br>Load the character's body from its character ID with Convai Embody.</td>
<td><a href="start-from-the-convai-embody-template.md">start-from-the-convai-embody-template.md</a></td>
</tr>
</tbody>
</table>

## Choose a template

| | Web SDK template | Convai Embody template |
|---|---|---|
| Repository | [`Conv-AI/convai-playcanvas-web-sdk`](https://github.com/Conv-AI/convai-playcanvas-web-sdk) | [`Conv-AI/convai-playcanvas-embody`](https://github.com/Conv-AI/convai-playcanvas-embody) |
| Packages | `@convai/web-sdk` | `@convai/embody` and `@convai/web-sdk` |
| Character model | A GLB file in your app | Resolved from the character ID |
| Face animation | Lip sync | Lip sync and blinking |
| Environment | Production | Staging, which serves web bodies |

## Legacy editor template

The earlier PlayCanvas Editor template, [Convai SDK](https://playcanvas.com/project/1216467/overview/convai-sdk), and the pages under this section that describe it are built on the deprecated `convai-web-sdk` package. Start new projects from one of the templates above.
