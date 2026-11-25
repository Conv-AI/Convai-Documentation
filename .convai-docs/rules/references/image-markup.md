# Image placeholders and markup

How an image or its placeholder is written; when a page needs one is in `images.md`. On a product page
the reader follows along on screen, so show the panel they must find and the state that confirms the
step worked (CV-51).

## Placeholders

When a needed image does not exist yet and capture does not cover the subject, add a placeholder
specific enough that whoever captures it knows the exact screen, fields and version without asking:

```md
{% hint style="warning" %}
**Screenshot required before publishing:** Capture the Convai Settings asset in the Unity Inspector with the API Key field filled and the Character ID field visible.
{% endhint %}

<figure><img src="../../.gitbook/assets/TODO-convai-settings-api-key-field.png" alt="[Draft alt text: the intended image and its purpose]"><figcaption><p>TODO: Replace with screenshot showing [specific state].</p></figcaption></figure>
```

Never a vague `TODO screenshot`. The file name starts with `TODO-`, with draft alt text and caption. Both
markers are publish-blocking linter errors (CV-50), so an unfinished page cannot go live.

## Captured screenshots

When the subject file has `capture`, write no placeholder: describe each shot in
`.convai-docs/shots/<page path without .md>.json` and the capturer takes it.

```json
{"schema": 1, "page": "<page path>", "subject": "<subject>", "shots": [
  {"id": "whole-screen", "surface": "<capture.surfaces id>", "route": "/dashboard/character/{character}",
   "masks": ["#character-id-input"], "alt": "...", "caption": "..."}]}
```

Optional: `steps` (`click`, `hover` or `wait_for` a selector; never typing), `selector` (one element, `pad`
0-64) or `clip`. Mask anything account-specific; each mask must match an element. The figure's `src` is
`<page-slug>--<id>.png` in the assets folder (slug: file name, or a `README.md`'s folder); alt and
caption match the shot's. Never write `captured`.

## Standards

| Item | Standard |
|---|---|
| Location | The space's `.gitbook/assets/` folder, unless the repository uses another established asset folder |
| File name | Descriptive kebab-case for what it shows: `convai-settings-api-key-field.png`, never a tool's default name (CV-80) |
| Alt text | The image's purpose and the relevant state, not every visual detail (CV-48) |
| Caption | What the image shows, verifies, or helps the reader find |
| Count | The fewest images that remove the ambiguity |
| Freshness | Matches the documented SDK version, engine version, and UI state |
| Cropping | The relevant area, with enough surrounding context for orientation |
| Sensitive data | No API keys, tokens, emails, private project names, local usernames, or internal paths (CV-49) |

Markup: a `<figure>` with the `<img>` (`src`, `alt`) and `<figcaption><p>`, as in the placeholder
example, with the real file name.
