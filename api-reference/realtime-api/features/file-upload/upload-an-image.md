---
title: Upload an image
description: Connect to a LiveKit room, send an image file using the required topic, and verify the upload using the response stream identifier.
last_reviewed: "2026-06-11"
---

Uploading an image to Convai requires an active LiveKit room connection. Call `sendFile` on the local participant with the `"file-upload"` topic and a supported image file to send the image and receive a confirmation response.

## Prerequisites

- The LiveKit JavaScript client SDK (`livekit-client`) is installed in your project.
- The room is in a connected state — `room.state` equals `'connected'` before calling `sendFile`.
- Your LiveKit token includes data publish permissions.
- The image is one of the supported types: `image/jpeg`, `image/png`, `image/gif`, or `image/webp`.
- The image is no larger than 10 MB.

## Send the image

{% stepper %}
{% step %}
### Connect to the LiveKit room

Create a `Room` instance and call `connect` with your LiveKit server URL and authentication token. Wait for the connection to complete before sending any files.

```typescript
import { Room } from "livekit-client";

const room = new Room();
await room.connect(LIVEKIT_SERVER_URL, YOUR_LIVEKIT_TOKEN);
```
{% endstep %}

{% step %}
### Validate the file before sending

Check the MIME type and file size before calling `sendFile`. Convai rejects files with an unsupported type or a size above 10 MB. Validating client-side gives immediate feedback and avoids a wasted upload attempt.

```typescript
const MAX_SIZE = 10 * 1024 * 1024; // 10 MB
const ALLOWED_TYPES = ["image/jpeg", "image/png", "image/gif", "image/webp"];

function validateFile(file: File): boolean {
  if (file.size > MAX_SIZE) {
    console.error("File exceeds the 10 MB limit.");
    return false;
  }
  if (!ALLOWED_TYPES.includes(file.type)) {
    console.error(`Unsupported file type: ${file.type}`);
    return false;
  }
  return true;
}
```
{% endstep %}

{% step %}
### Call sendFile with the required topic

Pass the file to `room.localParticipant.sendFile`. Set `topic` to `"file-upload"` — this exact string routes the byte-stream to the correct handler in Convai. Pass `file.type` as `mimeType` to preserve encoding information. Use the optional `onProgress` callback to track transfer progress as a value from `0` to `1`.

```typescript
async function uploadImage(file: File) {
  if (!validateFile(file)) return;

  const info = await room.localParticipant.sendFile(file, {
    topic: "file-upload",      // Required — must match exactly
    mimeType: file.type,       // Recommended — pass the file's MIME type
    onProgress: (progress) => {
      console.log(`Upload progress: ${Math.ceil(progress * 100)}%`);
    },
  });

  console.log(`Uploaded with stream ID: ${info.id}`);
}
```
{% endstep %}
{% endstepper %}

## Verify the upload

When `sendFile` resolves, `info.id` contains the unique stream identifier that Convai assigned to the upload. A non-empty `info.id` confirms that Convai received the byte-stream. Log or store this identifier to correlate the upload with AI responses that reference the image.

```typescript
console.log("Stream ID:", info.id);
console.log("Timestamp:", info.timestamp);
```

{% hint style="success" %}
A resolved `info.id` confirms that Convai received the image and integrated it into the LLM context for the active session. The next character response in the session can reference the uploaded image.
{% endhint %}

## Handle upload failures

Wrap the `sendFile` call in a `try/catch` block. The call rejects on network disconnection, MIME type rejection, or size limit rejection.

```typescript
try {
  const info = await room.localParticipant.sendFile(file, {
    topic: "file-upload",
    mimeType: file.type,
  });
  console.log("Upload succeeded:", info.id);
} catch (error) {
  console.error("Upload failed:", error);
}
```

For symptom-by-symptom diagnosis, see [Troubleshoot file upload](troubleshooting.md).

## Next steps

See the equivalent upload call for React Native, iOS, and Android.

{% content-ref url="platform-examples.md" %}
[File upload platform examples](platform-examples.md)
{% endcontent-ref %}

For the full parameter and response contract, see the reference.

{% content-ref url="file-upload-reference.md" %}
[File upload reference](file-upload-reference.md)
{% endcontent-ref %}
