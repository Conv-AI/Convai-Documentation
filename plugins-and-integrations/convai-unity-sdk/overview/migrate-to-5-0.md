---
title: Migrate to SDK 5.0
description: >-
  Update an existing Unity integration for the 5.0 transcript API, player
  identity, microphone policy, native audio libraries, and platform changes.
last_reviewed: "5.0.0-preview"
---

The 5.0 preview changes transcript APIs, local player identity, media behavior, when a character connects automatically and how action parameters are read. Upgrade a copy of your integration, resolve compile errors and verify saved scene bindings before replacing a deployed build.

{% hint style="warning" %}
These instructions describe the reviewed 5.0 release branch, whose package manifest still says `4.6.1` and changelog says Unreleased. Confirm the final package, channel and release notes before upgrading a production project.
{% endhint %}

## Update the package and native libraries

Resolve the seven [package dependencies](../getting-started/prerequisites.md), including `com.unity.collections` `2.6.8`. The native transport moves to the maintained LiveKit Unity 2.1 integration with FFI `0.12.80`. Let the matching downloader install its pinned binaries; do not combine old native libraries with the new managed bindings. See [Native transport libraries](../platform-guides/native-transport-libraries.md).

## Replace transcript integrations

| Previous integration | 5.0 replacement |
| --- | --- |
| Transcript turns and `GetTurns` | Entries and `GetEntries`; stable entry ID, revision and ordered history. |
| One change per subscription callback | `TranscriptChangeBatch` containing entry changes. |
| Append received transcript text | Assign the complete `TranscriptEntry.Text` to the row keyed by entry ID. |
| `SubscribeCommitted` | `SubscribeFinalized`; handle later corrections through the main subscription. |
| `ConvaiCharacter.OnTranscriptReceived(text, isFinal)` | `OnSpokenLine(line)` for spoken lines; the transcript facade for generated/history text. |
| `CharacterTtsTextChunk` | `CharacterSpokenLine`, with `LineIndex` and timing information. |
| Transcript callbacks on `ConvaiEvents` | `ConvaiManager.Transcripts`; raw protocol events remain accessible through the event hub for advanced consumers. |
| Caption Streaming / Stable | Active; also handle Completed, Interrupted and Cleared. |

Check saved `ConvaiCharacterEventRelay` listeners: **On Spoken Line** uses `CharacterSpokenLineRelayData`. `ConvaiTranscriptDisplay` now uses Captions or History mode; old append and partial-transcript controls are removed. The obsolete feedback prefab and handler are not part of this UI integration.

Follow [Migrate transcripts to 5.0](../scripting-reference/migrate-transcripts-to-5-0.md) for subscription, pagination, correction and cleanup examples. A final history entry does not mean its audio has finished.

## Preserve player and memory identity

An empty `ConvaiPlayer.PlayerId` is initialized once from the player name and then remains stable. `Configure(name)` and display-name changes keep it. Call `Configure(name, id)` only when deliberately changing local ownership and attribution. This local ID is separate from the end-user ID sent to Convai.

If a character requires an end-user ID for memory, missing identity now produces `connection.connect_end_user_id_required`. Also handle `connection.connect_ltm_end_user_limit_reached` and `connection.connect_ltm_not_configured` separately. Read the service-confirmed `CurrentEndUserId` and `CurrentLongTermMemoryStatus` rather than assuming a locally requested ID proves memory is active.

Use `client.Memory.GetSettingsAsync` and `UpdateSettingsAsync` in place of the deprecated character memory-toggle helpers. Character memory settings affect service state, so review their scope before changing them. See [Configure end-user ID requirements](../features/long-term-memory/configure-end-user-id-requirement.md).

## Review audio and input

