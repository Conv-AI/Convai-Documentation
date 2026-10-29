---
title: Custom persistence provider
description: Migrate retired persistence-provider examples and understand which local stores the default Unity runtime owns before adding application storage.
last_reviewed: "5.0.0-preview"
---

Remove integrations based on `IPersistenceProvider`, `PersistenceResult`, `PersistenceOptions`, `ConflictResolutionStrategy`, or `ConvaiRuntimeBuilder.UsePersistence`. These APIs are absent from the current SDK, so older examples using them do not compile.

{% hint style="warning" %}
For the SDK version documented here, follow the [current integration guidance](../stored-data.md). The older examples on this URL do not describe the shipped runtime.
{% endhint %}

## Keep application storage separate

The default runtime constructs `PlayerPrefsKeyValueStore` for runtime settings and session identifiers. There is no public builder hook that replaces this store across the default runtime. `IKeyValueStore` still exists, and standalone classes such as `ConvaiRuntimeSettingsStore` and `KeyValueStoreSessionPersistence` accept it in their constructors. Constructing one of those objects does not install it into `ConvaiManager`.

If your application needs cloud saves or encrypted local data, keep that application state in your own storage service. Use the SDK's public identity, settings, and session APIs at the integration boundary. Do not claim that a standalone store redirects SDK writes.

## Review what remains on the device

See [What the SDK stores on the device](../stored-data.md) for current keys and clearing behavior. Clearing local sessions does not erase Convai's server-side conversation or memory records.

{% content-ref url="custom-identity-provider.md" %}
[Custom identity provider](custom-identity-provider.md)
{% endcontent-ref %}
