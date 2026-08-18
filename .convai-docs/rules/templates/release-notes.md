---
title: Unity SDK release notes
description: What changed in each release of the Convai Unity SDK, including breaking changes and the migration steps each release requires.
last_reviewed: "<version you verified against>"
---

<!--
RELEASE NOTES TEMPLATE. Diataxis mode: reference.

EVERY ENTRY MUST BE TRACEABLE TO THE SOURCE. A release note is the single easiest page to
fabricate and the most damaging when wrong, because readers act on it to plan upgrades.

An entry is allowed only if you can point to one of:
  - a commit or pull request in the SDK repository
  - a version bump in the manifest (.uplugin, package.json, package manifest)
  - written release notes from the maintainer

If you cannot, write the placeholder line shown below and flag it for a human. Do not infer a
change from a diff you did not read, and do not pad a release with plausible-sounding fixes.

Newest release first. Do not rewrite published entries — a reader may have linked to one.
Replace all content. No body `#`. Delete this comment before publishing.
-->

<Lead paragraph: what this page tracks and how versions are numbered. Say where the reader
should go for upgrade instructions if a separate migration guide exists.>

## <version> — <YYYY-MM-DD>

<One sentence on what this release is about, if it has a theme. Otherwise go straight to the
sections below. Include only the sections that have entries — do not carry empty headings.>

### Breaking changes

<Lead with these. A reader scanning for whether an upgrade is safe looks here first.>

- **<What changed>.** <What breaks, and what to do instead.> See
  [<migration page title>](<migration-page>.md).

### Added

- <What is new, and what it lets the reader do.>

### Changed

- <What behaves differently now, and how.>

### Fixed

- <What was broken and is now fixed, described from the reader's side rather than the code's.>

### Deprecated

- **<What is deprecated>.** <What replaces it, and when it will be removed if that is decided.>

## <previous version> — <YYYY-MM-DD>

<Same structure.>

<!--
Placeholder for a release whose changes cannot be sourced. Leave it exactly like this and flag
it — the linter treats an unresolved placeholder as publish-blocking:

## <version> — <date>

Release notes pending. Source history was not available when this page was written.
-->
