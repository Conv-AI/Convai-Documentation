---
title: Choose a REST API mode
description: Select the client routes used for character and narrative reads, preserve a selected character version, and distinguish API routing from authentication.
last_reviewed: "5.0.0-preview"
---

Choose **API Mode** in the **Credentials** card to control character and narrative REST reads. This setting is separate from **Auth Mode**, which selects credentials for room connections.

## Select routes for your reads

{% stepper %}
{% step %}
### Open Credentials

Open **Convai > Settings** or **Edit > Project Settings > Convai SDK**, then scroll to **Credentials**. **Environment** selects Production, Beta, or a configured custom host; it does not establish access to that environment.
{% endstep %}
{% step %}
### Choose the mode

Use **Legacy** for the legacy routes. Use **Upgraded** for the Character API routes used by character details and narrative reads. Qualified character references, including selected versions, require Upgraded mode. **Character Workspace ID** supplies workspace read context where required by your service configuration.
{% endstep %}
{% step %}
### Verify the selected character

Refresh character details and narrative data with the intended character selection. Treat a failed read as an API response to diagnose; selecting Upgraded does not grant access or guarantee an environment's availability.
{% endstep %}
{% endstepper %}

## Preserve settings in scripts

Construct `ConvaiRestClient` with `ConvaiRestOptionsFactory.Create()` so project environment and API mode apply. Use `CreateForCharacterRead(characterReference, apiKey, useDraft, preserveSelectedReference)` for character-aware reads. Editor authoring can request draft data for bare references while preserving a selected Live or pinned reference.

Animation, memory, and room-connect operations continue through their legacy routes. Runtime short-lived auth tokens also retain compatible legacy routes; they are not Character API personal access tokens.

{% content-ref url="../authentication/README.md" %}
[Authentication](../authentication/README.md)
{% endcontent-ref %}
