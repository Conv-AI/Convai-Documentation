---
title: Ship a secure build
description: Build a Convai Unity SDK player in Auth Token mode so the account API key never reaches the shipped build, and meet WebGL CORS requirements.
last_reviewed: "5.0.0-preview"
---

Produce a player build that does not contain the Convai account API key, and configure a token endpoint that a WebGL build can actually reach. Use this page after [Configure Auth Token mode](configure-auth-token-mode.md), immediately before you build.

## What the build processor does

`ConvaiApiKeyStripBuildProcessor` runs before every build. If **Auth Mode** is **Auth Token**, it zeroes both the `_apiKey` and `_apiKeyObfuscated` fields on the project's `ConvaiSettings` asset for the duration of the build, then restores the saved key afterward. If **Auth Mode** is **Api Key**, the processor does nothing — the account key is included in the build as usual.

The strip only ever touches `ConvaiSettings` while a build is running. It writes a backup to `Library/Convai/AuthTokenBuildCredentialBackup.json` before stripping, so the key survives an Editor crash or a killed build process, and restores automatically:

- after the build finishes (`OnPostprocessBuild`),
- if the build is interrupted or canceled (`EditorApplication.update`),
- before the Editor quits with a pending backup (`EditorApplication.quitting`),
- at the start of the next build if a backup remains.

{% hint style="warning" %}
The backup contains your account credential. Keep it private and do not paste it into logs or support requests. The settings key is restored after the build; do not depend on it while stripping is active.
{% endhint %}

## Resolve a stopped build

If the processor cannot guarantee the key is absent, it stops the build with `BuildFailedException` instead of shipping an unstripped key. You may hit one of these exact messages:

| Console message | Cause |
|---|---|
| `Convai could not restore credentials left by an earlier interrupted build. The new build was stopped to avoid losing the saved API key.` | A previous build left a pending backup that never restored. Let the Editor idle so its update hook can restore the key, or restart it. If restoration still fails, inspect the private backup locally and the restore error before building again. |
| `Convai Auth Token mode requires a saved ConvaiSettings asset before building.` | The project has no saved `ConvaiSettings` asset. Open **Convai > Settings** once so the SDK creates it. |
| `Convai Auth Token mode requires the ConvaiSettings asset to live in this project, not inside a package — stripping the key from a package asset would not be saved the way the build depends on.` | The settings asset resolved to a package path instead of a project path. Move or recreate the asset inside the project. |
| `Convai could not locate the serialized API-key fields. The build was stopped because Auth Token mode cannot guarantee that the account key is absent.` | The `ConvaiSettings` asset's serialized layout does not match what the processor expects, typically after a custom modification to the asset. Restore the asset from a known-good copy. |

Other failures begin with `Convai failed to remove the stored API key before building:`, `Convai could not persist the API-key safety backup before building:`, or `Convai could not restore the API key`. Resolve the reported file or serialization problem without sharing the backup.

The SDK also stops a build that crosses the WebGL/non-WebGL boundary without switching the Editor's active build target. The message begins `Convai stopped this`; switch the active target and rebuild. Key stripping is skipped for that rejected build.

When stripping succeeds, the Console logs `[Convai] Temporarily removed the stored API key for this Auth Token player build. It will be restored in Project Settings when the build finishes.`, and after the build restores it, `[Convai] Restored the Project Settings API key after the player build.`

## The stored key is obfuscated, not encrypted

`ConvaiApiKeyObfuscation` applies an XOR cipher against a fixed key string, then Base64-encodes the result with a `cnv1:` prefix. This keeps the API key from being trivially greppable in the serialized asset and in version control diffs — it is not encryption. Anyone with the SDK source can reverse it, and any key shipped inside a client build is ultimately extractable.

{% hint style="danger" %}
Do not treat obfuscation as security. If you ship an API Key mode build to an audience you do not fully control, the account key can be recovered from that build. Ship in Auth Token mode for any build that leaves your own machine.
{% endhint %}

## Meet WebGL CORS requirements

A WebGL build reaches your token endpoint from the browser, so the endpoint needs more than HTTPS. Confirm your backend does all of the following before distributing a WebGL build in Auth Token mode:

- Uses HTTPS. The SDK rejects any endpoint that is not HTTPS or an HTTP loopback address, and a browser blocks a mixed-content request from an HTTPS page regardless.
- Allows the deployed game's exact origin through CORS — not a wildcard origin, when the request carries credentials or cookies.
- Allows every header configured in **Request Headers**, and any headers your custom provider sends, including `Content-Type` where needed.
- Responds to CORS preflight (`OPTIONS`) requests.

If your login system uses cookies instead of a bearer token, also configure `Secure`, `HttpOnly`, and an appropriate `SameSite` value, add CSRF protection, and verify how the browser actually sends credentials from Unity WebGL before you rely on it.

Native and WebGL builds send the resolved token with the same header, `API-AUTH-TOKEN` — there is no WebGL-specific header. The CORS requirements above exist because a browser enforces them for the outbound request to your endpoint; a native build has no such restriction.

## Verify the build shipped clean

After producing an Auth Token mode build, confirm the account API key is not present:

1. Check the Console during the build for `[Convai] Temporarily removed the stored API key for this Auth Token player build.` An absent line may mean no key was saved, or that the build used **Api Key** mode. Inspect the selected mode and saved-key state instead of treating the log's absence as proof.
2. After the build finishes, confirm `[Convai] Restored the Project Settings API key after the player build.` appears, if a key was stripped. The key field is hidden in Auth Token mode; temporarily selecting **Api Key** lets you inspect its saved state.
3. Run the built player and confirm a character connects successfully. A successful connection confirms your registered provider or configured endpoint supplied a valid token at runtime.

## Next steps

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>Troubleshoot authentication</strong><br>Console messages and error codes for both authentication modes.</td><td><a href="troubleshooting.md">troubleshooting.md</a></td></tr><tr><td><strong>Configure Auth Token mode</strong><br>Switch to Auth Token mode and configure the token endpoint in Project Settings.</td><td><a href="configure-auth-token-mode.md">configure-auth-token-mode.md</a></td></tr></tbody></table>
