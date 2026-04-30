# Phase 2: Custom Actions

Phase 1 used the four shipped default actions. Now you'll add your **own action** with no parameters and wire it to a Blueprint event. By the end of this phase, asking the bot _"print hello"_ will run your Blueprint code.

### What you'll need

* The Phase 1 setup working — chatbot in a level, `Enable Actions` ticked, NavMesh in place, character locomotion set up.
* The character Blueprint asset open (or accessible).

### Step 1 — Declare the action template

1. Select the Convai character actor in the level.
2. In the Details panel, find the **Convai Chatbot** component → **Convai → Actions → Environment → Actions**.
3. Click **`+`** to add a new entry. UE expands an `FConvaiAction` struct.
4. Fill in:
   * **Name**: `Print` (this is the canonical action name your handler will dispatch on).
   * **Description**: `Print a debug message to the screen`.
   * Leave **`Parameters`** empty.

The **`Rendered String`** field below auto-populates with:

```
Print — Print a debug message to the screen.
```

That's the wire-format string sent to the LLM. As you edit the Name or Description, the rendered string updates live.

### Step 2 — Bind a handler in Blueprint

The chatbot fires `OnActionReceivedEvent_V2` whenever the bot decides to act. You react to it in the character's Blueprint.

1. Open your character Blueprint.
2. In the **Components** tab, click the **Convai Chatbot** component to select it.
3. In the **Details** panel for that component, find the **Events** category. Click the **`+`** next to **`On Action Received Event V2`**. UE drops a bound event into the Event Graph.
4. The event delivers a **`Sequence Of Actions`** array (each entry is an `FConvaiResultAction`) plus references to the Chatbot Component and the interacting Player Component.

### Step 3 — Dispatch by action name

Inside the bound event, **for each** action in the array:

1. **Get** `Action` (the canonical name string).
2. **Switch on String** with cases for each action you've declared:
   * `Print` → call your custom logic, then `Handle Action Completion(Is Successful=true, Delay=0)`.
   * **Default** → call `Handle Action Completion(Is Successful=true, Delay=0)` to keep the queue moving (or leave un-handled actions to retry — that's an `Is Successful=false` case).

For the `Print` case:

1. Drag a **`Print String`** node off the execution pin and feed it a literal `"Hello from Convai!"` (or read from the Action — but for this phase the action has no params).
2. After the print, drag in **`Handle Action Completion`** off the chatbot reference. Set:
   * **Is Successful**: `true` (the action ran).
   * **Delay**: `0`.
   * Leave **Event Text** empty (advanced field) — this is for when you want to push an outcome back into the bot's dynamic context. Empty = no event.

That's the full handler. The bot now knows how to execute `Print`.

### Step 4 — Play test

Hit **Play** and ask the character: _"Print hello."_

In the editor's viewport you should see `"Hello from Convai!"` (or whatever literal you used) appear via Print String. The bot will also speak its acknowledgment.

### How the pipeline runs end-to-end

When the LLM emits an action:

1. The server sends `{name: "Print"}` (no target, no params).
2. The plugin's parser finds the `Print` template by name in your `Environment.Actions`.
3. Since the template has no declared parameters, `Parameters` stays empty.
4. `OnActionReceivedEvent_V2` fires on the chatbot with the parsed sequence.
5. Your Blueprint dispatches by `Action == "Print"` and runs the print.
6. `Handle Action Completion(true, 0)` advances the queue. If there were more actions in the sequence, the next would now run.

### Why the queue exists

The bot can emit **a sequence** of actions in one response, e.g. _"Wait 2 seconds, then go to the cube, then print done."_ The queue makes sure each action completes before the next one starts. Your handler is responsible for telling the queue when the current action is done — that's what `Handle Action Completion` does.

| Call                                  | Effect                                                        |
| ------------------------------------- | ------------------------------------------------------------- |
| `Handle Action Completion(true, 0)`   | Mark current action successful, run the next one immediately. |
| `Handle Action Completion(true, 1.5)` | Successful, but wait 1.5s before the next action.             |
| `Handle Action Completion(false, 0)`  | Retry the same action.                                        |

You can also push an outcome event into the bot's context in the same call — useful for narration:

```
Handle Action Completion(true, 0, EventText="Printed the message", ShouldRespond=Auto)
```

### When things go wrong

If your handler can't recover (the target is gone, preconditions failed), don't retry forever — **abort the whole sequence** and let the LLM replan:

```
Abort Action Sequence(EventText="Couldn't print — screen is off", ShouldRespond=Always)
```

This clears the rest of the queued actions and fires a context event so the LLM acknowledges and likely emits a new action plan on its next turn.

### Recap

You added one action template, wrote one handler, and got the bot doing custom things. The next step is **typed parameters** — telling the LLM that an action takes a number, an actor reference, or one-of-N choices. Onward to Phase 3 — Parameterized Actions.
