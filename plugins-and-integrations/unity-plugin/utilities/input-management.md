---
description: >-
  Input Management - Efficiently handle input for Convai's Unity plugin
  integration.
---

# Input Management

{% hint style="success" %}
Make sure that **Active Input Handling** in&#x20;

"_Project Settings > Player_" is set to **Both** or **Input System Package (New)**.&#x20;

Our recommendation is Both. This way, you can use both the new and old input systems. Using the old input system can be faster when creating inputs for testing purposes.
{% endhint %}

<figure><img src="../../../.gitbook/assets/ActiveInputHandling (1).png" alt=""><figcaption></figcaption></figure>

## How to Change the Talk Button or Any Input?

1. Click on the "**Convai Input Manager**" object in your scene.

<figure><img src="../../../.gitbook/assets/SelectInputManagerObject.png" alt=""><figcaption></figcaption></figure>

2. Find the Input Action you want to change in the Inspector. If you want to add a new Input Action, refer to this documentation. In this case, we selected "**Talk Key Action**" to change the talk button. Double-click on "**T \[Keyboard]**".

<figure><img src="../../../.gitbook/assets/InputManagerInspector.png" alt=""><figcaption></figcaption></figure>

4. In the opened window, click on the " **T \[Keyboard** " button in the Path field.

<figure><img src="../../../.gitbook/assets/PressPathButton.png" alt=""><figcaption></figcaption></figure>

5. Press the " **Listen** " button in the top left of the opened window. If you prefer, you can choose your desired input from the categories below.

<figure><img src="../../../.gitbook/assets/PressListenButton.png" alt=""><figcaption></figcaption></figure>

6. Press the key you want to assign.

<figure><img src="../../../.gitbook/assets/PressKey.png" alt=""><figcaption></figcaption></figure>

7. After assigning the desired key, you can see in the Inspector that the input for " **Talk Key Action** " has changed.

<figure><img src="../../../.gitbook/assets/TalkKeyActionChanged.png" alt=""><figcaption></figcaption></figure>

## How to Add a New Input Action?

1. First, open the " **ConvaiInputManager.cs** " script.                                                                                           ( " _Convai / Scripts / Utils / ConvaiInputManager.cs_ " )
2. Create a variable of type **InputAction** in the field where other InputAction variables are located. We'll create an Interaction Key Action for example.

```csharp
public InputAction InteractionKeyAction;
```

<figure><img src="../../../.gitbook/assets/CreateInputActionVariable.png" alt=""><figcaption></figcaption></figure>

3. In the OnEnable method, you need to enable the InputAction you created.

```csharp
InteractionKeyAction.Enable();
```

<figure><img src="../../../.gitbook/assets/EnableInputAction.png" alt=""><figcaption></figcaption></figure>

4. Now, let's create a method to access this InputAction.

```csharp
public bool WasInteractionKeyPressed()
{
#if ENABLE_INPUT_SYSTEM
    return InteractionKeyAction.WasPressedThisFrame();
#else
    return Input.GetKeyDown(KeyCode.E);
#endif
}
```

The **#if ENABLE\_INPUT\_SYSTEM** preprocessor directive ensures that this #if statement will function correctly when you select either **' Both '** or ' **Input System Package (New)** ' in " _Project Settings > Player > Active Input Handling_ "

If you select " **Input Manager (Old)** " for Active Input Handling, the **#else** statement will work. Thus, in the **#else** section, we added the equivalent for the old input system.

<figure><img src="../../../.gitbook/assets/CreateInputActionMethod.png" alt=""><figcaption></figcaption></figure>

5. After applying the above steps, save by pressing " **CTRL+S** " Make sure you've done everything correctly.
6. Return to Unity, click on ConvaiInputManager and in the Inspector, you can see the added Input Action. To assign a key to this Input Action, click the " **+** " button.

<figure><img src="../../../.gitbook/assets/OpenInputManagerInspector.png" alt=""><figcaption></figcaption></figure>

7. In the opened window, click on the " **Add Binding** " button.

<figure><img src="../../../.gitbook/assets/PressPlusIcon.png" alt=""><figcaption></figcaption></figure>

8. Click the " **Listen** " button in the opened window and press the key you want to assign or choose the desired key from the categories.

<figure><img src="../../../.gitbook/assets/PressPathAndListenButton.png" alt=""><figcaption></figcaption></figure>

9. After selecting the desired key, you can see the assigned key under your Input Action in the Inspector.

<figure><img src="../../../.gitbook/assets/Key Added..png" alt=""><figcaption></figcaption></figure>
