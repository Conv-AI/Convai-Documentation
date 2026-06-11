---
title: Troubleshoot file upload
description: Diagnose and fix file upload failures including rejected files, topic mismatches, missing responses, and inactive LiveKit sessions.
last_reviewed: "2026-06-11"
---

Use this page when an upload is rejected, hangs, or the image is not reflected in the AI's response. Each section describes a specific symptom, its most likely cause, the steps to fix it, and how to verify the fix.

## Upload fails with a file size error

**Symptom.** The `sendFile` call rejects with an error message that includes `"size"`, or the upload is blocked before the byte-stream completes.

**Cause.** The file is larger than the 10 MB limit.

**Fix.** Compress or resize the image before uploading. The following example uses the `browser-image-compression` library to reduce file size client-side.

```typescript
import imageCompression from "browser-image-compression";

async function compressAndUpload(file: File) {
  const compressed = await imageCompression(file, {
    maxSizeMB: 8,            // Target below the 10 MB limit
    maxWidthOrHeight: 1920,
  });

  const info = await room.localParticipant.sendFile(compressed, {
    topic: "file-upload",
    mimeType: compressed.type,
  });

  console.log("Uploaded:", info.id);
}
```

**Verify.** After compression, log `compressed.size` and confirm it is less than `10 * 1024 * 1024` (10 485 760 bytes) before calling `sendFile`.

## Upload fails with an unsupported type error

**Symptom.** The `sendFile` call rejects, or no response is received, and the file is not an image format.

**Cause.** The MIME type is not in the supported list: `image/jpeg`, `image/png`, `image/gif`, `image/webp`.

**Fix.** Validate the MIME type before calling `sendFile`. Reject unsupported files early with a clear user message.

```typescript
const ALLOWED_TYPES = ["image/jpeg", "image/png", "image/gif", "image/webp"];

function validateMimeType(file: File): boolean {
  if (!ALLOWED_TYPES.includes(file.type)) {
    console.error(`Unsupported file type: ${file.type}. Upload JPEG, PNG, GIF, or WebP images only.`);
    return false;
  }
  return true;
}
```

**Verify.** Log `file.type` before the upload call and confirm it matches one of the four supported values.

## Upload hangs or returns no response

**Symptom.** The `sendFile` call does not resolve or reject. The upload appears to start but never completes.

**Cause.** The most common causes are a typo in the topic string or the room not being in a connected state when `sendFile` is called.

**Fix.** Check both conditions before the upload call.

```typescript
// Check room state
if (room.state !== "connected") {
  console.error(`Room is not connected. Current state: ${room.state}`);
  return;
}

// Verify topic string exactly — one character difference causes a silent drop
const TOPIC = "file-upload"; // Must match exactly

const info = await room.localParticipant.sendFile(file, {
  topic: TOPIC,
  mimeType: file.type,
});
```

**Verify.** Log `room.state` immediately before the call and confirm it equals `"connected"`. Log the `topic` value to rule out whitespace or case differences.

## Upload is rejected due to missing data publish permission

**Symptom.** `sendFile` rejects with an error before the byte-stream completes, and the rejection is not related to file size or MIME type.

**Cause.** The LiveKit authentication token for the session does not include data publish permissions. LiveKit rejects the byte-stream at the transport layer before Convai receives any bytes.

**Fix.** Re-issue the LiveKit token with data publish permissions enabled. The exact grant name depends on the LiveKit server version you are using — refer to the LiveKit token documentation for the correct permission field. After re-issuing the token, reconnect the room and retry the upload.

**Verify.** Catch the rejection from `sendFile`, log the error message, and confirm it relates to permissions rather than size or type. After re-issuing the token and reconnecting, a successful upload resolves with a non-empty `info.id`.

## Image upload succeeds but the AI does not respond to it

**Symptom.** `sendFile` resolves and `info.id` is present, but the AI character does not reference or acknowledge the uploaded image in its next response.

**Cause.** The character may not have vision capabilities enabled, or the image was not included in the active LLM context for that turn.

**Fix.** Check the character's vision settings in the Convai dashboard and confirm vision is enabled for the character. Then retry the upload and send a follow-up message referencing the image.

**Verify.** After enabling vision, upload a clearly identifiable image and ask the character to describe what it sees. A response that references image content confirms the feature is active.

## Upload fails mid-transfer due to disconnection

**Symptom.** The `sendFile` call rejects partway through a large file upload, or a `disconnected` room event fires during the transfer.

**Cause.** The LiveKit room connection dropped while the byte-stream was in progress.

**Fix.** Listen for the room's `disconnected` and `reconnected` events and allow the user to retry after reconnection.

```typescript
room.on("disconnected", () => {
  console.warn("Room disconnected. Any in-progress upload has failed.");
  // Cancel UI progress indicator and notify the user
});

room.on("reconnected", () => {
  console.log("Room reconnected. You can retry the upload.");
  // Re-enable the upload UI
});
```

Retry the `sendFile` call after `reconnected` fires. Do not attempt to resume the same stream — start a new upload.

**Verify.** After reconnecting, confirm `room.state === "connected"` before retrying. Log the new `info.id` from the retry call to confirm the server received the complete file.

## Next steps

For the full parameter contract including all error conditions, see the reference.

{% content-ref url="file-upload-reference.md" %}
[File upload reference](file-upload-reference.md)
{% endcontent-ref %}

To understand why the topic string and room state matter architecturally, see the explanation page.

{% content-ref url="how-file-upload-works.md" %}
[How file upload works](how-file-upload-works.md)
{% endcontent-ref %}
