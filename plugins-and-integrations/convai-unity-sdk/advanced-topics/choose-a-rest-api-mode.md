---
title: Migrate from the REST API mode setting
description: Migrate character and narrative requests to the Character API and choose the Unity client that owns each REST operation after upgrading.
last_reviewed: "5.0.0-pre.1"
---

Character details and narrative reads use the Character API. The SDK selects the route for each task.

{% hint style="warning" %}
SDK 5.0 removes the **API Mode** setting. Replace code that selects `ConvaiApiMode.Legacy` or `Upgraded` with the client that owns the task.
{% endhint %}

## Update project settings

Open **Convai > Settings** or **Edit > Project Settings > Convai SDK**. In **Credentials**, use **Environment** to select the host preset, or configure your custom host settings. **Character Workspace ID** supplies workspace context for Character API reads. **Auth Mode** controls credentials for room connections.

Keep a selected Live or pinned character reference when reading a specific version. See [Pin a character version](../getting-started/pin-a-character-version.md).

## Select the client in code

| Task | Client |
| --- | --- |
| Read a character, its sections, or its triggers | `ConvaiCharacterNarrativeClient` |
| Edit character resources in trusted tooling | `ConvaiCharacterApiClient` |
| Read account usage or manage end users and memory | `ConvaiPlatformClient` |
| Connect as a scene player | `ConvaiManager.ConnectAsync` |

Use `ConvaiRestOptionsFactory.CreateCharacterReadOptions(characterReference, apiKey, useDraft, preserveSelectedReference)` to apply the project's environment and workspace. A draft read is requested only when the reference is bare and you allow it to change. Use `CreatePlatformOptions` for the project's Platform API settings.

## Verify your migration

Read the intended character and its narrative data. Confirm you are reading the published or pinned character reference you requested. If a read fails, inspect the response from that API.

{% content-ref url="../scripting-reference/rest-api-client.md" %}
[REST API client reference](../scripting-reference/rest-api-client.md)
{% endcontent-ref %}

{% content-ref url="../authentication/README.md" %}
[Authentication](../authentication/README.md)
{% endcontent-ref %}
