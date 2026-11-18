---
title: REST API client reference
description: Reference REST client services, routing options, credentials, and transport ownership for trusted tools and runtime Unity integrations.
last_reviewed: "5.0.0-pre.1"
---

The SDK provides a separate client for each Convai REST API. Scene gameplay uses `ConvaiManager.ConnectAsync` to open a room and `ConvaiPlayer.TrySendTextMessage` to send typed input.

## Clients

| Client | Namespace | Purpose |
| --- | --- | --- |
| `ConvaiCoreApiClient` | `Convai.CoreApi` | Send a typed `RoomConnectionRequest` to `/connect` |
| `ConvaiPlatformClient` | `Convai.PlatformApi` | Validate a key, query usage, and manage end users and memory |
| `ConvaiCharacterApiClient` | `Convai.CharacterApi` | Call generated Character API operations from trusted authoring tooling |
| `ConvaiCharacterNarrativeClient` | `Convai.CharacterApi.Runtime` | Read character details, sections, and triggers |

Each client accepts its own options. Read-only character requests can preserve a version reference and apply a workspace via `ConvaiCharacterApiOptions`. The Core client accepts an explicit connect URI through `ConvaiCoreApiOptions`. For settings-driven Platform and Character requests, use the public helpers in `Convai.Runtime.Configuration.ConvaiRestOptionsFactory`.

## Credential headers

| API | Account API key header | Token header |
| --- | --- | --- |
| Core | `x-api-key` | `API-AUTH-TOKEN` |
| Platform | `CONVAI-API-KEY` | `API-AUTH-TOKEN` |
| Character authoring and runtime reads | `CONVAI-API-KEY` | `Authorization: Bearer` for a Character API personal access token |

Core and Platform use `ConvaiCredential` from `Convai.Api.Transport`. Character API options use `CharacterApiCredentialKind`. Keep account keys and personal access tokens in trusted tooling or on your backend. Use [runtime authentication](../authentication/README.md) for distributed game clients.

## Transport and errors

The clients share `IConvaiApiTransport`. A client disposes a transport it creates. If you supply your own transport, dispose it after its callers finish. Inspect `ConvaiApiException` for error category and HTTP status where supplied.

{% hint style="warning" %}
SDK 5.0 removes the grouped `ConvaiRestClient` facade. Use the client for the route you called previously. For earlier room-less text integrations, see [Migrate from the standalone text client](../advanced-topics/interaction-text-client.md).
{% endhint %}

## Related pages

- [Migrate from the REST API mode setting](../advanced-topics/choose-a-rest-api-mode.md)
- [Long-Term Memory scripting reference](../features/long-term-memory/long-term-memory-scripting-reference.md)
- [Narrative Design scripting reference](../features/narrative-design/scripting-narrative-design.md)
- [Script the Scene Auto Tagger](../features/scene-metadata/scene-auto-tagger-scripting-api.md)
