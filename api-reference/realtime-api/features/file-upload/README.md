---
title: File upload overview
description: Send images to Convai over a LiveKit byte-stream session, and find how-to guides, platform examples, and reference for the file upload feature.
last_reviewed: "2026-06-11"
---

The file upload feature lets client applications send images to Convai during an active LiveKit session. Convai receives images through the LiveKit byte-stream channel and can integrate them into the AI response context. Use the pages in this section to understand the mechanism, complete the upload task on your platform, and look up the API contract.

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>How file upload works</strong><br>LiveKit byte-stream transport, topic routing, server processing flow, and response object shape.</td>
<td><a href="how-file-upload-works.md">how-file-upload-works.md</a></td>
</tr>
<tr>
<td><strong>Upload an image</strong><br>Step-by-step: connect to the Realtime API, join a LiveKit room, send the file, and verify the response.</td>
<td><a href="upload-an-image.md">upload-an-image.md</a></td>
</tr>
<tr>
<td><strong>File upload reference</strong><br>Upload call parameters, required topic value, supported MIME types, size limit, and response fields.</td>
<td><a href="file-upload-reference.md">file-upload-reference.md</a></td>
</tr>
<tr>
<td><strong>File upload platform examples</strong><br>Equivalent upload calls for JavaScript, React Native, Swift, and Kotlin.</td>
<td><a href="platform-examples.md">platform-examples.md</a></td>
</tr>
<tr>
<td><strong>Troubleshoot file upload</strong><br>Diagnose and fix rejected files, topic typos, missing responses, and inactive LiveKit sessions.</td>
<td><a href="troubleshooting.md">troubleshooting.md</a></td>
</tr>
</tbody>
</table>
