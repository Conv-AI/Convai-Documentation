# Image usage policy

Images are evidence and orientation aids, never decoration, filler, or a substitute for precise written
steps. All required information also exists as text outside the image (CV-59).

## When to use an image

Only when it does at least one of these jobs: disambiguates a UI state text can describe only
awkwardly; confirms a visual result the reader must recognize; shows where a component, asset, field,
menu, prefab, GameObject, or setting appears; shows a scene, hierarchy, Inspector state, animation
state, lip sync result, avatar setup, or runtime behavior that affects correctness; or documents a
state support teams commonly ask users to compare against.

Never when the content is code, terminal output, package names, field values, or configuration text
that should be selectable (CV-47); when it would only repeat a menu path the steps already give; when it
would go stale quickly without reducing ambiguity; when it is decorative or marketing; or when the page
already confirms the state and the image adds nothing new.

| Situation | Requirement |
|---|---|
| Inspector or editor field setup where the field or component can be confused | Image or placeholder required: prevents wrong-field setup |
| Scene hierarchy, prefab placement, GameObject or component arrangement | Image or placeholder required: spatial setup is error-prone in text |
| Project, build, XR, microphone, or permission UI with several similar options | Image or placeholder required: prevents the wrong setting |
| Visual feature output: animation, lip sync, avatar response, in-scene action | Image, GIF or video, or placeholder, required: the outcome is visual |
| Troubleshooting a visual mismatch or expected UI state | Image or placeholder when the reader must compare |
| Package or install confirmation state | Optional: useful for beginners; text verification can be enough |
| Hub page cards | Optional, only if images improve routing and are maintained |
| Architecture, lifecycle, data flow, decision logic | Prefer Mermaid; an image only when Mermaid is insufficient |
| Reference page for an API, class, or fields | Usually none: reference is text-first and searchable |
| Code, JSON, YAML, logs, console output; a simple procedure with unambiguous labels | None |

Placeholders, file names, alt text, captions and markup are in `image-markup.md`.
