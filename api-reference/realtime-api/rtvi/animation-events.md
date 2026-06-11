---
title: Animation events
description: Reference for visemes, neurosync-blendshapes, and chunked-neurosync-blendshapes — payload fields, viseme key mappings, blendshape count, and avatar guidance.
last_reviewed: "2026-06-11"
---

Animation events deliver real-time data to drive avatar facial animation. Viseme events provide coarse per-phoneme lip-sync weights. NeuroSync events provide high-fidelity 251-value facial blendshape frames for full expressive animation.

## `visemes`

Sent frequently during bot speech. Each event carries blend weights for 15 mouth shapes that correspond to the phonemes the bot is currently producing. Apply these weights to your avatar's lip-sync blend shapes to animate the mouth in sync with audio.

Values range from `0.0` (shape not active) to `1.0` (shape fully applied).

```json
{
  "label": "rtvi-ai",
  "type": "server-message",
  "data": {
    "type": "visemes",
    "visemes": {
      "sil": 0.0,
      "pp": 0.8,
      "ff": 0.0,
      "th": 0.0,
      "dd": 0.0,
      "kk": 0.0,
      "ch": 0.0,
      "ss": 0.0,
      "nn": 0.0,
      "rr": 0.0,
      "aa": 0.2,
      "e": 0.0,
      "ih": 0.0,
      "oh": 0.0,
      "ou": 0.0
    }
  }
}
```

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `"visemes"`. |
| `visemes` | object | Dictionary of 15 viseme keys, each with a float value between `0.0` and `1.0`. |

**Viseme key reference:**

| Key | Phonemes |
|---|---|
| `sil` | Silence |
| `pp` | P, B, M |
| `ff` | F, V |
| `th` | TH (voiced and unvoiced) |
| `dd` | T, D |
| `kk` | K, G |
| `ch` | CH, J, SH |
| `ss` | S, Z |
| `nn` | N, L |
| `rr` | R |
| `aa` | A (as in "father") |
| `e` | E (as in "bed") |
| `ih` | I (as in "bit") |
| `oh` | O (as in "boat") |
| `ou` | U, W |

**Recommended action:** Apply viseme weights to your avatar's mouth blend shapes on each event. Events arrive at the frame rate needed for smooth lip-sync; apply them immediately without additional buffering.

## `neurosync-blendshapes`

Sent per frame during bot speech when the NeuroSync animation service is active. Each event carries exactly 251 blendshape values covering the full expressive range of a facial rig.

```json
{
  "label": "rtvi-ai",
  "type": "server-message",
  "data": {
    "type": "neurosync-blendshapes",
    "blendshapes": [0.0, 0.1, 0.05, 0.0, 0.0, 0.02, "... 245 more values ..."]
  }
}
```

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `"neurosync-blendshapes"`. |
| `blendshapes` | float[] | Array of exactly 251 blendshape values, each between `0.0` and `1.0`. |
| `response_id` | string \| null | Optional. Response identifier, shared with the turn lifecycle events for synchronization. |
| `neurosync_turn_id` | integer \| null | Optional. NeuroSync turn identifier for matching blendshapes to audio. |
| `epoch` | integer \| null | Optional. Epoch counter within the turn. |
| `sequence` | integer \| null | Optional. Sequence number of this frame within the epoch. |

The array always contains exactly 251 values. The server raises an error if the NeuroSync service returns a different count.

**Recommended action:** Apply the 251 blendshape values to your avatar's facial rig in order. Use the optional `neurosync_turn_id` and `sequence` fields to synchronize frames with audio when needed.

## `chunked-neurosync-blendshapes`

A batched variant of `neurosync-blendshapes` that delivers multiple frames in a single event. Use this when you prefer to receive groups of frames rather than individual frames to reduce event-processing overhead.

```json
{
  "label": "rtvi-ai",
  "type": "server-message",
  "data": {
    "type": "chunked-neurosync-blendshapes",
    "blendshapes": [
      [0.0, 0.1, 0.05, 0.0, "... 247 more values ..."],
      [0.02, 0.12, 0.04, 0.0, "... 247 more values ..."],
      [0.01, 0.09, 0.06, 0.0, "... 247 more values ..."]
    ]
  }
}
```

| Field | Type | Description |
|---|---|---|
| `type` | string | Always `"chunked-neurosync-blendshapes"`. |
| `blendshapes` | float[][] | List of blendshape frames. Each inner array contains exactly 251 values. |
| `response_id` | string \| null | Optional. Response identifier. |
| `neurosync_turn_id` | integer \| null | Optional. NeuroSync turn identifier. |
| `epoch` | integer \| null | Optional. Epoch counter. |
| `sequence` | integer \| null | Optional. Sequence number of the first frame in the chunk. |

**Recommended action:** Queue all frames from the `blendshapes` list and apply them sequentially at the target frame rate for smooth animation.

## Related pages

{% content-ref url="server-events.md" %}
[Server events overview](server-events.md)
{% endcontent-ref %}

{% content-ref url="turn-events.md" %}
[Turn events](turn-events.md)
{% endcontent-ref %}
