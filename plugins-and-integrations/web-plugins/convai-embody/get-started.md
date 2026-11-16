---
title: Get started with Convai Embody
description: Create a new React app, render a Convai character as a 3D body with Convai Embody, and talk to it through the Convai chat widget over one connection.
last_reviewed: "1.2.0"
---

Build a page that shows a Convai character as a 3D body and lets you talk to it. Use this page for a first project: it starts from an empty folder and ends with a character that answers you by voice, with lip sync. The chat widget is part of the setup, not an extra, because a body you cannot talk to is a picture of one.

## Prerequisites

- Node.js 18 or later and a package manager.
- A Convai account, an API key from <code class="expression">space.vars.dashboard_url</code>, and a character ID.
- A character whose avatar has a published web body, or a default body that applies to it. A character with neither cannot be rendered. See [Troubleshooting](add-a-3d-character-to-a-react-app.md#troubleshooting).

## Create the app

Create a React app with Vite and install Convai Embody, the chat widget, and their peers. `@convai/web-sdk` holds the connection, `three` and `@react-three/fiber` draw the body, and `@convai/web-widget` is the chat panel.

{% tabs %}
{% tab title="npm" %}
```bash
npm create vite@latest my-character -- --template react
cd my-character
npm install @convai/embody @convai/web-widget @convai/web-sdk three @react-three/fiber
```
{% endtab %}

{% tab title="pnpm" %}
```bash
pnpm create vite my-character --template react
cd my-character
pnpm add @convai/embody @convai/web-widget @convai/web-sdk three @react-three/fiber
```
{% endtab %}
{% endtabs %}

## Add your credentials

Put the API key and character ID in a `.env` file at the project root. Vite exposes variables that start with `VITE_` to the page.

{% code title=".env" %}
```bash
VITE_CONVAI_API_KEY=YOUR_API_KEY
VITE_CONVAI_CHARACTER_ID=YOUR_CHARACTER_ID
```
{% endcode %}

{% hint style="danger" %}
An API key is a workspace-wide credential. Anyone who opens a page that ships it can read it. It is right for a local project like this one. For a public page, create a short-lived auth token on your server and pass `token` instead of `apiKey`. See [Auth Tokens](../convai-web-sdk/auth-tokens.md).
{% endhint %}

## Render the character and the chat widget

Replace the generated `src/App.jsx` with the component below. `ConvaiCharacter` brings its own canvas, camera, lights, and orbit controls, resolves the character's body, opens the connection, and drives the face. `onReady` hands you the character once its body is loaded and its connection is live. The widget takes that same connection, so chat and lip sync share one session.

{% code title="src/App.jsx" %}
```jsx
import { useState } from 'react'
import ConvaiCharacter from '@convai/embody/react'
import { ConvaiWidget } from '@convai/web-widget/react'

export default function App() {
  const [client, setClient] = useState(null)

  return (
    <>
      <ConvaiCharacter
        apiKey={import.meta.env.VITE_CONVAI_API_KEY}
        characterId={import.meta.env.VITE_CONVAI_CHARACTER_ID}
        onReady={(character) => setClient(character.client)}
      />
      {client && <ConvaiWidget convaiClient={client} />}
    </>
  )
}
```
{% endcode %}

If the character has Long-Term Memory turned on, the connection also needs an end-user id so the character can tell your users apart. Pass a stable id for the person using your app: `session={{ endUserId: user.id }}`. Without it, connecting fails with "Missing end\_user\_id".

Do not create the widget's client with the Web SDK's `useConvaiClient`. That hook constructs a second `ConvaiClient`, which opens a second connection: the widget would talk to one session while the character lip-syncs to another, so the character stays silent.

Remove the generated styles so the character fills the window. Replace `src/index.css` with:

{% code title="src/index.css" %}
```css
html, body, #root { margin: 0; height: 100%; }
```
{% endcode %}

## Run the app

```bash
npm run dev
```

Open the printed URL. The body downloads first, which takes a few seconds on a first visit. The character then stands at eye level in the middle of the page with its idle animation playing, and its eyes follow the camera as you drag to turn around it or scroll to move closer. The chat launcher sits in the bottom-right corner.

## Talk to the character

Click the launcher. The widget opens in voice mode with the character's name and portrait. To type instead, click **Exit Voice Mode**, write a message in the **Conversation** box, and press Enter. Voice mode asks for microphone access the first time you use it.

{% hint style="success" %}
The reply appears in the widget, the character speaks it, and the character's mouth moves in time with its voice.
{% endhint %}

## Next steps

{% content-ref url="add-a-3d-character-to-a-react-app.md" %}
[Add a 3D character to a React app](add-a-3d-character-to-a-react-app.md)
{% endcontent-ref %}

{% content-ref url="react-api-reference.md" %}
[React API reference](react-api-reference.md)
{% endcontent-ref %}
