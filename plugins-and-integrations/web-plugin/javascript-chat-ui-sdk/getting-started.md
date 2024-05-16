---
description: >-
  Begin building web applications with our quick start guide for the JavaScript
  Chat UI SDK
---

# Getting Started

At first import ChatBubble component and useConvaiClient hook from convai-chatui-sdk.

```javascript
import ChatBubble,{ useConvaiClient } from "convai-chatui-sdk";
```

Invoke the `useConvaiClient` hook in your application, passing `characterId` and `apiKey` as parameters, then store the returned states in a `client` variable for future reference.

```javascript
const { client } = useConvaiClient(characterId, apiKey);
```

In the return statement of your component, render the `ChatBubble` component that was imported via the NPM package.

```javascript
return (
      <ChatBubble
        chatHistory="Show"
        chatUiVariant="Sequential Line Chat"
        client={client}
      />
  );
```

