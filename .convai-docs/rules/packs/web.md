# Web SDK pack

SDK-specific facts for the Convai Web SDK. Generic doctrine lives in `references/`.

Every fact below was verified against the SDK source on the `stable-release` branch, with the file and
symbol noted where it matters. An earlier draft of this pack was built from the published documentation
instead, and verifying it against code found three wrong claims and four missing API areas — which is
why the rule is what it is: code settles a claim, documentation does not.

Last audited: 2026-08-18 against `Conv-AI/convai-web-sdk_internal` (`stable-release`) at `be3824c`.

---

## Product naming

- The product is the **Convai Web SDK**, package `@convai/web-sdk`.
- Call it an **SDK**, never a plugin. The docs are consistent on this inside
  `convai-web-sdk/`; the parent folder is named `web-plugins/` for historical reasons and that name
  should not leak into page prose.
- There is a **legacy** SDK, package `convai-web-sdk` (unscoped), documented at
  `plugins-and-integrations/web-plugins/convai-web-sdk-1/` and marked deprecated there. Its title is
  "Convai Web SDK (Legacy)". Never present it as current, and never mix its API with the new one — see
  "The legacy SDK is a different API" below.
- Refer to Convai's backend as **Convai**. Never "Convai cloud", "Convai's servers", or "cloud-powered".

## Audience and prerequisites baseline

Web developers. Assume JavaScript and TypeScript fluency and familiarity with a package manager and a
bundler. Do not assume React knowledge on the vanilla pages, and do not assume game-engine knowledge
anywhere.

Baseline prerequisites stated in the current quickstart:

- A Convai account with an API key
- A character ID from the Convai dashboard
- For the React path: **React 18 or 19**. Both are declared peer dependencies alongside `react-dom`.

The package declares **no `engines` field**, so there is no Node version requirement in the manifest.
The published quickstart says Node 18+; that claim is not backed by the package and should be confirmed
with the Web SDK owner before a page repeats it.

No browser-support statement exists in the source or the docs. **Do not invent one.**

## Terminology and concepts

| Term | Notes |
|---|---|
| Convai Web SDK | The product. |
| `@convai/web-sdk` | The npm package. Always inline code. |
| `@convai/web-sdk/core` | Import subpath for the framework-free core. |
| `@convai/web-sdk/react` | Import subpath for the React bindings. |
| `@convai/web-sdk/vanilla` | Import subpath for the vanilla-TypeScript API. |
| `@convai/web-sdk/vanilla/websocket` | Import subpath for the WebSocket transport. |
| `@convai/web-sdk/lipsync-helpers` | Import subpath for the blendshape and ARKit helpers. |
| `ConvaiClient` | The core client class. |
| `useConvaiClient` | The React hook. |
| `createConvaiWidget()` | The vanilla helper that mounts a widget. |
| `BlendshapeQueue`, `MemoryManager` | Named runtime pieces, defined in `src/core/`. |
| `AudioRenderer` | **Two different things with one name.** In vanilla it is the SDK's own class in `src/vanilla/AudioRenderer.ts`. In React it is an alias re-exported from LiveKit. Never describe them as the same object. |
| `ConvaiWidget` | **Also two things.** A React component, and a vanilla construct mounted through `createConvaiWidget`. Say which one a page means. |
| `ConvaiConfig` | The public config interface, `src/core/types.ts`. |
| `createBlendshapeQueue`, `createARKitBlendshapeQueue`, `createARKitNameMapper` | Lip sync helpers, from the `lipsync-helpers` subpath. |

`ConvaiWidgetProps` exists in the source but is **not exported**, so it is not public API. Do not
document it as a type a reader can import.

The six subpaths above are the package's declared `exports`. There is no other public entry point.

Web-native terms keep their conventional spelling: npm, ES module, bundler, `Promise`, WebSocket,
`getUserMedia`, `AudioContext`.

Format every package name, import path, class, hook, component, method, event name, and config field as
inline code, including inside table cells.

## Public API areas a writer must not miss

Verified in `src/core/types.ts`. The published documentation covers only part of this surface, so a page
written from those pages alone will silently omit real features:

| Area | Notes |
|---|---|
| `transport` | Selects `"livekit"` or `"websocket"`. A significant choice for an integrator, with its own subpath. |
| `authToken` | Token-based auth alongside `apiKey`. Prefer it for anything client-side. |
| `enableEmotion`, `emotionConfig` | Emotion support, with selectable providers. |
| `visionInputConfig` | Vision input configuration. |
| `respondModes` | Response mode selection. |
| `endUserMetadata`, `characterSessionId` | Session and end-user identity. |

Read the full `ConvaiConfig` interface before writing any configuration page. Do not document a field
set from an existing page; that is how the above went missing.

## Install and package model

Installed from npm. The current docs show:

```bash
npm install @convai/web-sdk
```

`yarn add` and `pnpm add` equivalents appear on the React page. There is **no CDN or script-tag install**
documented; do not write one.

All six import subpaths are part of the single package — `react` and `vanilla` are not separate
packages. A page that implies otherwise is wrong.

Canonical entry page: `plugins-and-integrations/web-plugins/convai-web-sdk/quickstart.md`.

## The legacy SDK is a different API

The legacy `convai-web-sdk` package uses class and method names that do not exist in the current SDK —
for example `setResponseCallback`, `startAudioChunk`, `endAudioChunk`, `sendTextChunk`, `resetSession`.
None of these belong on a current Web SDK page.

