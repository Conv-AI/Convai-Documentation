---
title: Asset ownership and copy-on-write
description: Understand why editing a package-shipped Convai profile creates an editable project copy instead of changing the original asset.
last_reviewed: "4.5.0"
---

Every settings asset an embodiment module ships with — a `ConvaiGazeProfile`, a `ConvaiEmotionProfile`, and the rest — lives inside the Convai package until you change it. The moment you edit one that ships with the package, Convai copies it into your project and points the character at the copy instead of writing to the original. Understanding why explains behavior that otherwise looks like a bug: your edit worked, but not on the file you expected.

***

## Why editing in place is not an option

A profile or settings asset that ships inside the SDK lives under `Packages/com.convai.convai-sdk-for-unity/`. Editing it there is wrong even when Unity happens to allow the write: it is the default every future character inherits, the next SDK update replaces the file, and the change does not travel with your project when you share it or install the SDK on another machine.

So the inspector controls stay live instead of disabled behind a warning. The first edit copies the asset into your project, points the character at the copy, and applies your change there — then tells you what it did afterward. Nothing is asked of you before you are allowed to try; Convai does the bookkeeping the package layout created the need for.

***

## What counts as SDK-owned versus yours

Convai classifies every settings asset into one of four ownership kinds (`SDK/Editor/Ownership/ConvaiAssetOwnership.cs`) before deciding whether an edit needs a copy first:

| Ownership | Meaning | What you see |
| --- | --- | --- |
| None | No asset is assigned. The character runs on the module's built-in defaults. | Nothing — this is the default, unconfigured state. |
| Project-owned | A project asset only this character reads. | No notice. You are already editing exactly what you think you are editing. |
| Project-shared | A project asset that other characters in the open scenes also read. | An info notice naming how many characters share it, with a **Make Unique For This Character** button. |
| SDK-owned | An asset that ships inside the Convai package. | An info notice explaining that the settings ship with the SDK, with a **Create A Project Copy** button. |

Sharing is reported, not blocked — editing several characters that share a profile at once is a choice you can legitimately make. Only an SDK-owned asset requires a copy before an edit means anything.

***

## What happens on the first edit

Change any field on an SDK-owned asset while a character is selected, and Convai:

1. Duplicates the asset into your project.
2. Points the character's component at the copy.
3. Applies your edit to the copy — including any change already made before the copy existed, transferred property by property.
4. Records the whole action as one undo step, named for what happened rather than for the mechanism — for example "Create Nova's own animation settings" rather than "Inspector".

The `.asset` file itself is not covered by Unity's undo system — `AssetDatabase` asset creation never is — so undoing the edit reverts the character's reference but leaves the copied file in the project, where you can find and delete it yourself.

***

## Where the copy lands

The copy lands beside the character's own prefab, when the character has one that lives in your project: a settings asset next to the character it belongs to explains itself. When there is no prefab — a plain scene object, or a prefab that itself lives in a package — the copy lands in `Assets/Convai/<Module>/` instead, where `<Module>` is the module's own folder name, for example `Assets/Convai/Gaze/`. Either way, the file name starts with the character's own name, reduced to letters, digits, and underscores, so a copy made for "Nova (Front Desk)" is still findable by searching for `Nova`.

Duplicating a settings asset from its own inspector, with no character selected, has no character to name the copy after. That copy lands under `Assets/Convai/<AssetTypeName>/` instead, grouped by the asset's type.

{% hint style="warning" %}
A project asset shared by several characters is never copied automatically — only an SDK-owned asset is. Use **Make Unique For This Character** to give one character its own copy of a shared project asset.
{% endhint %}

***

## Next steps

{% content-ref url="character-embodiment.md" %}
[Character embodiment](character-embodiment.md)
{% endcontent-ref %}

{% content-ref url="dialogue-state.md" %}
[Dialogue state](dialogue-state.md)
{% endcontent-ref %}