* Reserve each character's voice AudioSource for SDK playback. Move unrelated clips and audio filters to a separate source.
* New microphone policies default to noise suppression on, automatic gain control off and echo cancellation off. Saved scenes keep their values. Processing changes apply on the next connection.
* Use **Allow Microphone** for sessions that must not open capture. Mute alone is not that policy. A runtime `SetMicrophoneAllowed` choice belongs to one session; configure a persistent default when reconnects must remain text-only.
* Use an input lease when driving push-to-talk from custom UI or XR controls. Follow controller state rather than assuming a press lasts until your own release event.
* A custom microphone factory must support capture drain for group conversation. Ordinary rooms can use the legacy fallback; group presses cannot.

Test native spatial playback and voice volume after the audio migration. The carrier-clip path changes how Unity applies panning and gain, so an old scene's perceived level can change.

## Check automatic connection

A character's **Auto Connect** now starts its conversation after initialization or re-enable only when the room allows **Connect On Start**. Before, **Auto Connect** did not read the room's setting. The setting is **Starts Connected** on `ConvaiRoomManager`, or **Connect On Start** on a `ConvaiRoomManagerProfile`. The effective value comes from the profile when the room uses one. Turning it off now also blocks characters that are enabled later during play.

Explicit connection calls are not affected. `ConnectAsync` and `StartConversationAsync` still connect when automatic connection is off.

If a scene relied on **Auto Connect** with **Starts Connected** off, choose one of these:

* Turn **Starts Connected** on, which allows automatic room and character connections.
* Keep it off and call `ConnectAsync` or `StartConversationAsync` from your code.

`ConvaiRoomManager` implements the new `IConvaiRoomStartupConnectionPolicy` interface, and its `AllowsCharacterAutoConnectOnStart` property returns the room's effective **Connect On Start**. A connection service that does not implement the interface leaves **Auto Connect** unrestricted. See [Scene components reference](../getting-started/scene-components.md).

## Review browser and Editor behavior

**WebGL Vision:** Frame Source is now the default publication policy. Game View is explicit, and a missing source can still fall back to the visible canvas. Check that no unintended UI is sent. Browser volume and mute now use `ConvaiAudioOutput`; spatial rolloff remains unavailable.

**Build target:** Activate WebGL before a WebGL build. The build guard rejects a mismatched active target.

**Editor tools:** `Convai.ConfigureRoom` keeps fields you omit. Pass an explicit value when you want a reset. Tool results redact player identity and shorten session IDs; do not parse those fields as complete identifiers. The memory tools introduce remote service writes that preview by default. Five Scene Auto Tagger tools are new: `Convai.FindSceneTagCandidates`, `Convai.TagSceneObjects`, `Convai.GetSceneTagRun`, `Convai.ApplySceneTags` and `Convai.DescribeSceneView`. Tagging uploads captures, so the assistant skill runs it only when asked, and apply previews by default. The MCP tool contract version is now `11`; a client that checks it should expect that value.

**Scene context:** Spatial facts use banded distances and a per-character object cap, and are published only while the character is in conversation. A fact now names the character it is measured from. It reads `Chair: 3 m to Ava's left; visible to Ava; stationary` where it read `Chair: 3.0 m ahead`, so update applications that parse spatial fact text. A logical group's fact describes its nearest member and reads `Name (nearest of N): …`. Attention references must exist in the action configuration: give an object an action target, or list it in the action config, if it should receive attention. Every world object, action targets included, now goes in the scene description, and a new room for a scene with one character receives that description in its connect request. Scenes with more than one character, and rejoins, still send it as a data message limited to 15,360 bytes.

## Update the coding agent skill and instructions

The packaged `convai-unity-sdk` skill (version `1.2.0`), the Setup guidance and the managed agent instruction blocks now let a coding agent enter and exit Play Mode, save the scenes it changed and bake a NavMesh whenever the task needs it. Before, they told the agent to wait for an explicit request before each of these actions. Explicit user restrictions still apply. A diagnosis-only request may reproduce a problem in Play Mode but does not authorize repairs or gameplay actions. State a restriction explicitly when the agent must not enter Play Mode, save scenes or bake a NavMesh.

