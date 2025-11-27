---
description: Begin building applications with our quick start guide for the Web SDK
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/plugins-and-integrations/web-plugins/convai-web-sdk/getting-started
---

# Getting Started

At first import Convai client from convai-web-sdk.

```javascript
import { ConvaiClient } from "convai-web-sdk";
```

Declare the `convaiClient` variable using the `useRef` hook provided by the React library. The `useRef` hook returns a mutable ref object, which can be used to store a value that persists across component renders.

```javascript
const convaiClient = useRef(null);
```

Initialize the Convai client inside a `useEffect` hook to ensure it runs only once when the component is mounted. By providing an empty dependency array as the second parameter to the `useEffect` hook, the initialization code will be executed only on the initial render.

```javascript
convaiClient.current = new ConvaiClient({
      apiKey: string //Enter your API Key here,
      characterId: string //Enter your Character ID,
      enableAudio: boolean, //use false for text only.
      sessionId: string //use this to save conversation sessions to save conversations
      apiBaseUrl: "https://your-onprem-api",   // REST (character/speaker) base
      webstreamUrl: "wss://your-webstream",    // gRPC websocket host
      disableAudioGeneration: boolean false, //Optional parameter for chat only applications
    });
```

Your Convai Client has been initialized. Now you can use Convai Client methods to set up a conversation with your NPC.&#x20;

These are the main methods that allow you to interact and converse with your NPC using the ConvaiClient.

1. **setResponseCallback**

**Description:** Sets the response callback function for the ConvaiClient instance. This callback function will be invoked when a response is received from the Convai API. This part of the code should be also under the same use effect as the initialization one.

**Parameters:** `callback` (function): A callback function that will be executed when a response is received. It takes one parameter representing the received response data.

**Example:**&#x20;

```javascript
//Declare this part(React hooks) of the code outside the use effect
const [userText, setUserText] = useState("");
const [npcText, setNpcText] = useState("");
const [keyPressed, setKeyPressed] = useState(false);
const [isTalking, setIsTalking] = useState(false);
const finalizedUserText = useRef();
const npcTextRef = useRef();
------------------------------------------------------------------------------------


convaiClient.current.setResponseCallback((response) => {
      if (response.hasUserQuery()) {
        var transcript = response.getUserQuery();
        var isFinal = transcript.getIsFinal();
        if (isFinal) {
          finalizedUserText.current += " " + transcript.getTextData();
          transcript = "";
        }
        if (transcript) {
          setUserText(finalizedUserText.current + transcript.getTextData());
        } else {
          setUserText(finalizedUserText.current);
        }
      }
      if (response.hasAudioResponse()) {
        var audioResponse = response?.getAudioResponse();
        npcTextRef.current += " " + audioResponse.getTextData();
        setNpcText(npcTextRef.current);
      }
    });
```

This part of the code gets the user Query from the response and the finalized text is set as userText which is further used to generate a response from the NPC which is stored as npcText.&#x20;

Also, remember to declare both the `onAudioPlay` and `onAudioStop` methods described below inside the `useEffect` after the `setResposeCallback` method to avoid facing errors.



2. **startAudioChunk**&#x20;

**Description:** Initiates the client to start accepting audio chunks for voice input. This method     signals the client to begin receiving and processing audio data.

**Parameters:** None

**Example:**

```javascript
function handleKeyPress(event) {
    //Whenever the user press [Space] the client will start receiving the audio
    if (event.Code === "KeyT" && !keyPressed) {
      setKeyPressed(true);
      finalizedUserText.current = "";
      npcTextRef.current = "";
      setUserText("");
      setNpcText("");
      convaiClient.current.startAudioChunk();
    }
  }
```

You can use this method to make the client listen and take input of the audio only when the user presses some particular key.



3. **endAudioChunk**

**Description:** Instructs the client to stop taking user audio input and finalize the transmission of audio chunks for voice input. This method indicates the end of the audio input and allows the client to process the received audio data.

