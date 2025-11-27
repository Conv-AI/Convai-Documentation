---
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/plugins-and-integrations/unreal-engine/guides/creating-metahuman-characters-1/adding-lipsync-to-metahuman
---

# Adding ReadyPlayerMe Character

## Steps to add a ReadyPlayerMe Character

1.  Create a new blueprint and select `ConvaiRPM_Character` as the parent class which you can find under `All Classes` .

    <figure><img src="../../../../.gitbook/assets/image (105).png" alt=""><figcaption></figcaption></figure>
2.  Drag the blueprint to the scene and the default ReadyPlayerMe character should appear.

    <figure><img src="../../../../.gitbook/assets/image (106).png" alt=""><figcaption></figcaption></figure>
3.  Create a new character on [Convai Playground](https://convai.com/pipeline/dashboard) and copy the Character ID, you can also edit the avatar by clicking on the `Edit Avatar` icon on the top right of the avatar preview window.<br>

    <figure><img src="../../../../.gitbook/assets/image (109).png" alt=""><figcaption></figcaption></figure>
4.  Back to Unreal, click the character in the scene and under the details panel find the Char ID field and paste the copied character ID into it.

    <figure><img src="../../../../.gitbook/assets/image (107).png" alt=""><figcaption></figcaption></figure>
5.  Hit `Play` , and wait for a few seconds then the character should now load into the game.

    <figure><img src="../../../../.gitbook/assets/image (110).png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
The first time the character loads will take more time but after that it will be cached and loaded faster.
{% endhint %}
