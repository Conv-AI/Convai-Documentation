---
title: Migrate to Unity SDK 4
description: Update an existing Unity project from version 3 of the Convai SDK to version 4, including every rename and required code change.
last_reviewed: "<version you verified against>"
---

<!--
MIGRATION TEMPLATE. Diataxis mode: how-to.

The reader has a working project and is about to break it. Two things matter more than
anything else on this page: they must know what will break BEFORE they start, and every
change must be complete. A migration guide that misses one rename leaves the reader with a
project that no longer compiles and no way to tell what they missed.

Every rename, signature change, and removal must be verified against the source of both
versions. If you cannot confirm the old name, do not guess it — an incorrect "rename X to Y"
sends the reader searching for something that never existed.

Order the steps in the order a reader must perform them, not by subsystem.
Replace all content. No body `#`. Delete this comment before publishing.
-->

<Lead paragraph: which versions this moves between, roughly how much work it is, and whether the
change can be done incrementally or must be completed in one pass.>

## Before you start

- <Back up or branch the project. Say this concretely.>
- <Version and tooling prerequisites, with inline-code values.>
- <Anything that must be resolved before starting, such as an intermediate version.>

{% hint style="warning" %}
<The single most damaging mistake a reader can make here, if there is one. Max two hints.>
{% endhint %}

## What changed

<A short orientation on the shape of the change, so the reader understands what they are doing
rather than applying edits blindly. Two or three sentences.>

## Breaking changes

| Old | New | What to do |
|---|---|---|
| `<old name or signature>` | `<new name or signature>` | <The edit, stated so it can be applied without further reading.> |
| `<removed item>` | — | <What replaces it, or what to do instead.> |

<This table is the page. Make it complete. If an item's replacement is uncertain, mark it and
flag it for a human rather than writing a plausible guess.>

## Migrate the project

1. <Step, in the order it must happen.>
2. <Step.>
3. <Step.>

## Verify the migration

<The observable conditions that confirm the project is fully migrated: it compiles, a specific
feature works, a specific log line appears. Give the reader a way to be sure, not a feeling.>

- <Check, with the expected result.>
- <Check, with the expected result.>

## Troubleshooting

### <Symptom the reader sees after migrating>

**Symptom:** `<exact message>`

**Cause:** <Usually a step missed above. Name which one.>

**Fix:** <What to do.>

## Next steps

{% content-ref url="<related-page>.md" %}
[<Related page title>](<related-page>.md)
{% endcontent-ref %}
