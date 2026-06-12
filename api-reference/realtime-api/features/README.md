---
title: Features
description: Extend Realtime API sessions with character actions, dynamic context injection, and image file upload for richer AI interactions.
---

Realtime API features add structured capabilities on top of the base session. Each feature is enabled through fields in the `POST /connect` request body or by sending RTVI messages during an active session.

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Character actions</strong><br>Declare what physical actions a character is allowed to perform and receive structured action instructions per turn.</td>
<td><a href="character-actions/">character-actions</a></td>
</tr>
<tr>
<td><strong>Dynamic context</strong><br>Inject live session data — game state, learner progress, environment changes — without reconnecting.</td>
<td><a href="dynamic-context/">dynamic-context</a></td>
</tr>
<tr>
<td><strong>File upload</strong><br>Send images to Convai during a LiveKit session and include visual context in the AI response.</td>
<td><a href="file-upload/">file-upload</a></td>
</tr>
</tbody>
</table>
