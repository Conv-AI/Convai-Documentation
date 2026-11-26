# Captured screenshots

On a page whose subject has screenshot capture (its subject file has a `capture` object), screenshots
are captured from the product, never left as a "Screenshot required before publishing" placeholder
for a person. The writer describes each shot in the page's shot manifest; the capturer takes it.
Editor screenshots (Unity, Unreal) are not captured yet and keep the placeholder path in
`references/images.md`.

## What the writer does

The writer's rules are the "Captured screenshots" section of `image-markup.md`, which every page
type that takes screenshots reads. This file is the full format and the capture behaviour, for the
capturer and for maintainers; a page write does not read it.

## The manifest

```json
{
  "schema": 1,
  "page": "convai-playground/character-tour.md",
  "subject": "playground",
  "shots": [
    {
      "id": "whole-screen",
      "surface": "character-editor",
      "route": "/dashboard/character/{character}?tab=description",
      "steps": [{"wait_for": "role=tab[name=\"Description\"]"}],
      "masks": ["[data-testid=\"character-id\"]"],
      "alt": "The character editor with the Description tab open",
      "caption": "The character editor with a test character open."
    }
  ]
}
```

| Key | Holds |
|---|---|
| `schema` | `1` |
| `page` | The page's path in the documentation repository |
| `subject` | The page's subject; its subject file must have `capture` |
| `slug` | Only when two pages of one space would share a slug; the check says when |
| `shots[].id` | Kebab-case, unique on the page; part of the image name |
| `shots[].surface` | A surface from the subject's `capture.surfaces`; its source files decide when the shot is stale |
| `shots[].route` | The product path to open. `{character}` is the fixture character's id, found by name at capture time; never write an id |
| `shots[].steps` | Optional. `{"click": selector}`, `{"hover": selector}` or `{"wait_for": selector}`. A click or hover target must match one element. There is no typing step |
| `shots[].selector` or `shots[].clip` | Optional. A selector crops to one element (plus `pad`, 0 to 64 CSS pixels); a clip is `{x, y, width, height}` in CSS pixels. Neither means the whole 1440x900 window |
| `shots[].masks` | Selectors painted over in this shot, added to the subject's `capture.masks` |
| `shots[].alt` | What the image shows and why the reader needs it, never "screenshot" or a file name |
| `shots[].caption` | One sentence on what the image shows or confirms |
| `shots[].captured` | Written by the capturer: when, the source commit and digest, the shot's own digest, the image's SHA-256 and size |

Selectors are Playwright selectors: CSS, `text=...`, or `role=tab[name="Description"]`.

The documentation repository is public. A manifest names a surface by its id and a route by its
product path; it never holds a source path, a repository name, an account, a character id or a key.

## Capture

Every shot is 1440x900 CSS pixels at device scale 2, in the light theme (a product that keeps its own
theme gets it from the subject's `capture.local_storage`, written into the capture profile before the
page loads), from the fixture: a
dedicated docs account that holds one workspace and only the "Museum Guide" character. Before any
shot the capturer reads the account's own lists (GET requests only) and refuses an account with more
or fewer than one workspace, without a character of that exact name, or with any other character,
because every list screen shows the whole workspace. A person signs that account in once with
`capture.py login --fresh`, which starts from an empty browser profile and moves the previous one
aside without deleting it.

Masking is mandatory. Before and after each shot the capturer reads what the shot's area shows, and
the shot fails, writing nothing, when anything unmasked there is an email address, something shaped
like a key or token, a password field, the account's name or menu, or another workspace's name. It
then checks the written image carries the mask colour in every masked box. A failure names what kind
of data was found and where, never the data itself; the fix is a mask selector in the shot.

Capture never changes the account. Every request that is not a read is aborted before it leaves the
browser, unless the subject's `capture.allow_post` names it as a read, and a shot cannot type.

## Staleness

`tools/shots.py status <page>` reports, per shot: `error` (the manifest or the page must change),
`uncaptured`, or `stale`. A shot is stale when its definition or the subject's default masks
changed, when its image is not the file the capturer wrote, or when the source files behind its
surface changed since the commit it was captured from. `capture.py run <page> --only-stale` captures
exactly those again.
