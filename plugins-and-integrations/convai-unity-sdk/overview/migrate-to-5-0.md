---
title: Migrate to SDK 5.0
description: >-
  Update an existing Unity integration for the 5.0 transcript API, player
  identity, microphone policy, native audio libraries, and platform changes.
last_reviewed: "5.0.0-preview"
---

The 5.0 preview changes transcript APIs, local player identity, media behavior and how action parameters are read. Upgrade a copy of your integration, resolve compile errors and verify saved scene bindings before replacing a deployed build.

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

## Review browser and Editor behavior

**WebGL Vision:** Frame Source is now the default publication policy. Game View is explicit, and a missing source can still fall back to the visible canvas. Check that no unintended UI is sent. Browser volume and mute now use `ConvaiAudioOutput`; spatial rolloff remains unavailable.

**Build target:** Activate WebGL before a WebGL build. The build guard rejects a mismatched active target.

**Editor tools:** `Convai.ConfigureRoom` keeps fields you omit. Pass an explicit value when you want a reset. Tool results redact player identity and shorten session IDs; do not parse those fields as complete identifiers. The memory tools introduce remote service writes that preview by default. Five Scene Auto Tagger tools are new: `Convai.FindSceneTagCandidates`, `Convai.TagSceneObjects`, `Convai.GetSceneTagRun`, `Convai.ApplySceneTags` and `Convai.DescribeSceneView`. Tagging uploads captures, so the assistant skill runs it only when asked, and apply previews by default. The MCP tool contract version is now `11`; a client that checks it should expect that value.

**Scene context:** Spatial facts use banded distances and a per-character object cap, and are published only while the character is in conversation. A fact now names the character it is measured from. It reads `Chair: 3 m to Ava's left; visible to Ava; stationary` where it read `Chair: 3.0 m ahead`, so update applications that parse spatial fact text. A logical group's fact describes its nearest member and reads `Name (nearest of N): …`. Attention references must exist in the action configuration: give an object an action target, or list it in the action config, if it should receive attention. Every world object, action targets included, now goes in the scene description, and a new room for a scene with one character receives that description in its connect request. Scenes with more than one character, and rejoins, still send it as a data message limited to 15,360 bytes.

## Review action parameters

The SDK now reads more of what a character writes in an action command, which changes what an Action Behavior receives in four cases.

* A String or Auto parameter whose value is a JSON object or array arrives whole, as the character wrote it. Before, it arrived empty.
* Brace groups labelled with the action's slots fill the slots they name, in any order. `{high: 80} {low: 20}` no longer fills the slots by position.
* `move_to {speed: run} Blue Sphere` reads each slot. Before, `speed` got `{speed:` and the target got `run} Blue Sphere`.
* A one-slot action sent with nothing after its name has that parameter marked Missing, not Provided with an empty value. An Action Behavior can now tell no value from a blank one through `ConvaiActionParameterValue.Presence` for one-slot actions too. The template's empty slot (`{}`) still reads as Provided and blank.

## If upgrading from before 4.6.1

Remove the ignored reason argument from `DisconnectAsync`. Replace `SetExplicitConversationTarget` with `SetInitialCharacter` for startup selection or `TalkTo` for a live switch. Replace `NarrativeDesignFetcher` with the documented data service, and remove usage of deleted placeholder providers and participant-builder options. Review the historical 4.6.1 entry in [Release notes](release-notes.md) for those earlier changes.

## Verify the migrated application

* [ ] Project scripts compile and saved event listeners accept the new payloads.
* [ ] Transcript rows update once per entry, handle corrections/removals and clear correctly.
* [ ] A character reaches ready state and responds through every input mode the app exposes.
* [ ] Memory identity and failure codes behave correctly for the app's provider.
* [ ] Action Behaviors handle JSON, labelled and Missing parameter values.
* [ ] Mic denial, text-only operation, reconnect and background recovery work on target devices.
* [ ] Browser publishing, audio unlock and lip-sync timing pass in the deployed hosting environment.

These are application checks to run after migration. They do not report validation already completed for your project.
