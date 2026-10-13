---
title: Render links and link previews
description: Turn links the character sends into clickable links, media cards and Open Graph site cards in the Convai widgets or in your own chat UI.
last_reviewed: "1.9.2"
icon: link
---

Render the links a character sends as clickable links with image, video and document cards instead of literal `[Doc](https://…)` markdown. Use this page to turn links on, to add Open Graph site cards through `linkPreviewResolver`, or to render links safely in a chat UI you built yourself.

## Prerequisites

- The Convai Web SDK installed, with a client that connects. See [Web SDK quickstart](quickstart.md).

{% hint style="warning" %}
Links depend on a server-side setting. `preserveLinksInOutput` is a per-session flag sent on `/connect`, and the server default is off. Where the server does not support it, links are stripped before they reach the client and everything on this page renders plain text, with no errors. As of 1.9.0, Convai's hosted servers do not preserve links yet, so plan for plain text until your Convai contact confirms the setting is available for your deployment.
{% endhint %}

## Turn links on

Set `preserveLinksInOutput: true` in the client configuration. `ConvaiWidget` and `createConvaiWidget` render the links with no further wiring.

{% tabs %}
{% tab title="React" %}
{% code title="src/App.tsx" %}
```tsx
import { useConvaiClient, ConvaiWidget } from '@convai/web-sdk/react';

export default function App() {
  const client = useConvaiClient({
    apiKey: 'YOUR_API_KEY',
    characterId: 'YOUR_CHARACTER_ID',
    preserveLinksInOutput: true,
  });

  return <ConvaiWidget convaiClient={client} />;
}
```
{% endcode %}
{% endtab %}

{% tab title="TypeScript" %}
{% code title="src/main.ts" %}
```typescript
import { ConvaiClient } from '@convai/web-sdk/core';
import { createConvaiWidget } from '@convai/web-sdk/vanilla';

const client = new ConvaiClient({
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
  preserveLinksInOutput: true,
});

createConvaiWidget(document.body, { convaiClient: client });
```
{% endcode %}
{% endtab %}
{% endtabs %}

- The flag is read once, when the session connects. To change it, reconnect; a UI toggle that does not reconnect has no effect on the current session.
- The flag is sent as `preserve_links_in_output` and omitted when unset, so the server default applies. If you build the `/connect` request on your server for `connectWithConnectionData()`, add the field there.
- If you render `chatMessages` yourself, expect markdown links in `content` once the flag is on. Speech is unaffected; URLs are never read aloud.

## How each link renders

Both widgets render links the same way. Previews appear on the character's bubble only. The user's own bubble keeps links clickable, with the same hover titles, but never embeds media, so a pasted URL cannot pull remote media into the transcript.

| Link | Character's bubble | Click | If it fails |
|---|---|---|---|
| Web page | Underlined link. Long bare URLs are shortened for display; hover shows the full URL. | New tab | — |
| Image (`png jpg gif webp avif`) | Card with a loading skeleton, then the image and a `host · file` caption. | Opens a lightbox. Escape, the backdrop or **×** close it; **Open original** opens a new tab. | `Preview unavailable — host · file` after an error or 12 seconds without loading. `http:` images on an `https:` page are never requested. |
| Video (`mp4 webm mov ogg`) | Card with native controls. | Play, fullscreen | As for images. |
| Document (`pdf doc docx xls xlsx csv ppt pptx txt md zip`) | File card with an extension tile, the filename and `host · Opens in a new tab`. | New tab | Nothing is fetched, so nothing fails. |
| `mailto:`, `tel:`, `sms:` | Chip with an icon and the address. Hover explains what happens. | Hands off to the operating system | A missing handler is silent by browser design. |
| `ftp:` | Link with an **FTP** badge. Hover warns that most browsers no longer open these. | New tab | The browser refuses silently. |
| `javascript:`, `data:` and other schemes | The label as dotted text, never a link. | Nothing | — |

A message shows at most 6 cards. Further media or document links render as plain links.

The skeleton is a translucent block derived from `currentColor`, so it matches the background the widget sits on. Its shimmer and the lightbox entrance animation are suppressed under `prefers-reduced-motion`.

### Style the cards in the vanilla widget

