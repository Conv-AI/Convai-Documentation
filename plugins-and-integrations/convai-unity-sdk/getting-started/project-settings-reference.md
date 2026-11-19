---
title: Project Settings reference
description: >-
  Find project-wide Convai credentials, runtime defaults, logging controls,
  and advanced settings, and see when changes take effect.
last_reviewed: "5.0.0-pre.1"
---

Open **Convai > Settings** or **Edit > Project Settings > Convai SDK** to edit project-wide SDK settings. Both commands open the same Project Settings panel. Edit character, room, and input settings on their scene components or prefabs.

## Settings sections

| Section | Purpose | Important controls |
| --- | --- | --- |
| Credentials | Select authentication and service configuration. | Auth Mode, API Key, token endpoint fields, Environment and [Character Workspace ID](#character-workspace-id). |
| Runtime Defaults | Seed runtime preferences. | Transcript System, Notification System, Player Display Name, Microphone and Background Policy. |
| Diagnostics | Control SDK logging. | Verbose, Default, Errors Only, Global Log Level, Stack Trace Levels, Colored Console Output and category overrides. |
| Connection & Scripting Defines | Set the connection timeout and enable optional build features. | Connection Timeout (s) and Scripting Define Symbols for the active build target group. |

<figure><img src="../../../.gitbook/assets/unity-project-settings-sections.png" alt="The Credentials and Runtime Defaults cards on the Convai SDK Project Settings page."><figcaption><p>(1) Choose how players authenticate in <strong>Credentials</strong>. (2) Change startup behavior in <strong>Runtime Defaults</strong>.</p></figcaption></figure>

<figure><img src="../../../.gitbook/assets/unity-project-settings-diagnostics-connection.png" alt="The Diagnostics card shows logging presets. The Connection and Scripting Defines card shows the connection timeout."><figcaption><p>(1) Choose a logging preset in <strong>Diagnostics</strong>. (2) Find the timeout and scripting options under <strong>Connection &amp; Scripting Defines</strong>.</p></figcaption></figure>



Open **Convai > Home > Welcome** to review **Setup Health**. It checks the local settings asset, credentials, and platform microphone configuration. After resolving any findings, validate the scene and try a connection. For an illustrated walkthrough, see [Configure microphone](configure-microphone.md#macos-and-ios). Check the displayed SDK and Unity versions under **Convai > Home > Help**.

## Credentials and service selection

**Api Key** is the rendered enum label for API-key authentication. **Auth Token** exposes **Token Endpoint URL**, **HTTP Method**, **Token Response Field** and **Request Headers**. Use [Configure API key](configure-api-key.md) for local development and [Authentication](../authentication/README.md) for production token setup.

**Environment** selects the service environment. **Custom** exposes **Realtime Server URL**, **REST Base URL**, and **Character API Base URL** overrides. Change these only for an environment you intend to target. [REST API routing](../advanced-topics/choose-a-rest-api-mode.md) describes how each service selects its host.

Changing credentials or endpoints does not rotate authentication inside an established room. Reconnect to use new connection credentials.

## Character Workspace ID

**Character Workspace ID** names the Convai workspace that the SDK reads character and narrative data from. Leave it empty. On Convai's hosted service, each API key belongs to one workspace and reads only that workspace, so the field cannot widen what a key can see.

Every Convai account has a Personal Workspace. A Shared Workspace holds a team's characters and can have its own API key, which belongs to the workspace rather than to one person.

### Requests that use it

The SDK adds the workspace to these reads only:

| Read | Where it happens |
| --- | --- |
| Character details | **Fetch** next to the character name in the character Inspector |
| Narrative Design sections and triggers | The narrative design components, in the Editor and at runtime |
| Character list | The character picker in the Scene Auto Tagger |

Room connections do not send it, so it never changes which character a conversation reaches. It also has no effect on the released character versions list, Long-Term Memory, or other account requests.

### Read a team's characters

With the field empty, Convai reads the workspace that the API key in **Credentials** belongs to:

| API key in Credentials | Workspace the SDK reads |
| --- | --- |
| Your personal API key | Your Personal Workspace |
| A Shared Workspace's API key | That Shared Workspace |

To work with a team's characters, enter that Shared Workspace's API key in **Credentials**. The workspace owner manages the key.

### When to enter an ID

An ID that names a different workspace from the key's makes the Character API refuse the read. An ID that matches the key's workspace changes nothing. Some on-premises Convai deployments let a personal API key read every workspace its account is a member of. Only there does an ID select a different workspace: enter that workspace's UUID. Spaces around it are ignored.

## Runtime defaults

| Setting | Default | Scope |
| --- | --- | --- |
| Transcript System | On | Enables transcript presentation by default; runtime preferences can override it. |
| Notification System | Off | Enables session-state and error notifications. |
| Player Display Name | Player | Default display name, distinct from local Player ID and end-user identity. |
| Microphone | System Default | Default device choice; **Refresh** enumerates connected devices again. |
| Background Policy | PauseTimeline | How local presentation behaves when the application is backgrounded. |

These values initialize the runtime settings service. A runtime settings UI or script can override them. For effective character volume, use [Configure character audio](configure-character-audio.md); for capture policy, use the room's **Allow Microphone** setting.

## Diagnostics and advanced settings

Logging presets replace category overrides. Use a narrow log level when investigating a problem, and review logs for sensitive values before sharing them.

**Connection Timeout (s)** has a UI range of 5–120 seconds and a default of 30. It is not a replacement for every transport-specific timeout. Changing a scripting define symbol for the active build target group triggers script recompilation. The Editor asks for confirmation before applying the change.

Each section's reset applies to that section. Resetting **Connection & Scripting Defines** also removes the Convai scripting define symbols for the active build target group. Review the confirmation dialog before resetting.
