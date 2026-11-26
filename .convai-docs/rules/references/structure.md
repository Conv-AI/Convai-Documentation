# Site structure

Where a page belongs: the spaces, the groups inside a space, the capability pages, and file names.
How one page is shaped is in `page-structure.md`.

## The spaces

The site is moving to seven spaces synced from one repository through `gitbook-docs.yaml`, with
`assembly-studio` added later. The top bar reads: Get started, Playground, Experiences, SDKs (a
dropdown: Unity, Unreal Engine, Web), API and tools.

| Space | URL | Holds | Today's path in the documentation repository |
|---|---|---|---|
| `home` (Get started) | `/` | What Convai is, choose-your-path cards, quickstarts, capability pages, credits and billing, changelog, glossary, the Cyberpunk 2077 mod | `README.md`, `convai-credits/`, `plugins-and-integrations/modding-framework/` |
| `playground` | `/playground` | Dashboard, character editor (one page per tab), voices and ElevenLabs, Workspaces, versioning, testing, publishing | `convai-playground/`, the ElevenLabs page under `plugins-and-integrations/other-integrations/` |
| `experiences` | `/experiences` | Avatar Studio, Convai Sim, Chat Experiences, embedding a published experience, Asset Uploader | `no-code-experiences/` without XR Animation Capture, `plugins-and-integrations/convai-pixel-streaming-embed/`, `plugins-and-integrations/asset-uploader/` |
| `unity` | `/unity` | The Unity SDK section | `plugins-and-integrations/convai-unity-sdk/` |
| `unreal` | `/unreal` | The Unreal Engine plugin section | `plugins-and-integrations/convai-unreal-engine-plugin/` |
| `web` | `/web` | Web SDK, Convai Embody, PlayCanvas, character and animation assets for the web | `plugins-and-integrations/web-plugins/` without the legacy Web SDK |
| `api` (API and tools) | `/api` | Character APIs, Live APIs, Interaction APIs, authentication, Convai MCP, Convai CLI | `api-reference/` |
| `assembly-studio` | `/assembly-studio` | Added later | None yet |

**Today and after the migration.** The repository is still one space with today's paths: the root
`README.md` is the Welcome page, and `SUMMARY.md` groups the sidebar under one `##` heading per
top-level section. Until the documentation owner announces the migration, write every page at today's
path; the table says which space it becomes. No page-writing task moves a page.

## Where a page belongs

Pick the space by what the page is about, not by which team wrote it; the subject's `docs_paths` name
its folders. If a page fits no space, stop and ask. Never create a top-level section or change the root
structure in a page-writing task.

A space's sidebar groups are, in this order: Overview, Getting started, Concepts, How-to guides,
Reference, Troubleshooting, Release notes. A space leaves out a group it has no pages for and never
reorders them. The Unity and Unreal groups already follow this order and keep their names: never rename
a group or move a page to fit it, because both change URLs.

Every group and every top-level page has an icon from the space's allowed list (CV-81).

## Capability pages

One page each for Memory, Knowledge Bank, Narrative Design, Actions, Vision, Voice and Emotion, in the
`home` space under a group named Capabilities (`capabilities/<name>.md`). Each is an explanation page:
what the capability is, in a few paragraphs, then one link per platform (Playground, Unity, Unreal
Engine, Web, API) to that platform's page for it, and no platform steps. Each platform page links back
to its capability page in its first section. The Narrative Design Guide under Web is folded into the
Narrative Design capability page.

## File naming and location

| Item | Standard |
|---|---|
| Page file | One `.md` file per page, named in lowercase kebab-case English from its title (`configure-api-key.md`), never from its folder: the first publish fixes the URL. |
| Section index | `README.md` in the section folder. Every folder that holds pages has one. |
| Folders | Mirror the GitBook navigation tree: `SUMMARY.md` indentation equals folder depth. |
| Images | In the space's `.gitbook/assets/` folder, by relative path; no per-folder image folders. |
| Variables | `.gitbook/vars.yaml` (`variables.md`). |

## Renaming and moving pages

A rename or a move changes the published URL, and breaks every link, bookmark and search result that
points at it. Do it only in a restructuring task, never to fit a pattern, and only with the
documentation owner's approval. The change carries a `.gitbook.yaml` redirect for the old URL and the
`SUMMARY.md` update (CV-65, CV-84), and its summary lists every inbound link found.
