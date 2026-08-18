# Image usage policy

Images are evidence and orientation aids. They are not decoration, filler, or a substitute for precise
written steps.

## When to use an image

Use an image only when it does at least one of these jobs:

- Disambiguates a visual UI state that text alone can describe only awkwardly.
- Confirms a visual result the reader must recognize.
- Shows where a component, asset, field, menu, prefab, GameObject, or setting appears in the editor.
- Shows a scene, hierarchy, Inspector state, animation state, lip sync result, avatar setup, or
  runtime behavior that affects correctness.
- Documents a UI or visual state that support teams commonly need users to compare against.

## When not to use an image

- The content is code, terminal output, package names, field values, or configuration text that
  should be selectable.
- The screenshot would only repeat an obvious menu path already written in the steps.
- The screenshot would become stale quickly and does not reduce ambiguity.
- The image is decorative or marketing-oriented.
- The page already has enough visual confirmation and the new image does not add new information.

## Required vs optional images

| Situation | Requirement | Rationale |
|---|---|---|
| Inspector/editor field setup where the exact field/component can be confused | Required image or required placeholder | Prevents wrong-field setup and support tickets. |
| Scene hierarchy, prefab placement, or GameObject/component arrangement | Required image or required placeholder | Spatial setup is error-prone in text only. |
| Package/install confirmation state | Optional image | Useful for beginner pages, but text verification can be enough. |
| Project/build/XR/microphone/platform permission UI with multiple similar options | Required image or required placeholder | Prevents selecting the wrong setting. |
| Visual feature output (animation, lip sync, avatar response, in-scene action) | Required image, GIF/video, or required placeholder | The outcome is visual and must be recognizable. |
| Architecture, lifecycle, data flow, or decision logic | Prefer Mermaid; use image only when Mermaid is insufficient | Diagrams should remain maintainable and accessible. |
| Code samples, JSON, YAML, snippets, logs, console output | No image | Use selectable text/code blocks. |
| Simple numbered procedure with unambiguous menu labels | No image | Avoid screenshot noise. |
| Hub/index page cards | Optional image | Use only if images improve routing and are maintained. |
| Reference page for API/classes/fields | Usually no image | Reference should be text-first and searchable. |
| Troubleshooting visual mismatch or expected UI state | Required image or placeholder if comparison is needed | Helps readers compare their state against the expected state. |

## Required image placeholders

If an image is required for AAA clarity but the final screenshot is not available, add a placeholder
block specific enough that the screenshot owner can capture the correct image without guessing.

```md
{% hint style="warning" %}
**Screenshot required before publishing:** Capture [exact UI, scene, Inspector, or runtime state]. The image must show [specific fields/components/result] for [SDK/engine version if relevant].
{% endhint %}

<figure><img src="../../.gitbook/assets/TODO-descriptive-image-name.png" alt="[Describe the intended image and its documentation purpose]"><figcaption><p>TODO: Replace with screenshot showing [specific state].</p></figcaption></figure>
```

A placeholder is a work order for whoever captures the screenshot. It must be specific enough that they
can take the right image without asking you what you meant.

Good — the capturer knows the exact screen, the exact fields, and the version:

```md
{% hint style="warning" %}
**Screenshot required before publishing:** Capture the Convai Settings asset in the Unity Inspector with the API Key field filled and the Character ID field visible.
{% endhint %}
```

Bad — nobody can act on this:

```md
TODO: add screenshot
```

Placeholder rules:

- Use placeholders only where the final page genuinely needs an image.
- Prefix unfinished image files with `TODO-` so they are easy to find before publishing.
- The placeholder text must state exactly what to capture.
- Both the `TODO-` file prefix and the "Screenshot required before publishing" marker are
  publish-blocking ERRORs in the linter, so an unfinished page cannot reach `main` by accident.
- The placeholder must include draft alt text and a draft caption.
- Never leave a vague placeholder such as `TODO screenshot`.
- Never publish a page with `TODO-` image paths or "Screenshot required before publishing" hints.

## Image standards

| Item | Standard |
|---|---|
| File location | Store GitBook image assets under `.gitbook/assets/` unless the active docs repository uses another established asset folder. |
| File name | Descriptive kebab-case: `convai-settings-api-key-field.png`, `package-manager-sdk-installed.png`. |
| Placeholder file name | Prefix with `TODO-`: `TODO-convai-settings-api-key-field.png`. |
| Alt text | Describe the image purpose and the relevant state, not every visual detail. |
| Caption | State what the image shows, verifies, or helps the reader find. |
| Image count | Use the fewest images needed to remove ambiguity. |
| Freshness | Screenshots must match the documented SDK version, engine version, and UI state. |
| Accessibility | All required information must also exist as text outside the image. |
| Cropping | Crop to the relevant UI area, but keep enough surrounding context for orientation. |
| Sensitive data | Do not show API keys, tokens, emails, private project names, local usernames, or internal paths. |

## Image markup

```html
<figure><img src="../../.gitbook/assets/convai-settings-inspector.png" alt="Unity Inspector showing the Convai Settings asset with the API key field selected"><figcaption><p>Convai Settings asset in the Unity Inspector.</p></figcaption></figure>
```

Always include meaningful `alt` text. Do not use screenshots as the only source of essential text.
Keep screenshots current with the documented SDK version.
