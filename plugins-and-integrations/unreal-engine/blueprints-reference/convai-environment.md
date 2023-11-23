---
description: >-
  The Convai Environment class is used to define what actions are available for
  the character and what are the objects and other characters in the scene.
---

# Convai Environment

**Convai Environment** is used as input to the `StartTalking()` or `SendText()` functions in the [Convai Player ](broken-reference)component, and it allows the character to generate actions.

{% hint style="info" %}
A **Convai Environment** object must have a **Main Character** set to be considered valid.
{% endhint %}

<figure><img src="../../../.gitbook/assets/image (209).png" alt=""><figcaption><p><strong>Convai Environment class</strong> blueprint functions schematic - Omitting some functions for improved visibility.</p></figcaption></figure>

## Functions

<table><thead><tr><th width="347.3333333333333">Function</th><th width="98">Returns</th><th>Description</th></tr></thead><tbody><tr><td><code>CreateConvaiEnvironment()</code></td><td>UConvaiEnvironment*</td><td>Creates a Convai Environment object.</td></tr><tr><td><code>SetMainCharacter(FConvaiObjectEntry InMainCharacter)</code></td><td>void</td><td>Assigns the main character initiating the conversation, typically the player character, unless the dialogue involves non-player characters talking to each other.</td></tr><tr><td><code>AddAction(FString Action)</code></td><td>void</td><td>Adds an action to the Environment object</td></tr><tr><td><code>AddActions(TArray ActionsToAdd)</code></td><td>void</td><td>Adds an array of actions to the Environment object</td></tr><tr><td><code>RemoveAction(FString Action)</code></td><td>void</td><td>Remove an action from the environment object.</td></tr><tr><td><code>RemoveActions(TArray ActionsToRemove)</code></td><td>void</td><td>Removes an array of actions from the Environment object</td></tr><tr><td><code>ClearAllActions()</code></td><td>void</td><td>Remove all actions from the Environment object. </td></tr><tr><td><code>AddObject(FConvaiObjectEntry Object)</code></td><td>void</td><td>Adds an object to the Environment object</td></tr><tr><td><code>AddObjects(TArray ObjectsToAdd)</code></td><td>void</td><td>Adds an array of objects to the Environment object</td></tr><tr><td><code>RemoveObject(FString ObjectName)</code></td><td>void</td><td>Remove an object from the environment object.</td></tr><tr><td><code>RemoveObjects(TArray ObjectNamesToR</code>emove)</td><td>void</td><td>Removes an array of objects from the Environment object</td></tr><tr><td><code>ClearObjects()</code></td><td>void</td><td>Remove all objects from the Environment object. </td></tr><tr><td><code>AddCharacter(FConvaiObjectEntry Character)</code></td><td>void</td><td>Adds a character to the Environment object</td></tr><tr><td><code>AddCharacters(TArray CharactersToAdd)</code></td><td>void</td><td>Adds an array of characters to the Environment object</td></tr><tr><td><code>RemoveCharacter(FString CharacterName)</code></td><td>void</td><td>Remove a character from the environment object.</td></tr><tr><td><code>RemoveCharacters(TArray CharacterNamesToRemove)</code></td><td>void</td><td>Removes an array of characters from the Environment object</td></tr><tr><td><code>ClearCharacters()</code></td><td>void</td><td>Remove all characters from the Environment object. </td></tr></tbody></table>
