# Phase 1: Default Actions

The chatbot ships with four action templates already registered. With a handful of editor steps and **zero Blueprint scripting**, you can have a Convai character walking to objects, following the player, and waiting on demand.

By the end of this phase your character will respond to spoken instructions like _"Go to the blue cube,"_ _"Now come back,"_ _"Follow me,"_ and _"Stop."_

### What you'll need

* A level with a Convai character actor placed in it (any of the sample characters work).
* One or more objects in the level (the FirstPerson template is perfect for this phase).

### Step 1 — Enable actions on the chatbot

1. **Select the Convai character actor in the level.**
2. In the **Details** panel, scroll to the **Convai Chatbot** component (typically appears under the actor's Components list — click on it).
3. Find the **Convai → Actions** category.
4. Tick the **`Enable Actions`** checkbox.

{% hint style="info" %}
This toggle controls whether the chatbot's `Environment` is serialized as `action_config` at `/connect` time. Without it, the server treats the bot as conversational-only.
{% endhint %}

<figure><img src="../../../.gitbook/assets/image (2).png" alt=""><figcaption></figcaption></figure>

### Step 2 — Register an object

The bot can only target things you've told it about. Add the cube to the chatbot's `Environment.Objects` list:

1. In the same **Convai → Actions** category, find the **`Environment`** struct.
2. Expand it, then expand **`Objects`**.
3. Click the **`+`** to add a new entry.
4. Fill in:
   * **Name**: `cube` (this is the human-friendly token the LLM will use — keep it short and unambiguous).
   * **Description**: `A blue cube on the floor`.
   * **Ref**: pick the cube actor in the scene from the dropdown.

You can add as many objects as you like — repeat for each cube and any other prop the bot should know about.

<figure><img src="../../../.gitbook/assets/image (3).png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
Tip: stable, distinct names matter. _"red cube"_ and _"blue cube"_ are easy for the LLM to pick between; _"cube"_ and _"cube2"_ aren't.
{% endhint %}

### Step 3 — Make the character movable

The default `Move To` and `Follow` actions need the character to actually be able to walk. Convai ships an editor utility that wires this up for you:

1. In the **Content Browser**, navigate to your character Blueprint.
2. **Right-click the asset** → **Convai** → **Setup Convai Pawn Movement**.

<figure><img src="../../../.gitbook/assets/image (4).png" alt=""><figcaption></figcaption></figure>

What this does, depending on the Blueprint's parent class:

* **Pure `Actor` parent** → reparents to `APawn`, then adds a `FloatingPawnMovement` component with Convai-tuned defaults (max speed `375`, acceleration `200`, deceleration `250`, turning boost `3`).
* **`APawn` parent (not Character)** → adds `FloatingPawnMovement` if missing, applies the same defaults.
* **`ACharacter` parent** → leaves the existing `CharacterMovementComponent` alone but tunes the same defaults on it (max walk speed, max acceleration, braking deceleration).
* **Anything else** (e.g. a custom `AActor` subclass with a different hierarchy) → leaves the parent untouched and **logs a warning** asking you to reparent to something that eventually inherits from `APawn` (recommended, since `ACharacter` requires a capsule collision component which not every setup wants).

> If you wrote your character from scratch on a non-Pawn base class, the easiest fix is to reparent to `APawn` (the pawn-movement path is lighter) and re-run this menu option.

### Step 4 — Add a NavMesh

The movement components above use Unreal's navigation system, so you need a **NavMeshBoundsVolume** covering the area you want the bot to walk on.

1. From the **Place Actors** panel (or the level editor's "Quickly add to the project" button), drop a **NavMeshBoundsVolume** into the level.
2. Scale it so it covers the entire walkable ground area.
3. Press **`P`** with the level editor focused — this toggles the green navigation overlay. You should see green covering the floor wherever the bot is allowed to walk. If a region isn't green, the volume isn't covering it (or the geometry is unwalkable — too steep, too narrow).

<figure><img src="../../../.gitbook/assets/image (466).png" alt=""><figcaption></figcaption></figure>

### Step 5 — Play test

Hit **Play**. With the chatbot connected, try:

* _"Go to the cube."_ → the bot walks to the cube actor.
* _"Now come back to me."_ → it walks back. (The `bAutoFillConversationPartnerFromPlayer` toggle on the chatbot — on by default — registers the player automatically so _"me"_ resolves correctly.)
* _"Follow me."_ → it tracks the player.
* _"Stop."_ → it halts.
* _"Wait for 5 seconds, then go to the cube."_ → it waits, then moves.

These are the four shipped default actions:

| Action          | Description                                                    |
| --------------- | -------------------------------------------------------------- |
| **Move To**     | Move the character to a target location (Object or Character). |
| **Follow**      | Follow a character.                                            |
| **Stop Moving** | Stop the current movement.                                     |
| **Wait For**    | Wait for a duration in seconds.                                |

You can edit these — change the descriptions, prune the list, add your own — under **Convai → Actions → Environment → Actions** in the Details panel.

### Troubleshooting

* **Bot acknowledges but doesn't move** → most often the NavMesh isn't covering where it's trying to go. Press `P` and check.
* **Bot walks oddly slowly / fast** → tune `MaxSpeed` (or `MaxWalkSpeed` for Character) on the movement component.
* **Bot says "I don't know what cube you mean"** → the `Name` field on the Object entry doesn't match what you're saying, or there's no `Ref` assigned. Both are needed.
* **"Setup Convai Pawn Movement" did nothing** → the warning log will tell you why. Open the Output Log (Window → Output Log) and search for `ConvaiContentBrowserContextMenu`.

When you're ready to add your own actions, head to Phase 2 — Custom Actions.
