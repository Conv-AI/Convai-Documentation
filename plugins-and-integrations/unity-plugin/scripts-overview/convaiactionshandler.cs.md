# ConvaiActionsHandler.cs

{% hint style="warning" %}
Only go through this if you want to customize the behavior of the NPC. Only proceed if you are familiar with gRPC and how to use it in Unity.
{% endhint %}

{% hint style="info" %}
To understand the script in even more depth, please check out the comments in the script.
{% endhint %}

## Class Overview

The `ConvaiActionsHandler` class is a component in Unity used to handle and execute a list of custom actions for a Convai NPC. It allows parsing and processing of user-defined actions, including animations and interactions.

### Requirements

* This class assumes the existence of a `ConvaiInteractablesData` object in the scene to provide global action settings.
* The GameObject containing this script should have a `ConvaiNPC` component attached to it for NPC-related actions.

## Properties

* `actionMethods`: An array of `ActionMethod` objects, defining custom actions with names, animations, and choices.
* `ActionConfig`: An instance of the `ActionConfig` class used to store action configuration data.

### Hidden Fields

* `_actionList`: A list that stores parsed actions to be executed.
* `_actions`: A list of strings representing individual actions extracted from the input string.
* `_currentNPC`: A reference to the `ConvaiNPC` component attached to the GameObject containing this script.
* `_interactablesData`: A reference to the global action settings object, `ConvaiInteractablesData`, in the scene

### Other Reference

* `ActionMethod`: A serializable class used to define individual action methods with name, animation, and choice.
* `ConvaiAction`: A private class used to represent a parsed action with a verb, target GameObject, and animation name.

## Functions

1. `Awake()`: Initializes the Convai Actions Handler, finding global settings and checking for a Convai NPC component.
2. `Start()`: Sets up action configuration, including actions, characters, and objects, and starts playing the action list.
3. `ParseActions(string actionsString)`: Parses a string of actions and matches them with defined Convai actions and global action settings.
4. `PlayActionList()`: Manages playing actions from the action list using a coroutine.
5. `DoAction(ConvaiAction action)`: Executes specific actions based on the `ActionChoice` enum.
6. `AnimationActions(string animationName)`: Plays an animation for the Convai NPC with the provided animation name.
7. `ActionMethod` (Serializable Class): Defines individual action methods with name, animation, and choice.
8. `ConvaiAction` (Private Class): Represents a parsed action with a verb, target GameObject, and animation name.
9. `Crouch()`: Handles the crouching action, including animation and collider adjustments.
10. `MoveTo(GameObject target)`: Moves the Convai NPC to a target GameObject.
11. `PickUp(GameObject target)`: Performs the pick-up action on a target GameObject.
12. `Drop(GameObject target)`: Drops a target GameObject.
13. `Jump()`: Initiates a jump action with a specified jump force.

### Imports

We will import Convai NPC Script which we will use to keep track of the current NPC by which the actions are supposed to be performed by.

```csharp
using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using Service;
using UnityEngine;
using UnityEngine.Serialization;
```

#### ActionChoice

The Action Choice enum is used to display the list of actions in the editor. This helps us choose the action in the script. We use the enum later to choose the function corresponding to the action.

```csharp
// STEP 1: Add the enum for your custom action here.
public enum ActionChoice
{
    NONE,
    JUMP,
    CROUCH,
    MOVE_TO,
    PICK_UP,
    DROP
}
```

#### ActionMethod

This class is used to keep track of the animations and the action enum corresponding to each action. An array of this class is used to keep track of all the actions that the character can perform.

```csharp
[Serializable]
public class ActionMethod
{
    [SerializeField] public string Action;
    [SerializeField] public string animationName;
    [SerializeField] public ActionChoice actionChoice;
}
```

#### ConvaiAction

This class is used to internally track the actions. While parsing the action, we break it down into a verb and, if present, a target. We use this data in our parser.

```csharp
public class ConvaiAction
{
    public ActionChoice verb;
    public GameObject target;
    public string animation;

    public ConvaiAction(ActionChoice verb, GameObject target, string animation)
    {
        this.verb = verb;
        this.target = target;
        this.animation = animation;
    }
}
```

#### Awake()

In the awake function, we initialize the Global Actions settings and get an instance of the current NPC's Convai NPC component.

<pre class="language-csharp"><code class="lang-csharp">// Awake is called when the script instance is being loaded
<strong>private void Awake()
</strong></code></pre>

#### Start()

In the start function, we will initialize the actions config that contains all the actions related information like the actions that the current character can do and objects and the characters present in the scene. It also starts the coroutine `PlayActionList()` that listens and parses the actions that we receive as response from the server.

```csharp
// Start is called before the first frame update
private void Start()
```

#### ParseActions()

The parse actions function takes the string containing the list of actions as an input and breaks it down into an object of ConvaiAction type. It converts the action to a verb and an object (or a target). It also gets a animation corresponding to the action string and the corresponding action enum.&#x20;

After creating the Convai Action object, it adds it to a playlist, that will be played with the `PlayActionList()` function.

```csharp
public void ParseActions(string ActionsString)
```

#### PlayActionList()

This function checks a action playlist and execute the actions in order they are added to the playlist.

```csharp
public IEnumerator PlayActionList()
```

#### DoAction()

The Do Action function uses the action Enum and the Target to execute the function corresponding to the action.

{% code overflow="wrap" %}
```csharp
public IEnumerator DoAction(ConvaiAction action)
{
    // STEP 2: Add the function call for your action here corresponding to your enum.
    //         Remember to yield until its return if it is a Enumerator function.

}
```
{% endcode %}

#### AnimationActions()

The animation Actions function executes actions that do not have a corresponding functions. Specifically cosmetic actions that are only supposed to play an animation.

```csharp
private IEnumerator AnimationActions(string animationName)
```

#### Action Implementation Methods

This region is where we add the functions corresponding to each action.

```csharp
// STEP 3: Add the function for your action here.
#region Action Implementation Methods
    .
    .
    .
#endregion
```