**Parameters:** None

**Example:**

```javascript
function handleKeyRelease(event) {
    if (event.Code === "KeyT" && keyPressed) {
      setKeyPressed(false);
      convaiClient.current.endAudioChunk();
    }
  }
```

You can use this method to make the client stop listening to the audio on release of some particular key.



4. **onAudioPlay**

**Description:** Notifies whenever the NPC starts speaking.

**Parameters:** None&#x20;

**Example:**

```javascript
convaiClient.onAudioPlay(() => {
    setIsTalking(true);
  });
```

{% hint style="info" %}
This method can be used to work with animations where once the audio starts we can set the avatar to do `talking` animation.
{% endhint %}



5. **onAudioStop**

**Description:** Notifies whenever the NPC stops speaking.

**Parameter:** None

**Example:**

```javascript
convaiClient.current.onAudioStop(() => {
      setIsTalking(false);
    });
```

{% hint style="info" %}
This method can also be used to work with animations where once the audio stops we can set the avatar to be in `idle` position.
{% endhint %}



6. **sendTextChunk**

**Description:** Can be used to send a text chunk to the client which will further be processed and the NPC output will be generated.

**Parameter:** text (string): Takes a text chunk of type string as input.

**Example:** Can be used when your are using textbox to take user's input. You can set up the text box in the following way where&#x20;

```javascript
const [enter, setEnter] = useState(0);

/*The above state will be used as a trigger, we'll change enter to 1 whenver user
is present in the text box and presses enter, once the content is sent to the client 
we'll again set enter to 0.*/  

function sendText() {
    finalizedUserText.current = "";
    npcTextRef.current = "";
    setNpcText("");
    convaiClient.current.sendTextChunk(userText);
    setEnter(0);
  }

//Handles textBox messages
useEffect(() => {
  if (
    document.activeElement.tagName === "INPUT" ||
    document.activeElement.tagName === "TEXTAREA" ||
    document.activeElement.isContentEditable
  ) {
    if (userText !== "" && enter) {
      sendText();
    }
  }
}, [enter]);
```

You can use this method to get the input from a text box and then send it to the client for processing.



7. **resetSession**

**Description:** Used for resetting the current session.

**Parameter:** None

**Example:**

```javascript
const ResetHistory = () => {
      convaiClient.current.resetSession();
  };
```



8. **toggleAudioVolume**

**Description:** Can be used to toggle audio mode from on to off or vice versa.

**Parameter:** None

**Example:**

```javascript
const ToggleAudioVolume() {
    convaiClient.current.toggle();
  }
```

### Additional Service URL Overrides (REST & gRPC)

For advanced on-premise or enterprise deployments, the Convai Web SDK allows you to override the default Convai API and WebStream endpoints. This is useful when routing traffic through **self-hosted REST services** or **on-premise gRPC WebStream servers**.

#### Available Overrides

| Key            | Description                                                          | Default                        |
| -------------- | -------------------------------------------------------------------- | ------------------------------ |
| `apiBaseUrl`   | Base URL for Convai’s REST API (session, chat, voice, etc.)          | `https://api.convai.com`       |
| `webstreamUrl` | Base URL for the gRPC WebStream server (realtime inference endpoint) | `https://webstream.convai.com` |

These can be supplied when initialising the Convai Web SDK client.

#### Example (React)

```tsx
const convaiClient = useRef(
  new ConvaiClient({
    apiKey: "your-api-key",
    characterId: "your-character-id",
    apiBaseUrl: "https://your-onprem-api.example.com",
    webstreamUrl: "https://your-onprem-webstream.example.com",
  })
);
```

#### Example (Vanilla JS)

```ts
const client = new ConvaiClient({
  apiKey: "your-api-key",
  characterId: "your-character-id",
  apiBaseUrl: "https://your-onprem-api.example.com",
  webstreamUrl: "https://your-onprem-webstream.example.com"
});
```
