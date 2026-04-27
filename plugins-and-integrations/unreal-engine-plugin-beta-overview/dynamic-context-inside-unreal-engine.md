---
description: >-
  Give AI characters real-time awareness of game state, player actions, and
  environment using Dynamic Context.
---

# Dynamic Context inside Unreal Engine



{% hint style="info" %}
This guide assumes you have the [Convai Unreal Engine plugin](https://www.fab.com/sellers/Convai?lang=en) installed and a Convai-powered AI character is already set up in your scene. If not, please refer to the [installation and setup documentation](https://docs.convai.com/api-docs/plugins-and-integrations/unreal-engine-plugin-beta-overview/installation-and-setup).
{% endhint %}

Dynamic Context is a Convai feature that gives your AI characters a live feed of everything happening in your game. Instead of a character that only responds to what a player says, Dynamic Context enables a character that reacts to the actual state of your virtual world — scores, inventory changes, environmental events, and more — all tracked as named variables injected into the character's reasoning in real time.

### Key Blueprint Functions

| Function                  | Purpose                                              | When to Use                                          |
| ------------------------- | ---------------------------------------------------- | ---------------------------------------------------- |
| `Invoke Speech`           | Triggers the character to speak proactively          | Scene start, scripted events                         |
| `Add Context Event`       | Sends a one-time event notification to the character | Discrete state changes (e.g. player picks up weapon) |
| `Set Context State`       | Tracks a persistent, incrementable variable          | Running counts (e.g. score, bullets fired)           |
| `Get Context State Value` | Retrieves the current value of a tracked variable    | Before incrementing a counter                        |

### Response Modes

Each Dynamic Context function lets you control whether the character speaks after receiving the update:

| Mode     | Behavior                                            | Best For                                 |
| -------- | --------------------------------------------------- | ---------------------------------------- |
| `Always` | Character speaks immediately after the update       | One-time events worth acknowledging      |
| `Auto`   | Character decides when to comment                   | Recurring events like scoring a hit      |
| `Never`  | Context is silently recorded, no response triggered | High-frequency events like bullets fired |

### Tutorial: Virtual Shooting Range

The following walkthrough uses a virtual shooting range to demonstrate all three Dynamic Context functions together. The scene includes a MetaHuman instructor character, a pickup weapon, and a set of target cones.

{% embed url="https://youtu.be/zGIBCWSElXs" %}

#### Step 1 — Trigger a Welcome Message on Scene Load

<figure><img src="../../.gitbook/assets/image (464).png" alt=""><figcaption></figcaption></figure>

* Select your AI character in the scene and click **Edit Blueprint**.
* In the **Begin Play** event, get the `Convai Chatbot Component`.
* Call **Invoke Speech** and set a `Trigger Message` describing the opening scenario — for example: _"Welcome the player to the virtual training range. Be concise."_
* Leave **Generate Actions** and **Replicate on Network** disabled (still under development).
* Compile and Save.

{% hint style="info" %}
Adding **"be concise"** to your trigger message prevents the character from delivering long opening monologues. Welcome messages should orient the player quickly.
{% endhint %}

#### Step 2 — Notify the Character When the Player Picks Up a Weapon

<figure><img src="../../.gitbook/assets/image (463).png" alt=""><figcaption></figcaption></figure>

Use `Add Context Event` for discrete, one-time state changes.

1. Select the **weapon actor** in your scene and click **Edit Blueprint**.
2. Find the **overlap event** that handles the pickup mechanic — specifically the node sequence where the weapon component is added to the player before the actor destroys itself.
3. Before the **Destroy Actor** node, add a reference to the `Convai Chatbot Component` using **Get First Convai Chatbot Component**.
4. Call **Add Context Event** and set the message: _"The player has picked up the gun."_
5. Set **Response Mode** to `Always` — this is a significant state change that warrants an immediate acknowledgment.
6. Connect the node into your existing execution chain, then Compile and Save.

**Why `Add Context Event` and not `Set Context State`?** `Add Context Event` is for things that happen once and shouldn't accumulate — a notification, not a counter. `Set Context State` is for variables the character needs to track across multiple turns.

#### Step 3 — Track Targets Hit

<figure><img src="../../.gitbook/assets/image (460).png" alt=""><figcaption></figcaption></figure>

Use `Set Context State` with increment logic to give the character a running count of targets hit.

1. Select a **target cone** and click **Edit Blueprint**.
2. Scroll to **Events** and add **On Component Hit** — this fires every time the cone is struck by a projectile.
3. Get the `Convai Chatbot Component` and call **Set Context State**.
4. Set the variable name to `targets_shot`.
5. For the value, implement increment logic:
   * Duplicate the Chatbot Component reference and call **Get Context State Value** with the name `targets_shot`.
   * Add a **Branch** node:
     * **Found:** Convert the returned string to integer using **String To Integer**, add `1`, and feed the result into the `Set Context State` value pin.
     * **Not Found:** Pass `1` as the initial value directly.
6. Set **Response Mode** to `Auto` — the character will decide when to comment rather than speaking on every single hit.
7. Compile and Save. Repeat this blueprint on all target actors in the scene (or use a parent class to share the logic).

#### Step 4 — Track Bullets Fired

<figure><img src="../../.gitbook/assets/image (461).png" alt=""><figcaption></figcaption></figure>

Track bullet count silently so the character can calculate accuracy without interrupting gameplay.

1. Open **BP\_WeaponComponent** (found under your First Person blueprints).
2. Locate the **Left Mouse Button** event that spawns the projectile.
3. Copy the full `Set Context State` increment logic from Step 3 and paste it into this blueprint.
4. Rename the variable to `bullets_shot`.
5. Set **Response Mode** to `Never` — the character should record bullet count without speaking on every shot.
6. Compile and Save.

With `targets_shot` and `bullets_shot` both tracked, the character can now calculate accuracy on any turn without you scripting that logic anywhere. For example: 3 targets hit out of 6 shots fired → the character arrives at 50% independently.

#### Step 5 — Add Vision So the Character Can See the Environment

<figure><img src="../../.gitbook/assets/image (462).png" alt=""><figcaption></figcaption></figure>

Dynamic Context covers what the character **knows** about game state. Vision covers what the character can **see**.

1. Select your AI character and click **Edit Blueprint**.
2. In the **Components** panel, click **+ Add** and search for `Environment Webcam`. Add it to the character.
3. In the **Viewport**, position the `EnvironmentWebcam` component at the character's eye level, pushed slightly forward to avoid mesh collision.
4. In the **Content Browser**, create a new folder called `convai_vision`.
5. Inside it, right-click → **Convai** → **Create Vision Render Target**. Name it `RT_Vision`.
6. Return to the character Blueprint, select the `EnvironmentWebcam` component, and set **Convai Render Target** to `RT_Vision`.
7. Enable **Auto Start Vision**.
8. Compile and Save.

The render target now shows exactly what the character sees. Players can ask questions like _"How many targets do you see?"_ and the character will count from its camera view — no pre-baked scripting required.

{% hint style="info" %}
**Dynamic Context + Vision together:** Dynamic Context tells the character what has happened in the game. Vision tells the character what is in front of it. Used together, the character has both situational awareness and environmental perception.
{% endhint %}

### Beyond the Shooting Range

The same blueprint pattern generalizes to any project:

* **Training simulations** — track which procedures have been completed, flag missed steps in real time, let the AI evaluator reference the full session for a rubric-based score.
* **RPGs and open world** — track quest progress, faction standing, items collected. NPCs react to the player's actual game state, not a scripted branch tree.
* **Multiplayer** — each player session carries its own context; characters can address individual players by their score or interaction history.
* **Enterprise simulations** — track trainee responses across a compliance or sales scenario and surface gaps automatically.
