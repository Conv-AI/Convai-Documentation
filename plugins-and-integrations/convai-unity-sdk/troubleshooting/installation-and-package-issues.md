---
title: Installation and package issues
description: Fix Convai Unity SDK import failures, unsupported Unity versions, missing package dependencies, and bootstrapper startup warnings.
last_reviewed: "4.5.0"
---

Package import and initial configuration problems account for the majority of first-run failures with the Convai Unity SDK. Most produce a clear message in the Unity Console the moment you enter Play Mode — or even before that, as compiler errors. An unsupported Unity version is the single most common root cause and produces no clear message at all, so confirm it first, then work through the Setup Health checks and the remaining first-line checks below.

## First-line check

Work through these steps before diving into specific issues. They cover the most common root causes and take under three minutes.

{% stepper %}
{% step %}
### Confirm the Unity version

Open `Help → About Unity` (Windows) or `Unity → About Unity` (macOS) and read the exact build number. The Convai Unity SDK requires Unity <code class="expression">space.vars.unity_min_version</code> — this is a hard floor on the exact patch, not a rounded version: an earlier `6000.0` patch such as `6000.0.20f1` is refused, and there is no supported configuration on Unity 2023 or earlier. Every `6000.0` through `6000.5` stream is supported once the editor is at or above the minimum patch.

If the editor is older, upgrade before installing the SDK — the package depends on packages that only exist on Unity 6.
{% endstep %}

{% step %}
### Run the Setup Health checks

Go to **Edit → Project Settings → Convai SDK**. The **Setup Health** section opens first and runs a set of project-configuration checks automatically — each item shows a colored status badge, a title, and a message.

The checks include `Settings Asset` (flags a missing `ConvaiSettings.asset`), `API Key` (flags a missing key), `iOS Microphone Usage Description` (flags an empty `Info.plist` description), `Prepare iOS for Recording` (flags the iOS audio session setting used for Convai microphone recording and speaker playback), `Android Microphone Permission` (informational), and a `Define Drift` check for each Convai feature-flag scripting define that differs across build target groups.

Select **Fix** next to any flagged item to apply the automated correction — for example **Create** adds the missing `ConvaiSettings.asset`, and **Sync All** aligns a drifting scripting define across build target groups. Select **Refresh** in the section header to re-run every check after making changes manually.

If every item shows a healthy (green) badge, the project-level setup is correct and the issue lies elsewhere — continue to the next check below.
{% endstep %}

{% step %}
### Open the Unity Console

Press **Ctrl+Shift+C** (Windows) or **Cmd+Shift+C** (Mac) to open the Console. Type `Convai` in the search box to filter messages.

Look for either of these two exact messages — they appear the moment you press Play:

* `Convai Bootstrapper: ConvaiSettings not found! Please configure settings via Edit > Project Settings > Convai SDK.` → The `ConvaiSettings` asset is missing or was not created. The SDK cannot start.
* `Convai Bootstrapper: API key not configured. Please set your API key in Edit > Project Settings > Convai SDK.` → The settings asset exists but the API key field is empty.

