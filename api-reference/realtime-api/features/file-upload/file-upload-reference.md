---
title: File upload reference
description: Reference for the file upload call, covering all parameters, the required topic value, supported MIME types, file size limit, and response fields.
last_reviewed: "2026-06-11"
---

Complete contract for the `sendFile` call used to upload images over the LiveKit byte-stream channel. All parameters, type constraints, the required `"file-upload"` topic value, supported MIME types, the 10 MB size limit, and the response object shape are listed here.

## `sendFile` signature

```typescript
room.localParticipant.sendFile(
  file: File | Blob | URL,
  options: {
    topic: string;
    mimeType?: string;
    onProgress?: (progress: number) => void;
  }
): Promise<{ id: string; size?: number; timestamp: number }>
```

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file` | `File` / `Blob` / `URL` | Yes | The file to upload. Pass a `File` object from a file input, a `Blob` for in-memory data, or a `URL` pointing to a local file resource. |
| `options.topic` | `string` | Yes | Topic string that routes the byte-stream to the Convai file upload handler. Must be exactly `"file-upload"`. Any other value results in the upload being silently ignored by Convai. |
| `options.mimeType` | `string` | Recommended | MIME type of the file. Pass `file.type` from a `File` object. Omitting this field may cause Convai to reject the upload if the type cannot be inferred from the stream. |
| `options.onProgress` | `(progress: number) => void` | No | Callback invoked during the upload. The `progress` argument is a number from `0` (upload started) to `1` (upload complete). |

## Response

`sendFile` returns a `Promise` that resolves to:

```typescript
{
  id: string;        // Unique stream ID assigned by the server
  size?: number;     // File size in bytes as received; may be absent
  timestamp: number; // Upload timestamp as a Unix millisecond value
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | `string` | Yes | Unique identifier for the byte-stream. Use this to confirm the server received the upload and to correlate uploads with AI responses. |
| `size` | `number` | No | File size in bytes as reported by the server. This field is optional and may be absent on some platforms. |
| `timestamp` | `number` | Yes | Upload timestamp as a Unix millisecond value. |

## Supported MIME types

| MIME type | Format |
|---|---|
| `image/jpeg` | JPEG |
| `image/png` | PNG |
| `image/gif` | GIF |
| `image/webp` | WebP |

Files with any other MIME type are rejected by Convai.

## Constraints

| Constraint | Value |
|---|---|
| Maximum file size | 10 MB |
| Required topic | `"file-upload"` |
| Transport | LiveKit byte-stream — not HTTP |
| Required room state | `'connected'` |
| Required token permission | Data publish |

## Error conditions

`sendFile` rejects when any of the following conditions occur.

| Condition | Description |
|---|---|
| File exceeds 10 MB | The file size is greater than 10 MB. Compress or resize the image before uploading. |
| Unsupported MIME type | The `mimeType` value is not in the supported list. Validate against the supported types before calling `sendFile`. |
| Room not connected | `room.state` is not `'connected'` at the time of the call. Wait for the connection to be established. |
| Missing data publish permission | The LiveKit token does not include data publish grants. Re-issue the token with the correct permissions. |
| Network disconnection | The connection dropped during transfer. Handle the rejection and retry after the room reconnects. |

## Next steps

For symptom-by-symptom diagnosis, see the troubleshooting page.

{% content-ref url="troubleshooting.md" %}
[Troubleshoot file upload](troubleshooting.md)
{% endcontent-ref %}
