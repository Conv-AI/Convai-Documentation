---
description: >-
  Follow the retained actions workflow for the deprecated unscoped Web SDK, or
  move to the current Convai Web SDK action event and configuration surface.
metaLinks:
  canonical: >-
    https://docs.convai.com/api-docs/plugins-and-integrations/web-plugins/convai-web-sdk
---

# Actions

{% hint style="warning" %}
**Deprecated on August 26, 2026.** The unscoped `convai-web-sdk` package is no longer supported. Migrate to [Actions in the current Convai Web SDK](../convai-web-sdk/actions.md). This page remains available for historical reference and is not maintained.
{% endhint %}

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
