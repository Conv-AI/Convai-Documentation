---
description: >-
  This guide shows how to dynamically pass variables to Narrative Design section
  and triggers
---

# Narrative Design Keys

We will create a simple scenario where the character welcomes the player and asks them about their evening or morning based on the player's time of day.

1. In the playground, enable Narrative Design on your character and change the starting section name to `Welcome`.<br>
2.  Add the following to the Objective field of the Welcome section:\
    `The time of day currently is {TimeOfDay}. Welcome the player and ask him how his {TimeOfDay} is going.` \
    \
    Notice that by adding any string between curly brackets it becomes a variable, and what we did here is adding the time of day as a variable, then from Unreal we can pass either the word "Morning" or "Evening" and the character will respond accordingly.<br>

    <figure><img src="../../../.gitbook/assets/image (383).png" alt=""><figcaption><p>Narrative Design Keys</p></figcaption></figure>


3.  Setting Narrative Template Keys in JavaScript

    To initialize your narrative design framework with custom template keys, you can pass the `narrativeTemplateKeys` argument when instantiating the `convaiClient`. This allows you to define and structure your narrative flow programmatically.

```javascript
//example
function getNarrativeTemplateKeys(): Map<string, string> {
  const narrativeKeys = new Map<string, string>();
  // Populate the map with narrative keys and values
  // This could be from a database, configuration file, or other source
  narrativeKeys.set('TimeOfDay', 'Replace it with time');
  narrativeKeys.set('chapter1', 'The journey begins in a small village.');
  // Add more narrative keys as needed
  return narrativeKeys;
}


const client = new convaiClient({
  apiKey: 'your-api-key',
  characterId: 'your-character-id',
  narrativeTemplateKeys: getNarrativeTemplateKeys()
});
```

<br>
