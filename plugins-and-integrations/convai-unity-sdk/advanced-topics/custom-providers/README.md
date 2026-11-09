---
title: Credentials, identity, and storage
description: Choose current identity and authentication integration points, and replace older credential and persistence examples that no longer apply.
last_reviewed: "5.0.0-preview"
---

Use a custom end-user identity provider when your application has a login system. For runtime credentials, use the [Authentication](../../authentication/README.md) integration points. The default runtime uses local `PlayerPrefs` storage; it does not expose a builder hook for replacing that store.

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Custom identity provider</strong><br>Resolve a stable user ID and optional metadata before connecting.</td><td><a href="custom-identity-provider.md">custom-identity-provider.md</a></td></tr><tr><td><strong>Custom credential provider</strong><br>Migrate credential snapshot examples to Auth Token mode.</td><td><a href="custom-credential-provider.md">custom-credential-provider.md</a></td></tr><tr><td><strong>Custom persistence provider</strong><br>Replace retired persistence-provider examples with supported application storage.</td><td><a href="custom-persistence-provider.md">custom-persistence-provider.md</a></td></tr><tr><td><strong>Personal access token</strong><br>Distinguish Character API tokens from runtime auth tokens.</td><td><a href="personal-access-token.md">personal-access-token.md</a></td></tr></tbody></table>
