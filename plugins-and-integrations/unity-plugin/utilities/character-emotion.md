---
description: In this guide, we learn about character emotion coming from server
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/plugins-and-integrations/unity-plugin/utilities/character-emotion
---

# Character Emotion

Convai Character emit character emotions when they interact with the player and these emotions help in making the character more human-like, we are starting to implement a system which you as a developer can use to make your game more interactive using the character emotions.

Whenever the character responds to the user, we send back a list of emotions to the SDK, which look something like this

<figure><img src="../../../.gitbook/assets/Character Emotions.png" alt=""><figcaption></figcaption></figure>

For v0 of this system, we will only be sending the emotions, in future we will apply the facial expressions corresponding to each emotion which will make the character more interactive.
