---
description: >-
  This guide shows how to dynamically pass variables to Narrative Design section
  and triggers
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/plugins-and-integrations/unreal-engine/guides/narrative-design/narrative-design-keys
---

# Narrative Design Keys

We will create a simple scenario where the character welcomes the player and asks them about their evening or morning based on the player's time of day.

1. In the playground, enable Narrative Design on your character and change the starting section name to `Welcome`.<br>
2.  Add the following to the Objective field of the Welcome section:\
    `The time of day currently is {TimeOfDay}. Welcome the player and ask him how his {TimeOfDay} is going.` \
    \
    Notice that by adding any string between curly brackets it becomes a variable, and what we did here is adding the time of day as a variable, then from Unreal we can pass either the word "Morning" or "Evening" and the character will respond accordingly.

    <figure><img src="../../../../.gitbook/assets/image (489).png" alt=""><figcaption><p><br></p></figcaption></figure>
3. Back in Unreal, open the character's blueprint.<br>
4.  Set the `Narrative Template Keys` variable with a map containing the same variable name `TimeOfDay` and for demonstration purposes we will hard code the value to "Morning".<br>

    <figure><img src="../../../../.gitbook/assets/image (486).png" alt=""><figcaption><p><br></p></figcaption></figure>
5.  Start the play mode and try it out.<br>

    <figure><img src="../../../../.gitbook/assets/image (487).png" alt=""><figcaption></figcaption></figure>


6. Feel free to try other scenarios and settings to align better with your usecase.



{% hint style="info" %}
* You can use the narrative design keys feature in both sections and triggers.
* Make sure the variable names are between curly brackets and has no spaces in between.
* You can dynamically set, change or clear the narrative keys in Unreal blueprints.
{% endhint %}