This is the highest-risk mistake for this pack: the two folders have same-named pages (`actions.md` in
both) and a writer searching the repository will hit legacy pages first as often as not. Before quoting
any Web SDK identifier from an existing page, check which folder it came from.

Do not write new pages under `convai-web-sdk-1/`. It is documentation of a deprecated package, kept for
readers who have not migrated.

## GitBook variables

`.gitbook/vars.yaml` in the documentation repository is the only authority for values. No Web SDK
variables are defined there yet, and the current Web pages hard-code or omit version numbers.

| Variable | Holds | Derive from | Used in |
|---|---|---|---|
| `web_sdk_version` | Current `@convai/web-sdk` release version | The package's published version | Install steps, release references |
| `web_package_name` | The npm package name | The package manifest | Install steps, import examples |
| `dashboard_url` | Convai dashboard URL | Stable product URL | API key and character ID steps |

**Add these to `.gitbook/vars.yaml` before the first Web page is written**, and reference them with
`<code class="expression">space.vars.web_sdk_version</code>`. Do not carry the current version into this
pack — a value frozen here goes stale and becomes a wrong fact.

## Gold-standard example pages

**No Web page currently meets the quality bar.** Every page sampled carries a body `#` H1, none set
`title` frontmatter, the current README opens with `## Introduction` and closes with `## Conclusion`,
and no page uses `space.vars`.

Until a Web page is written to standard and accepted, model structure on the Unity SDK section, which
does meet the bar:

| Mode | Model page |
|---|---|
| How-to | `plugins-and-integrations/convai-unity-sdk/getting-started/installation.md` |
| Hub | `plugins-and-integrations/convai-unity-sdk/README.md` |

Take the structure, frontmatter, block usage, and heading discipline. The audience is close enough that
the voice transfers, unlike the product packs.

**When the first Web page is written to standard and accepted, replace this section with its path.**

## Section layout

```
plugins-and-integrations/web-plugins/
├── README.md                      area hub
├── convai-web-sdk/                the current SDK
│   ├── README.md                  SDK hub
│   ├── quickstart.md              entry point
│   ├── react/                     React bindings
│   ├── vanilla-typescript/        framework-free API
│   └── <feature>.md               one page per feature
└── convai-web-sdk-1/              legacy SDK, deprecated — do not extend
```

The `react/` and `vanilla-typescript/` split is a real fork in the reader's path, not a variant of one
page. Keep them as separate pages rather than collapsing them into tabs.

## Platform and version notes

Set `last_reviewed` on any page whose accuracy depends on the package version: install pages, the
quickstart, the core API pages, and the event reference. Set it to the `@convai/web-sdk` version you
verified against.

## SDK source of truth

**Repository:** `Conv-AI/convai-web-sdk_internal`, branch `stable-release`. The path is per-machine —
ask for it when running `/plan-docs web` or `/verify-doc` on a Web page. Do not guess it.

Verify against these:

| Claim | Where |
|---|---|
| Package name, version, entry points, peer dependencies | `package.json` — the `exports` field is the list of public subpaths |
| Config fields, types, defaults | `src/core/types.ts` |
| Client behavior and methods | `src/core/ConvaiClient.ts` |
| React surface | `src/react/` — check `index.ts` for what is actually exported |
| Vanilla surface | `src/vanilla/` |
| Lip sync helpers | `src/lipsync-helpers/` |

The repository also ships a `docs/` directory. **Read it to orient yourself, then verify everything you
take from it against the code**, and never copy its wording — our pages follow `references/`, not
another repository's house style. See "In-repo documentation is a lead, not a source of truth" in
`references/safe-publishing.md`.

An identifier is public only if it is exported from the relevant `index.ts`. Existing in the source is
not the same as being public API — `ConvaiWidgetProps` is the example that caught this pack out.

## Not part of this pack

These live under `web-plugins/` but are different subjects. Do not document them from this pack:

| Subject | What it is | Where it belongs |
|---|---|---|
| `playcanvas-plugin/` | A PlayCanvas engine integration | Its own SDK pack — run `/new-pack playcanvas sdk` |
| `narrative-design-guide/` | The narrative design feature, authored in the Convai Playground | Ownership unresolved — confirm with the Playground owner whether it belongs to `playground.md` before writing here |
| `glb-characters-for-convai.md` | Character asset preparation guidance | Cross-cutting asset guidance, not Web SDK |
| `glb-fbx-animations-for-convai.md` | Animation asset preparation guidance | Cross-cutting asset guidance, not Web SDK |

## Known violations in existing pages

Fix these only on pages the task covers; do not silently rewrite pages the task did not ask about.

| Pattern | What is wrong | What to do instead |
|---|---|---|
| Body `# Title` H1 on every page | Duplicates the GitBook page title | Delete it; start with a headingless lead paragraph. |
| `## Introduction` / `### Overview` opening sections | Forbidden heading | Delete it; fold the content into the lead paragraph. |
| `## Conclusion` closing section | Vague heading that usually restates the page | Replace with `## Next steps` and content refs, or delete. |
| Missing `title` frontmatter | Sidebar label cannot be matched to the page title | Add `title`, identical to the `SUMMARY.md` label. |
| Hardcoded or absent version numbers | Goes stale silently | Use a `space.vars` expression once the variables exist. |
| Legacy method names appearing in current pages | Sends the reader to an API that no longer exists | Check which folder the identifier came from before quoting it. |
