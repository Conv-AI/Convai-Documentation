---
description: Simple examples for naming, describing, and testing character actions.
---

# Writing clear action names and descriptions

Actions let your character do things in your project, such as move somewhere, inspect an object, equip an item, or change a setting.

You add them in the **Convai Chatbot Component**, under **Actions**.

## Start with a clear action name

Read the action name and an example value together. The result should be easy to understand.

| Action name       | Parameter     | Example value           | Read together                           |
| ----------------- | ------------- | ----------------------- | --------------------------------------- |
| `Move to`         | `Destination` | `loading dock`          | `Move to loading dock`                  |
| `Inspect`         | `Object`      | `control panel`         | `Inspect control panel`                 |
| `Equip`           | `Item`        | `bronze shield`         | `Equip bronze shield`                   |
| `Set difficulty`  | `Difficulty`  | `Hard`                  | `Set difficulty Hard`                   |
| `Deliver message` | `Message`     | `Meet me at the bridge` | `Deliver message Meet me at the bridge` |
| `Lower bridge`    | None          | None                    | `Lower bridge`                          |

The parameter can already explain what the value is. For example, `Inspect` can have an `Object` parameter. You do not have to call the action `Inspect object` unless that is clearer for your project.

Both versions can work. Choose the one that is easiest for you and your team to read.

## Use parameter names that make sense to you

A parameter is the extra information the action needs. For example:

* `Destination` tells `Move to` where to go.
* `Item` tells `Equip` what to equip.
* `Message` tells `Deliver message` what to deliver.

`Value` is also a valid name. A more specific name can make your setup easier to read, but it is not required.

## Add a short description

A useful description answers the questions that matter for that action:

* When should the character use it?
* What happens when it runs?
* What information should the character include?

A complete example in the description can also help.

### Move somewhere

**Name:** `Move to`

**Parameter:** `Destination`

> Use this action when the user asks the character to go somewhere. It moves the character to that place. Include the destination. Example: Move to loading dock.

{% hint style="info" %}
Notice how we added "Example: Move to loading dock" as an example in the description.
{% endhint %}

### Inspect something

**Name:** `Inspect`

**Parameter:** `Object`

> Use this action when the user asks the character to inspect something. It starts the inspection in the game. Include the object. Example: Inspect control panel.

### Deliver a message

**Name:** `Deliver message`

**Parameter:** `Message`

> Use this action when the user asks the character to deliver a message. It sends the message through the game. Use it even if the character also replies aloud. Include the full message. Example: Deliver message Meet me at the bridge.

### Choose from a fixed list

**Name:** `Set difficulty`

**Parameter:** `Difficulty`

> Use this action when the user asks to change the difficulty. Include the requested difficulty. Example: Set difficulty Hard.

These examples show the pattern. Describe what your own action really does.

## Choose how the value is entered

Use **Choices** when you want to provide a list of available values.

Use **String** when the action should accept text without a fixed list.

For example, a difficulty action may use Choices such as `Easy`, `Normal`, and `Hard`. A message action may use String because the message can be different each time.

Choose the option that fits your project. Neither option is a general accuracy setting.

## Keep the wording easy to follow

Actions can use Spanish, English, or another language. When possible, keep the action name, parameter, and description in the same language so the setup is easier for people to read.

If the character supports several languages, test the action in each language you plan to use.

## Test more than one sentence

Try the example from the description, then try a few natural variations.

For an `Inspect` action, you could try:

* Direct: “Inspect the control panel.”
* Natural: “Could you take a closer look at that control panel?”
* Should not run: “What does a control panel usually do?”

Repeat important tests in a fresh session. One successful attempt shows that the setup can work; several attempts show how consistently it works.

It can also help to test the action by itself before enabling many similar actions.

## If an action does not run

Check these items:

* Is the action enabled on the character you are testing?
* Does the action name match the event used in your Blueprint?
* Does the parameter name match what your Blueprint expects?
* Does the description clearly say when to use the action?
* Does the description say what information to include?
* If you use Choices, is the value in the list?
* Does the action work when it is the only enabled action?

Also check what reached Unreal:

* No action arrived.
* The action arrived, but a value was missing.
* The action and value arrived, but the game did not use them.

Knowing which one happened makes the next check much easier.