If you see compiler errors instead of these runtime messages, the assembly chain is broken — see [Missing or broken assemblies](#missing-or-broken-assemblies) below before entering Play Mode.
{% endstep %}

{% step %}
### Verify the ConvaiSettings asset

In the Project window, navigate to `Assets/Resources/`. Look for a file named `ConvaiSettings`.

This asset must exist at the exact path `Assets/Resources/ConvaiSettings.asset`. The SDK's bootstrapper loads it via `Resources.Load` at startup. If it is anywhere else — including a subfolder of `Resources/` — it will not be found.

If the file is missing, open **Edit → Project Settings → Convai SDK**. Opening the settings window creates the asset automatically if it does not exist.
{% endstep %}

{% step %}
### Confirm the settings window opens

Go to **Edit → Project Settings → Convai SDK**. The window opens with six sections: **Setup Health**, **Credentials**, **Runtime Defaults**, **Diagnostics**, **Advanced**, and **About**.

* If the window is blank or shows no sections, there is a compiler error in the project. Fix all script errors first — the settings provider only renders when all editor scripts compile cleanly.
* If the window opens but the **Credentials** section shows no API key, select **Credentials**, paste your key from the [Convai developer dashboard](https://convai.com/), then select **Validate & Save**.

When everything is configured correctly, pressing Play shows `Convai Bootstrapper: Initialization complete.` in the Console.
{% endstep %}
{% endstepper %}

## Package requirements

| Item | Required value |
| --- | --- |
| **Package name** | <code class="expression">space.vars.sdk_package_id</code> |
| **Version** | <code class="expression">space.vars.unity_sdk_version</code> |
| **Minimum Unity version** | <code class="expression">space.vars.unity_min_version</code> |

### Required dependencies

All six dependencies are pulled in automatically by UPM when you install the Convai SDK package. If any is missing or at the wrong version, assembly compilation fails.

| Dependency | Minimum version | Notes |
| --- | --- | --- |
| `com.unity.nuget.newtonsoft-json` | <code class="expression">space.vars.dep_newtonsoft_json_version</code> | JSON serialization — required by all SDK communication |
| `com.unity.ugui` | <code class="expression">space.vars.dep_ugui_version</code> | UI Toolkit module — required by all UI components |
| `com.unity.inputsystem` | <code class="expression">space.vars.dep_inputsystem_version</code> | New Input System — required by conversation input |
| `com.unity.ai.navigation` | <code class="expression">space.vars.dep_ai_navigation_version</code> | NavMesh authoring package — resolved automatically with the SDK package |
| `com.unity.collections` | <code class="expression">space.vars.dep_collections_version</code> | Native collections — required by the vendored LiveKit transport's audio and video sources |
| `com.unity.modules.xr` | <code class="expression">space.vars.dep_modules_xr_version</code> | Built-in XR input module — required by XR push-to-talk input |

To verify installed versions: **Window → Package Manager → In Project**.

## Missing or broken assemblies

Assembly definition errors prevent the project from entering Play Mode. The Console shows errors like `The type or namespace name 'X' could not be found` before any Convai bootstrapper messages appear.

### Newtonsoft.Json missing

**Error:** `The type or namespace name 'Newtonsoft' could not be found`

**Fix:** Open **Window → Package Manager**. Click **+** → **Add package by name**. Enter `com.unity.nuget.newtonsoft-json` and confirm. Unity installs version <code class="expression">space.vars.dep_newtonsoft_json_version</code> or higher automatically.

**Verify:** Open the Console. Newtonsoft namespace errors are gone and the project compiles cleanly.

### Input System missing

**Error:** `The type or namespace name 'InputSystem' could not be found`

**Fix:** Install `com.unity.inputsystem` version <code class="expression">space.vars.dep_inputsystem_version</code> or higher via Package Manager. After installation, Unity prompts you to switch to the new Input System backend — accept this prompt.

**Verify:** Open the Console. InputSystem namespace errors are gone. Accept the backend switch prompt if Unity shows it.

### Collections missing or downgraded

**Error:** `The type or namespace name 'Collections' does not exist in the namespace 'Unity'`

**Fix:** Install `com.unity.collections` version <code class="expression">space.vars.dep_collections_version</code> or higher via Package Manager. Do not downgrade below this version: SDK `4.4.1` pins `com.unity.collections` to <code class="expression">space.vars.dep_collections_version</code> specifically to avoid a known regression in Collections `2.6.7` that conflicts with the Unity AI Assistant package's `xxHash3`/`Unsafe` compiled code on Unity 6.0 projects.

**Verify:** Open the Console. Unity.Collections namespace errors are gone and the project compiles cleanly.

### XR module missing

**Error:** `The type or namespace name 'XR' does not exist in the namespace 'UnityEngine'`

**Fix:** `com.unity.modules.xr` is a built-in Unity module rather than a registry package. It ships enabled by default; if a project's `Packages/manifest.json` explicitly excludes it, remove the exclusion, or add `com.unity.modules.xr` at version <code class="expression">space.vars.dep_modules_xr_version</code> to its `dependencies` block directly and let Unity reimport.

**Verify:** Open the Console. UnityEngine.XR namespace errors are gone and the project compiles cleanly.

### AI Navigation missing or fails to resolve

**Symptom:** Package Manager reports the Convai SDK package itself as unresolved, or lists `com.unity.ai.navigation` with a resolution error — the SDK's own compiled code does not reference this package's API directly, so a missing copy does not raise a C# namespace error the way the other dependencies do.

**Fix:** Open **Window → Package Manager**. Click **+** → **Add package by name**. Enter `com.unity.ai.navigation` and confirm.

**Verify:** Package Manager shows `com.unity.ai.navigation` installed and the Convai SDK package resolves without errors.

### Assembly recompile loop

If Unity enters an infinite recompile loop after installing the package, close Unity and delete the `Library/` folder, then reopen the project.

{% hint style="danger" %}
Deleting the `Library/` folder forces Unity to reimport the entire project from scratch. This process can take 5–30 minutes depending on project size. Close Unity completely before deleting the folder. Only do this if all other fixes have failed.
{% endhint %}

**Verify:** Unity completes asset import without entering another recompile loop.

## Troubleshoot installation failures

| Symptom | Likely cause | Fix | Verify |
| --- | --- | --- | --- |
| Unity refuses to open the project, or Package Manager reports an incompatible editor version | Editor is below the Unity <code class="expression">space.vars.unity_min_version</code> floor | Upgrade to Unity <code class="expression">space.vars.unity_min_version</code> or newer — any `6000.0` through `6000.5` build at or above the minimum patch is supported | `Help → About Unity` reports a build at or above the floor |
| Setup Health section shows a **Warning** or **Blocked** item | A required project setting is missing or has drifted — settings asset, API key, iOS microphone usage description, iOS recording preparation, or a scripting define | Open Edit → Project Settings → Convai SDK → Setup Health and select **Fix** next to the item, or correct it manually and select **Refresh** | The item's status badge turns healthy (green) |
| `Convai Bootstrapper: ConvaiSettings not found!` in Console | `ConvaiSettings.asset` missing or deleted | Open Edit → Project Settings → Convai SDK to recreate it automatically | Re-enter Play Mode — `Convai Bootstrapper: Initialization complete.` appears |
| `API key not configured` warning on Play | API key field is empty | Paste key from Convai dashboard into Edit → Project Settings → Convai SDK → Credentials, then select **Validate & Save** | Re-enter Play Mode — the `API key not configured` warning is gone |
| `The type or namespace 'Newtonsoft' could not be found` | Newtonsoft.Json package missing | Install `com.unity.nuget.newtonsoft-json` via Package Manager | Project compiles without Newtonsoft namespace errors |
| `The type or namespace 'InputSystem' could not be found` | Input System package missing or old version | Install `com.unity.inputsystem` <code class="expression">space.vars.dep_inputsystem_version</code>+ | Project compiles without InputSystem namespace errors |
| `The type or namespace 'Collections' does not exist in the namespace 'Unity'` | `com.unity.collections` missing, or downgraded below <code class="expression">space.vars.dep_collections_version</code> | Install `com.unity.collections` <code class="expression">space.vars.dep_collections_version</code>+ via Package Manager; do not downgrade to `2.6.7` | Project compiles without Unity.Collections namespace errors |
| `The type or namespace 'XR' does not exist in the namespace 'UnityEngine'` | `com.unity.modules.xr` excluded from `Packages/manifest.json` | Restore `com.unity.modules.xr` in `Packages/manifest.json` | Project compiles without UnityEngine.XR namespace errors |
| Convai SDK package fails to resolve, or Package Manager flags `com.unity.ai.navigation` | AI Navigation dependency missing | Install `com.unity.ai.navigation` <code class="expression">space.vars.dep_ai_navigation_version</code>+ via Package Manager | Convai SDK package resolves without errors in Package Manager |
| Package not found when adding via UPM name | Scoped registry not configured | Follow the UPM installation guide to add the Convai scoped registry to `manifest.json` | SDK package appears in Package Manager |
| Asset Store import fails with conflict errors | Files from a previous SDK version still present | Remove the old `Assets/Convai/` folder before reimporting | Package imports without conflict errors |
| Project Settings → Convai SDK window is blank | Script compilation errors exist | Fix all CS errors in the Console; the settings UI only renders when editor scripts compile cleanly | Edit → Project Settings → Convai SDK displays all six sections |
| Settings asset exists but window shows no key | Asset is in wrong path | `ConvaiSettings.asset` must be at exactly `Assets/Resources/ConvaiSettings.asset` — no subfolders | Edit → Project Settings → Convai SDK → Credentials shows the API Key field |
| Errors about `UGUI` or `UI/Default` shader | `com.unity.ugui` missing or wrong version | Install `com.unity.ugui` <code class="expression">space.vars.dep_ugui_version</code>+ via Package Manager | Project compiles without UGUI shader errors |
| Sample scene imports correctly but does not run | URP package missing | Sample scenes require URP; install `com.unity.render-pipelines.universal` and assign the URP asset in Project Settings → Graphics | Sample scene enters Play Mode without errors |

## Console log reference

These are the exact messages the SDK bootstrapper emits during initialization. They fire via `[RuntimeInitializeOnLoadMethod(BeforeSceneLoad)]` — before your `Awake` methods run.

| Message | Level | What it means |
| --- | --- | --- |
| `Convai Bootstrapper: Initializing...` | Info | SDK initialization has started |
| `Convai Bootstrapper: ConvaiSettings not found! Please configure settings via Edit > Project Settings > Convai SDK.` | **Error** | `ConvaiSettings.asset` not found at `Assets/Resources/ConvaiSettings.asset` |
| `Convai Bootstrapper: API key not configured. Please set your API key in Edit > Project Settings > Convai SDK.` | Warning | Settings asset found but API key field is empty |
| `Convai Bootstrapper: Initialization complete.` | Info | All settings loaded successfully; SDK is ready |

{% hint style="warning" %}
The `ConvaiSettings not found` error is non-blocking — the SDK logs it and continues. Your scene will load, but any connection attempt will immediately fail with `config.api_key_missing`. Always resolve bootstrapper errors before testing conversations.
{% endhint %}

## Next steps

Once the SDK initializes cleanly and the bootstrapper logs `Convai Bootstrapper: Initialization complete.`, the next issue category to check is connection and API key validation.

{% content-ref url="connection-and-api-issues.md" %}
[Connection and API issues](connection-and-api-issues.md)
{% endcontent-ref %}
