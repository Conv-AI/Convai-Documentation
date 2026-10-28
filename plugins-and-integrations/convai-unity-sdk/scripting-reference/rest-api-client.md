---
title: REST API client reference
description: Reference REST client services, routing options, credentials, and transport ownership for trusted tools and runtime Unity integrations.
last_reviewed: "5.0.0-preview"
---

`ConvaiRestClient` in `Convai.RestAPI` groups REST services used by SDK tooling and runtime integrations. It is separate from the real-time room connection. A public client method describes the request it can make; it does not guarantee account access or a deployed backend feature.

## Services

| Property | Purpose |
| --- | --- |
| `Characters` | Obsolete compatibility service for character data; use `ConvaiCharacterApiClient` |
| `Users` | Account operations |
| `EndUsers` | End-user identity operations |
| `Memory` | Long-Term Memory operations |
| `Narrative` | Obsolete compatibility service; use `ConvaiCharacterApiClient` for authoring and `ConvaiCharacterNarrativeClient` for runtime |
| `Animations` | Animation data |
| `Rooms` | Room connection requests |
| `Options` | Client configuration |

`DownloadFileAsync` accepts a URL string or URI and cancellation token. Dispose a client you create when its owner is finished. Do not dispose a shared SDK-owned client.

## Options and routing

`ConvaiRestClientOptions` accepts a credential in its constructor and exposes `AuthenticationMode`, `Environment`, `DefaultTimeout`, `CustomTransport`, `CharacterApiV2`, `CoreBaseUrl`, `PlatformBaseUrl`, `ProductionBaseUrl`, `BetaBaseUrl`, `InvocationSource`, and `ClientVersion`. `DefaultTimeout` is 30 seconds and the default environment is Production.

`CharacterApiV2` supplies upgraded Character API routing. Core room connection and Platform operations use their own clients and bases; an upgraded Character API selection does not move every REST operation to one endpoint. See [Choose a REST API mode](../advanced-topics/choose-a-rest-api-mode.md).

## Credential contracts

| Client family | API-key header | Token header |
| --- | --- | --- |
| Core connection | `x-api-key` | `API-AUTH-TOKEN` |
| Legacy Platform | `CONVAI-API-KEY` | `API-AUTH-TOKEN` |
| Character authoring/runtime read | `CONVAI-API-KEY` | `Authorization: Bearer` for its PAT credential kind |

A runtime connection token and a Character API personal access token are different contracts. Runtime Auth Token mode does not imply a Character authoring PAT. Keep developer credentials on trusted tooling/backends; use the runtime authentication flow for distributed applications.

## Lower-level clients

`ConvaiCoreApiClient`, `ConvaiPlatformLegacyClient`, `ConvaiCharacterApiClient`, and `ConvaiCharacterNarrativeClient` expose their own transport/options. The Character API client includes typed resource groups and generic operation execution; some resources may require backend/account capabilities beyond this SDK snapshot.

A separate `ConvaiInteractionClient` handles the Interaction text contract. Its bearer credential and backend availability should be verified for the deployment. See [Interaction text client](../advanced-topics/interaction-text-client.md) rather than treating it as a replacement for room chat.

## Related pages

- [Authentication](../authentication/README.md)
- [Long-Term Memory scripting reference](../features/long-term-memory/long-term-memory-scripting-reference.md)
- [Narrative Design API reference](../features/narrative-design/scripting-narrative-design.md)