A project that installed the skill or the instructions earlier keeps the old rule until you update it.

1. Open **Convai > Convai Editor > AI Coding**.
2. In the **Claude Code** and **ChatGPT / Codex** cards, update **Project skill** for each client you use.
3. For each client, update its instructions separately. The row is **Project instructions** in those two cards, and the client's own row under **Other AI Clients** for Cursor, Gemini or VS Code Copilot. Updating the project skill does not update an existing instruction block.

The MCP tool contract version stays at `11` for this change. See [Install the project skill](../ai-coding-assistant/install-project-skill.md) and [Play Mode, scene saves, and NavMesh bakes](../ai-coding-assistant/README.md#play-mode-scene-saves-and-navmesh-bakes).

## Review action parameters

The SDK now reads more of what a character writes in an action command, which changes what an Action Behavior receives in four cases.

* A String or Auto parameter whose value is a JSON object or array arrives whole, as the character wrote it. Before, it arrived empty.
* Brace groups labelled with the action's slots fill the slots they name, in any order. `{high: 80} {low: 20}` no longer fills the slots by position.
* `move_to {speed: run} Blue Sphere` reads each slot. Before, `speed` got `{speed:` and the target got `run} Blue Sphere`.
* A one-slot action sent with nothing after its name has that parameter marked Missing, not Provided with an empty value. An Action Behavior can now tell no value from a blank one through `ConvaiActionParameterValue.Presence` for one-slot actions too. The template's empty slot (`{}`) still reads as Provided and blank.

## Review runtime action targets

Three fixes change what the SDK sends when you register or remove action targets at runtime.

* A runtime action target that the backend has acknowledged keeps resolving to its scene object, and `character.Actions.UnregisterTarget` removes it from the next action-config sync. Before, the removal failed on a character that sends no `action_config` at connect. Convai Action Target components that stand for characters leave the sync the same way when removed.
* Every flush starts a new batch window, so registering or removing many targets no longer sends a full action config for each change.
* An action-target sync larger than 12 KiB is sent as separate actions, objects and characters updates, each with its own update ID and acknowledgement, instead of one message over the 15 KiB data-message limit, which the SDK refuses to send. Lists are never split into chunks. When one list alone is too large, nothing is sent and a warning names the list; register fewer targets or shorten their descriptions.

See [Register targets and toggle actions from code](../features/character-actions/register-targets-from-code.md).

## If upgrading from before 4.6.1

Remove the ignored reason argument from `DisconnectAsync`. Replace `SetExplicitConversationTarget` with `SetInitialCharacter` for startup selection or `TalkTo` for a live switch. Replace `NarrativeDesignFetcher` with the documented data service, and remove usage of deleted placeholder providers and participant-builder options. Review the historical 4.6.1 entry in [Release notes](release-notes.md) for those earlier changes.

## Verify the migrated application

* [ ] Project scripts compile and saved event listeners accept the new payloads.
* [ ] Transcript rows update once per entry, handle corrections/removals and clear correctly.
* [ ] A character reaches ready state and responds through every input mode the app exposes.
* [ ] Memory identity and failure codes behave correctly for the app's provider.
* [ ] Action Behaviors handle JSON, labelled and Missing parameter values.
* [ ] Action targets registered and removed at runtime take effect, and no Console warning reports an oversized action-target list.
* [ ] Characters with **Auto Connect** on connect at startup only when **Starts Connected** is on, or your code connects them.
* [ ] The project skill (Claude Code and ChatGPT / Codex) and the project instructions are updated for each coding agent client you use.
* [ ] Mic denial, text-only operation, reconnect and background recovery work on target devices.
* [ ] Browser publishing, audio unlock and lip-sync timing pass in the deployed hosting environment.

These are application checks to run after migration. They do not report validation already completed for your project.
