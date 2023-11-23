---
description: >-
  Follow these instructions to enable actions for your Convai-powered
  characters.
---

# Adding Actions to your Character

{% hint style="danger" %}
This feature is currently experimental and can misbehave. You are free to try it out and leave us any feedback.
{% endhint %}

{% hint style="info" %}
[**Download the Actions Version of our plugin from this link**](https://drive.google.com/file/d/1wWyecai-srBuzPrYT7FeeeW-Pk\_ifcJU/view)
{% endhint %}

The actions version of the plugin is a fork of the RPM Version of the plugin. This means that you can easily import characters and play around with them. To use custom characters with the actions version, first set up the character with Convai.

{% content-ref url="importing-custom-characters.md" %}
[importing-custom-characters.md](importing-custom-characters.md)
{% endcontent-ref %}

After setting it up, add the script name ConvaiActionsHandler.cs to the GameObject. This script keeps track of all the actions that the character can do along with an enum that is used internally to trigger the functions corresponding to the actions.&#x20;

<figure><img src="../../.gitbook/assets/image (22).png" alt=""><figcaption></figcaption></figure>

Add the ConvaiGlobalActionSettings.cs to an empty GameObject in the scene. This script will contain all the interactable objects and characters in the scene.

<figure><img src="../../.gitbook/assets/image (23).png" alt=""><figcaption></figcaption></figure>

Add the following fields:

<table><thead><tr><th width="238.5">Field</th><th>Description</th></tr></thead><tbody><tr><td>Characters<br>(in <code>Convai Global Action Settings</code>)</td><td>Characters that are present in the scene.<br>Add the GameObject of the Character and the Description of the Character.</td></tr><tr><td>Objects<br>(in <code>Convai Global Action Settings</code>)</td><td>Interactable Objects that are present in the scene. <br>Add the GameObject of the Interactable Object and the Description of the object.</td></tr><tr><td>Action Methods<br>(in <code>Convai Actions Handler</code>)</td><td><p>Actions that can be performed by the character. </p><p>Add the ActionChoice describing the action and the name of the animation state corresponding to the action (the animation must be present in the animator). </p></td></tr></tbody></table>



## Adding Custom Actions

To add custom actions, edit the ConvaiActionsHandler.cs script.

{% hint style="info" %}
If your action is cosmetic and is only an animation, you do not need to edit the code. Simply select the Action Choice `None`.
{% endhint %}

Add the `ActionChoice` enum at the beginning to identify the action in script.

{% code lineNumbers="true" %}
```csharp
// STEP 1: Add the enum for your custom action here. 
public enum ActionChoice
{
    NONE,
    JUMP,
    CROUCH,
    MOVE_TO,
    PICK_UP,
    DROP,
    DANCE,
    // add your action choice enum here.
}
```
{% endcode %}

Add the Function call corresponding to the action and the `ActionChoice` enum in the switch case in the `DoActions()` function.

```csharp
public IEnumerator DoAction(ConvaiAction action)
{
    // STEP 2: Add the function call for your action here corresponding to your enum.
    //         Remember to yield until its return if it is a Enumerator function.

    switch (action.verb)
    {
        case ActionChoice.MOVE_TO:

            yield return MoveTo(action.target);

            break;

        case ActionChoice.PICK_UP:

            yield return PickUp(action.target);

            break;

        case ActionChoice.DROP:

            Drop(action.target);

            break;

        case ActionChoice.DANCE:

            yield return Dance();

            break;

        case ActionChoice.JUMP:

            Jump();

            break;

        case ActionChoice.CROUCH:

            yield return Crouch();

            break;

        // Add a new case with the ActionChoice Enum.
        // Call the function in this Case.

        case ActionChoice.NONE:

            yield return AnimationActions(action.animation);

            break;

        default:

            break;
    }

    yield return null;
}
```

Add the Function that the action will be doing at the end.&#x20;

Now, add the corresponding animation to the Animator. Take note of the animation state.

<figure><img src="../../.gitbook/assets/image (37).png" alt=""><figcaption><p>Add the animation for the new action.</p></figcaption></figure>

Finally, in the Action Methods add the action information.

<figure><img src="../../.gitbook/assets/image (175).png" alt=""><figcaption><p>Add the new action information to the action methods array.</p></figcaption></figure>

{% hint style="info" %}
If your action is cosmetic and is only an animation, you do not need to edit the code. Simply select the Action Choice `None`.
{% endhint %}
