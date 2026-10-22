---
title: Add a chat widget to a character
description: Add the Convai chat widget to a Convai Embody character so users can type and talk to it over the connection the character already holds.
last_reviewed: "1.0.0-beta.0"
---

Add the Convai Web SDK chat widget beside a Convai Embody character so users can type and speak to it. Use this page after the character renders in your React app. At the end, a message sent from the widget gets a spoken reply that the character lip-syncs.

## Prerequisites

- A character rendered with `ConvaiCharacter` or `CharacterModel`. See [Add a 3D character to a React app](add-a-3d-character-to-a-react-app.md).

## Lift the client out of the character

The character holds the connection. `onReady` hands you the character once its body is loaded and its connection is live, and `character.client` is that connection's `ConvaiClient`. Store it in state outside the canvas, because the widget is DOM and cannot render inside the 3D scene.

## Render the widget

Pass the character's own client to `ConvaiWidget`. The widget subscribes to it, so the chat and the character share one connection. `ConvaiClient` comes from `@convai/embody/react`; `ConvaiWidget` is the chat UI package's, so install it (0.3.0 or later) next to Convai Embody:

```bash
npm install @convai/web-widget
```

{% code title="src/App.tsx" %}
```tsx
import { useState } from 'react'
import { ConvaiCharacter, type ConvaiClient } from '@convai/embody/react'
import { ConvaiWidget } from '@convai/web-widget/react'

export default function App({ token }: { token: string }) {
  const [client, setClient] = useState<ConvaiClient | null>(null)

  return (
    <>
      <ConvaiCharacter
        token={token}
        characterId="YOUR_CHARACTER_ID"
        onReady={(character) => setClient(character.client)}
      />
      {client && <ConvaiWidget convaiClient={client} />}
    </>
  )
}
```
{% endcode %}

{% hint style="warning" %}
Do not create the widget's client with `useConvaiClient`. That hook constructs a second `ConvaiClient`, which opens a second connection: the widget would talk to one session while the character lip-syncs to another, so the character stays silent.
{% endhint %}

## Verify the widget

Type a message in the widget and send it.

{% hint style="success" %}
The reply appears in the widget, the character speaks it, and the character's mouth moves in time with the audio.
{% endhint %}

## Next steps

{% content-ref url="react-api-reference.md" %}
[React API reference](react-api-reference.md)
{% endcontent-ref %}

{% content-ref url="../convai-web-sdk/react/convaiwidget.md" %}
[ConvaiWidget](../convai-web-sdk/react/convaiwidget.md)
{% endcontent-ref %}