`createConvaiWidget` exposes `part` attributes you can style from the host page:

| Element | Parts |
|---|---|
| Links | `message-link`, `message-link-badge`, `message-link-blocked`, `message-contact` |
| Media cards | `message-media-card`, `message-media`, `message-media-zoom`, `message-media-skeleton`, `message-media-caption`, `message-media-unavailable` |
| Document cards | `message-file-card`, `message-file-icon`, `message-file-name`, `message-file-meta` |
| Image lightbox | `lightbox`, `lightbox-backdrop`, `lightbox-image`, `lightbox-caption`, `lightbox-close`, `lightbox-open` |
| Site cards | `message-site-card`, `message-site-favicon`, `message-site-name`, `message-site-title`, `message-site-description`, `message-site-image` |

## Add site cards for web pages

A plain web link can show the page's own card: favicon, site name, title, description and image, read from its Open Graph and Twitter tags. A browser cannot fetch another origin's page, so you supply a resolver that asks your backend for the metadata.

{% tabs %}
{% tab title="React" %}
{% code title="src/App.tsx" %}
```tsx
import { ConvaiWidget, useConvaiClient, type LinkPreviewResolver } from '@convai/web-sdk/react';

const resolveLinkPreview: LinkPreviewResolver = async (url, signal) => {
  const res = await fetch(`/api/link-preview?url=${encodeURIComponent(url)}`, { signal });
  return res.status === 200 ? res.json() : null;
};

export default function App() {
  const client = useConvaiClient({
    apiKey: 'YOUR_API_KEY',
    characterId: 'YOUR_CHARACTER_ID',
    preserveLinksInOutput: true,
  });

  return <ConvaiWidget convaiClient={client} linkPreviewResolver={resolveLinkPreview} />;
}
```
{% endcode %}
{% endtab %}

{% tab title="TypeScript" %}
{% code title="src/main.ts" %}
```typescript
import { ConvaiClient } from '@convai/web-sdk/core';
import { createConvaiWidget, type LinkPreviewResolver } from '@convai/web-sdk/vanilla';

const resolveLinkPreview: LinkPreviewResolver = async (url, signal) => {
  const res = await fetch(`/api/link-preview?url=${encodeURIComponent(url)}`, { signal });
  return res.status === 200 ? res.json() : null;
};

const client = new ConvaiClient({
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
  preserveLinksInOutput: true,
});

createConvaiWidget(document.body, {
  convaiClient: client,
  linkPreviewResolver: resolveLinkPreview,
});
```
{% endcode %}
{% endtab %}
{% endtabs %}

`MarkdownRenderer` takes the same function as its `resolveLinkPreview` prop.

- The resolver returns `{ url, title?, description?, image?, siteName?, favicon? }` or `null`. A card is drawn only when the result has a `title` or an `image`.
- Nothing shows while the resolver runs, and nothing shows when it fails or returns `null`. The link itself is unaffected.
- Results are cached per URL for the page load, so a URL named twice costs one request.
- Site cards appear on the character's bubble only and count toward the 6-card limit. Media and document links keep their own cards and are never unfurled.
- `image` and `favicon` are used only when they are absolute `http(s)` URLs. Every other field is rendered as text, never as markup.

Your resolver endpoint fetches pages on the user's behalf. Require a session, refuse private and loopback addresses after DNS resolution, re-check every redirect, cap time and response size, and never forward cookies.

## Render links in your own chat UI

If you use `useConvaiClient` or `ConvaiClient` for the connection but draw your own message list, the character's text reaches you as a plain string. Render it with the SDK's bubble renderer or with its tokenizer.

### Use the bubble renderer in React

`MarkdownRenderer` is the component the React widget draws, so you get the cards, skeletons and scheme allowlist without extra code. Pass `media={false}` on the user's own bubble to keep links but drop embeds.

{% code title="src/Bubble.tsx" %}
```tsx
import { MarkdownRenderer } from '@convai/web-sdk/react';

export function Bubble({ text, isMe }: { text: string; isMe: boolean }) {
  return <MarkdownRenderer text={text} media={!isMe} />;
}
```
{% endcode %}

### Build a renderer on the tokenizer

