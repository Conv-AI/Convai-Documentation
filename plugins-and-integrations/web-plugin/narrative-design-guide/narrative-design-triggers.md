# Narrative Design Triggers

## Use of Invoke Narrative Design Trigger in Web.

These triggers would be used to navigate through the story graph and activate specific narrative design sections.

In the example bellow calling the trigger (start tour) would activate "Greet User" section.

<figure><img src="../../../.gitbook/assets/image (382).png" alt=""><figcaption><p>Narrative Design Trigger</p></figcaption></figure>

Once the logic is decided we can move to our Javascript code. Where we have initialised convaiClient.\
We can call `convaiClient.invokeTrigger()` whenver we require it in our use case.\
Additional information for context can also be passed as the second argument : message.

```javascript
convaiClient = new ConvaiClient({
        apiKey: "", // Replace with your API key
        characterId: "", // Replace with your character ID
        enableAudio: true,
        faceModal: 3,
        enableFacialData: true,
    });

// in the above scenario triggerName = "Start tour."
convaiClient.invokeTrigger("triggerName", "message");
```
