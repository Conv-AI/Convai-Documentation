---
description: Ask your NPC to perform actions using our JavaScript SDK
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/plugins-and-integrations/web-plugins/convai-web-sdk/actions
---

# Actions

To set up the Actions you need to follow the following steps:

1. Sign in to [Convai's website](https://convai.com/) and navigate to your Character Details.
2. Navigate to Actions, enable the Action Generation and select the actions you want your NPC to perform.
3. Go back to your code and Initialize an actionText state that will store the action that you want NPC to perform.

```javascript
const [actionText, setActionText] = useState("");
```

3. Inside the same useEffect where we check the audio response. Refer to the [Getting Started](getting-started.md) page to quickly understand how and where we check audio response.

```javascript
useEffect(()=>{

------------------------------------------------------------------------
//First Initialize Convai Client here. Refer Getting Started Page
//setResponseCallback method to be called after initializing the client
//onAudioPlay and onAudioStop methods need to be setup
------------------------------------------------------------------------

if (response.hasActionResponse()) {
        let actionResponse = response.getActionResponse();
        let parsedActions = actionResponse.getAction().trim().split("\n");
        setActionText(parsedActions[0].split(", "));
  }
 },[])
```

Actions have been set up and now you can use the ActionText to perform the required action.