`parseInlineMarkdown` turns one line of text into nodes you map onto your own markup. It is exported from `@convai/web-sdk/core`, `@convai/web-sdk/vanilla` and `@convai/web-sdk/react`.

{% code title="src/render.ts" %}
```typescript
import { parseInlineMarkdown } from '@convai/web-sdk/core';

for (const node of parseInlineMarkdown(line)) {
  switch (node.kind) {
    case 'link':
      // node.media is 'image' | 'video' | null: the hint for whether to embed.
      renderAnchor(node.href, node.label, node.media);
      break;
    case 'image':
      renderImage(node.src, node.alt);
      break;
    case 'blocked':
      // An unsafe scheme. Show the label as plain text, never as an href.
      renderPlainText(node.label);
      break;
    default:
      renderText(node);
  }
}
```
{% endcode %}

- A link whose closing `)` has not streamed in yet stays text, so bubbles do not flicker between shapes mid-response.
- `compactUrl` shortens a long bare URL for display, such as `a.example.com/…/file.mp4`, without changing the href. Never use its result as an href.
- `linkKindForUrl` and `describeUrl` give you the same classification and `host · file` captions the widgets use, and `resolveLinkPreviewCached` gives you the widgets' shared resolver cache if you draw your own site cards.

## The scheme allowlist

Only `http`, `https`, `ftp`, `ftps`, `mailto`, `tel` and `sms` become links. Everything else, including `javascript:` and `data:`, becomes a `blocked` node, and the widgets render it as text.

{% hint style="warning" %}
Never put a `blocked` node's `href` on an anchor. The server does not sanitise schemes: a markdown link whose target is `javascript:alert(1)` reaches the client unchanged, so the client is the only guard. If you write your own tokenizer instead of `parseInlineMarkdown`, check every href with `isSafeHref` before you render it.
{% endhint %}

## API reference

| Property / Method | Type | Description |
|---|---|---|
| `preserveLinksInOutput` | `boolean` | Client option. Sent on `/connect` as `preserve_links_in_output`. The server default is off. Read once at connect time. |
| `linkPreviewResolver` | `LinkPreviewResolver` | `ConvaiWidget` prop and `createConvaiWidget` option. Open Graph lookup for plain web links; omit it for no site cards. |
| `MarkdownRenderer` | `React.FC<{ text: string; media?: boolean; resolveLinkPreview?: LinkPreviewResolver }>` | The React widget's bubble renderer. `media` defaults to `true`; pass `false` for the user's own bubble. |
| `resolveLinkPreview` | `LinkPreviewResolver` | `MarkdownRenderer` prop for the same lookup as `linkPreviewResolver`. |
| `LinkPreviewResolver` | `(url: string, signal: AbortSignal) => Promise<LinkPreviewMeta \| null>` | Your backend call. |
| `LinkPreviewMeta` | `{ url, title?, description?, image?, siteName?, favicon? }` | What a resolver returns. |
| `resolveLinkPreviewCached` | `(resolver, url) => Promise<LinkPreviewMeta \| null>` | The per-URL cache the renderers share. |
| `parseInlineMarkdown` | `(line: string) => InlineNode[]` | Turns one line of text into `text`, `strong`, `em`, `link`, `image` and `blocked` nodes. |
| `InlineNode` | union type | `{ kind: 'link', href, label, media }`, `{ kind: 'image', src, alt }`, `{ kind: 'blocked', href, label }`, plus `text`, `strong` and `em`. |
| `isSafeHref` | `(url: string) => boolean` | `true` when the URL's scheme is on the allowlist and may be used as an href. |
| `mediaKindForUrl` | `(url: string) => 'image' \| 'video' \| null` | Classifies a URL by file extension; `null` means not previewable. |
| `linkKindForUrl` | `(url: string) => LinkKind` | Presentation class of a safe URL: `web`, `image`, `video`, `document`, `email`, `phone`, `sms` or `ftp`. |
| `LinkKind` | union type | The values `linkKindForUrl` returns. |
| `describeUrl` | `(url: string) => string` | `host · file`, for captions. |
| `compactUrl` | `(url: string, max?: number) => string` | Display-only shortening of a long URL. |
