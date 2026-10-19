---
title: Build a website assistant
description: Add one Convai character to every page of your website that knows which page the visitor is on and can navigate, highlight elements, and fill in forms for them.
icon: compass
---

In this tutorial we will add a website assistant to a multi-page site: one Convai character that follows the visitor from page to page, answers questions about what is on screen, and acts on requests such as "take me to pricing" or "put my email in the contact form". By the end, you will have an assistant panel on every page that moves the visitor around the site by text or voice.

## What we will build

We will build an assistant for a sample site with a Home, Pricing, Docs, and Contact page. The assistant does four things:

- **Knows where the visitor is.** Each time the page changes, the site sends the character the page name, its elements, and its text.
- **Acts on the site.** The character chooses actions such as `Navigate To Pricing page` or `Highlight Start free trial button`, and the site runs them.
- **Hears back.** After running an action, the site tells the character what happened, so its next reply is accurate.
- **Keeps one conversation.** The visitor keeps talking to the same session across page changes and reloads.

Your application stays responsible for every action: the character only names one, and your code decides whether and how to run it.

The steps use framework-free TypeScript and a History API router. The same calls work in React, Vue, or a server-rendered site. See [Use it in React](#use-it-in-react) for the React version.

## Prerequisites

- Convai Web SDK 1.9.4 or later. See [Web SDK quickstart](../quickstart.md).
- A Convai character and an API key. For production, connect with an auth token instead of an API key. See [Connect with an auth token](../auth-tokens.md).
- The pages of your site and the elements the assistant may point at.

The assistant works with Convai and with self-hosted deployments, over the default realtime transport and over the SSE transport.

## Describe your site

List the pages and elements the assistant may use. Each `name` is what the character says when it picks an action target, so make the names short and unambiguous. Each `description` helps the character choose.

```ts
// site.ts
export interface SitePage {
  name: string;
  path: string;
  description: string;
}

export interface SiteElement {
  name: string;
  description: string;
  path: string; // the page the element lives on
  selector: string;
}

export const PAGES: SitePage[] = [
  { name: 'Home page', path: '/', description: 'Overview of Acme Robotics and its warehouse robots' },
  { name: 'Pricing page', path: '/pricing', description: 'Plans and prices: Starter, Team, and Enterprise' },
  { name: 'Docs page', path: '/docs', description: 'Setup guides for installing robots' },
  { name: 'Contact page', path: '/contact', description: 'Contact form to reach the sales team' },
];

export const ELEMENTS: SiteElement[] = [
  { name: 'Start free trial button', description: 'Starts a free trial', path: '/pricing', selector: '#start-trial' },
  { name: 'Install guide', description: 'How to install a robot', path: '/docs', selector: '#install-guide' },
  { name: 'Email field', description: 'Email input of the contact form', path: '/contact', selector: '#contact-email' },
  { name: 'Message field', description: 'Message input of the contact form', path: '/contact', selector: '#contact-message' },
];

export function currentPage(): SitePage {
  return PAGES.find((page) => page.path === location.pathname) ?? PAGES[0];
}
```

## Declare the actions

Pass the actions and their possible targets in `actionConfig`. Pages and elements both go into `objects`, so the character can target either one.

```ts
// assistant.ts
import { ConvaiClient, type ConvaiAction } from '@convai/web-sdk/core';
import { ELEMENTS, PAGES, currentPage, type SitePage } from './site';

const actionConfig = {
  actions: ['Navigate To', 'Highlight', 'Fill Email', 'Fill Message'],
  objects: [
    ...PAGES.map(({ name, description }) => ({ name, description })),
    ...ELEMENTS.map(({ name, description }) => ({ name, description })),
  ],
  characters: [{ name: 'Visitor', bio: 'The person browsing this website' }],
};
```

The configuration is sent when the session connects, so declare every page and element the assistant may need, not only those on the current page. For the full action contract, see [Handle character actions](../actions.md).

## Tell the character where the visitor is

Write a function that describes the current page. Start it with the assistant's role, because each update replaces the previous dynamic info as a whole.

```ts
const ROLE =
  'You are the website assistant for Acme Robotics. Answer questions about the site, and when the ' +
  'visitor asks to go somewhere, see something, or fill something in, perform the matching action. ' +
  'A line starting with "Action result" reports what the website did. If an action you chose has no ' +
  'result, it did not run: say so and choose it again.';

function describePage(page: SitePage): string {
  const visibleText = (document.querySelector<HTMLElement>('main')?.innerText ?? '')
    .replace(/\s+/g, ' ')
    .slice(0, 1500);
  const elements = ELEMENTS.filter((element) => element.path === page.path).map((element) => element.name);
  return [
    ROLE,
    `The visitor is on the ${page.name} (${page.path}).`,
    elements.length ? `Elements on this page: ${elements.join(', ')}.` : '',
    `Page text: ${visibleText}`,
  ].filter(Boolean).join('\n');
}
```

Send the description on connect with `dynamicInfo`, then again with `updateDynamicInfo` whenever the page changes. `updateDynamicInfo` does nothing until the session is ready, so also send it on `botReady`.

```ts
export const client = new ConvaiClient({
  apiKey: 'YOUR_API_KEY',
  characterId: 'YOUR_CHARACTER_ID',
  endUserId: visitorId(),
  characterSessionId: sessionStorage.getItem('assistant-session') ?? undefined,
  startWithAudioOn: false,
  actionConfig,
  dynamicInfo: describePage(currentPage()),
});

client.on('botReady', () => client.updateDynamicInfo(describePage(currentPage())));

// Call this from your router after each page renders.
export function onPageChange(page: SitePage): void {
  client.updateDynamicInfo(describePage(page));
}
```

Keep the page text short. A summary of what is visible is enough for the character to answer questions about it.

{% hint style="success" %}
Open the Pricing page and ask "Which page am I on?". The character names the Pricing page and can answer questions about its plans.
{% endhint %}

## Keep one conversation across pages

`endUserId` identifies the visitor, and `characterSessionId` resumes their conversation. Store the visitor ID for good, and store the session ID for the browser tab, so a reload or a full page load continues the same conversation.

```ts
function visitorId(): string {
  let id = localStorage.getItem('assistant-visitor-id');
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem('assistant-visitor-id', id);
  }
  return id;
}

client.on('characterSessionId', (id: string) => sessionStorage.setItem('assistant-session', id));
```

In a single-page app, create the client once at the root and keep it connected while the visitor moves between routes. In a site with full page loads, create it on every page: the stored session ID picks the conversation up where it stopped. The client's chat messages start empty on each connection, so the panel is blank after a full page load while the character still remembers the conversation. To show earlier turns, keep your own copy of the transcript in `sessionStorage`. To give a signed-in visitor long-term memory, use their account ID as `endUserId`. See [Use long-term memory](../long-term-memory.md).

## Run the actions

Subscribe to `actionResponse`. Each event carries the actions for one turn in order, so run them one after another.

```ts
client.on('actionResponse', ({ actions }: { actions: ConvaiAction[] }) => {
  void runActions(actions);
});

async function runAction({ name, target }: ConvaiAction): Promise<string> {
  switch (name) {
    case 'Navigate To': {
      const page = PAGES.find((p) => p.name === target) ?? pageNamedIn(lastVisitorText);
      if (!page) return 'failed, unknown page';
      navigate(page.path); // your router
      return `done, now on the ${page.name}`;
    }
    case 'Highlight': {
      const element = ELEMENTS.find((e) => e.name === target);
      if (!element) return 'failed, unknown element';
      if (element.path !== location.pathname) navigate(element.path);
      return spotlight(element.selector) ? 'done' : 'failed, element not on screen';
    }
    case 'Fill Email':
      return fill('/contact', '#contact-email', valueFrom(target, /[\w.+-]+@[\w-]+\.[\w.-]+/));
    case 'Fill Message':
      return fill('/contact', '#contact-message', valueFrom(target, /"([^"]+)"/));
    default:
      return 'failed, not supported';
  }
}
```

Convai can also return the target inside the action name, as in `Navigate To: Contact page` with no `target`. `normalize` splits a declared action name from the rest, so both shapes run the same way. `runActions` in [Report what happened](#report-what-happened) applies it before `runAction`:

```ts
const ACTIONS = actionConfig.actions;

function normalize(action: ConvaiAction): ConvaiAction {
  if (ACTIONS.includes(action.name)) return action;
  const name = ACTIONS.find((known) => action.name.toLowerCase().startsWith(known.toLowerCase()));
  if (!name) return action;
  const rest = action.name.slice(name.length).replace(/^[\s:-]+/, '').trim();
  return { name, target: action.target ?? (rest || undefined) };
}
```

The other helpers scroll an element into view and outline it, and type a value into a field:

```ts
function spotlight(selector: string): boolean {
  const element = document.querySelector<HTMLElement>(selector);
  if (!element) return false;
  element.scrollIntoView({ behavior: 'smooth', block: 'center' });
  element.classList.add('spotlight'); // style this class with an outline
  return true;
}

function fill(path: string, selector: string, value: string | undefined): string {
  if (location.pathname !== path) navigate(path);
  const field = document.querySelector<HTMLInputElement | HTMLTextAreaElement>(selector);
  if (!field) return 'failed, field not found';
  spotlight(selector);
  if (!value) return 'failed, no value given: ask the visitor what to enter';
  field.value = value;
  field.dispatchEvent(new Event('input', { bubbles: true }));
  return `done, entered "${value}"`;
}
```

Match targets against your own lists and ignore anything else, so the character can only reach pages and elements you declared. Leave irreversible steps, such as submitting a form or making a payment, to the visitor: highlight the button instead of pressing it.

### Read values from the visitor's message

An action target names one of your declared objects. A free-form value, such as an email address the visitor dictates, is not a declared object, so the action can arrive without a target. Keep the visitor's last message and read the value from it when the target is missing.

```ts
let lastVisitorText = '';
export function rememberVisitorText(text: string): void {
  lastVisitorText = text;
}

function valueFrom(target: string | undefined, pattern: RegExp): string | undefined {
  if (target && pattern.test(target)) return target;
  const match = lastVisitorText.match(pattern);
  return match ? (match[1] ?? match[0]) : undefined;
}

function pageNamedIn(text: string): SitePage | undefined {
  const words = text.toLowerCase();
  return PAGES.find((page) => words.includes(page.name.replace(' page', '').toLowerCase()));
}
```

Call `rememberVisitorText` before `sendUserTextMessage`, and from `messagesChange` for spoken requests, as the next section shows. `pageNamedIn` covers the occasional `Navigate To` that arrives without a target.

## Report what happened

After the actions run, append the results to the character's context without asking for a reply. The character reads them on the next turn, so it can confirm what happened or try again.

```ts
async function runActions(actions: ConvaiAction[]): Promise<void> {
  const results: string[] = [];
  for (const action of actions.map(normalize)) {
    // Skip names you did not declare, rather than reporting them as failures.
    if (!ACTIONS.includes(action.name)) continue;
    results.push(`${action.name}${action.target ? ` ${action.target}` : ''}: ${await runAction(action)}`);
  }
  if (results.length) {
    client.updateContext({ text: `Action result: ${results.join('; ')}`, mode: 'append', run_llm: 'false' });
  }
}
```

Without results, a character that chose an action cannot tell whether it ran, and it may wrongly tell the visitor it did. For the other `updateContext` options, see [Update character context at runtime](../dynamic-context.md).

## Add the chat panel

Render the conversation, send typed messages, and let the visitor talk. `AudioRenderer` plays the character's voice.

```ts
// main.ts
import { AudioRenderer } from '@convai/web-sdk/vanilla';
import type { ChatMessage } from '@convai/web-sdk/core';
import { client, rememberVisitorText } from './assistant';

const transcript = document.querySelector<HTMLOListElement>('#transcript')!;
const composer = document.querySelector<HTMLFormElement>('#composer')!;
const input = document.querySelector<HTMLInputElement>('#message')!;
const mic = document.querySelector<HTMLButtonElement>('#mic')!;

const SPEAKERS: Partial<Record<ChatMessage['type'], string>> = {
  'user-llm-text': 'visitor',
  'user-transcription': 'visitor',
  'bot-llm-text': 'assistant',
};

client.on('messagesChange', (messages: ChatMessage[]) => {
  transcript.replaceChildren(
    ...messages
      .filter((message) => SPEAKERS[message.type] && message.content)
      .map((message) => {
        const item = document.createElement('li');
        item.className = `from-${SPEAKERS[message.type]}`;
        item.textContent = message.content;
        return item;
      }),
  );
  const latest = messages.filter((m) => SPEAKERS[m.type] === 'visitor').at(-1);
  if (latest?.content) rememberVisitorText(latest.content);
});

composer.addEventListener('submit', (event) => {
  event.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  rememberVisitorText(text);
  client.sendUserTextMessage(text);
  input.value = '';
});

mic.addEventListener('click', () => void client.audioControls.toggleAudio());

void client.connect().then(() => new AudioRenderer(client.room));
```

Browsers block sound until the visitor clicks, taps or presses a key on the page, and the client usually connects before that. Start the character's audio on the first interaction, so the visitor hears the very first reply:

```ts
for (const type of ['pointerdown', 'keydown']) {
  addEventListener(type, () => void client.room.startAudio(), { once: true });
}
```

The panel is plain HTML: an ordered list for the transcript and a form with a microphone button, a text input, and a **Send** button. Fix it to the side of the page so it stays put while the page underneath changes.

## Try the assistant

Start your site, wait for the panel to connect, and try these requests in order:

1. "Take me to the pricing page." The site opens the Pricing page.
2. "What does the Team plan cost?" The character answers from the page text.
3. "Show me the free trial button." The button scrolls into view and is outlined.
4. "Go to the contact page and put jane@example.com in the email field." The site opens the Contact page and fills in the email field, from one request.
5. "Did that work?" The character confirms, based on the action results.

{% hint style="success" %}
The page changes and the elements are outlined as the character speaks, and it confirms the results correctly. Reload the page: the conversation continues where it left off.
{% endhint %}

Select the microphone and say the same requests out loud. Spoken requests produce the same actions.

## Use it in React

`useConvaiClient` takes the same options. Update the context from an effect that runs on route changes, and handle actions in another.

```tsx
import { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useConvaiClient } from '@convai/web-sdk/react';

export function useWebsiteAssistant() {
  const location = useLocation();
  const navigate = useNavigate();
  const client = useConvaiClient({
    apiKey: 'YOUR_API_KEY',
    characterId: 'YOUR_CHARACTER_ID',
    endUserId: visitorId(),
    actionConfig,
    dynamicInfo: describePage(currentPage()),
  });

  useEffect(() => {
    // Wait a frame so the new route has rendered before reading its text.
    const frame = requestAnimationFrame(() => client.updateDynamicInfo(describePage(currentPage())));
    return () => cancelAnimationFrame(frame);
  }, [client, location.pathname]);

  useEffect(
    () => client.on('actionResponse', ({ actions }) => void runActions(actions, navigate)),
    [client, navigate],
  );

  return client;
}
```

Mount the hook once in your root layout, so the conversation survives route changes.

## Next steps

{% content-ref url="../actions.md" %}
[Handle character actions](../actions.md)
{% endcontent-ref %}

{% content-ref url="../dynamic-context.md" %}
[Update character context at runtime](../dynamic-context.md)
{% endcontent-ref %}

{% content-ref url="../auth-tokens.md" %}
[Connect with an auth token](../auth-tokens.md)
{% endcontent-ref %}

{% content-ref url="../self-hosted-deployments.md" %}
[Connect to a self-hosted deployment](../self-hosted-deployments.md)
{% endcontent-ref %}
