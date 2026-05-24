---
title: Installation and package issues
description: Fix Convai Unity SDK import failures, missing dependencies, assembly errors, and bootstrapper startup warnings with step-by-step remediation.
last_reviewed: "4.2.0"
---

Package import and initial configuration problems account for the majority of first-run failures with the Convai Unity SDK. Most produce a clear message in the Unity Console the moment you enter Play Mode — or even before that, as compiler errors. Work through the first-line checks below before diving into specific issues.

## First-line check

Work through these three steps before diving into specific issues. They cover the most common root causes and take under two minutes.

{% stepper %}
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

Go to **Edit → Project Settings → Convai SDK**. The window should open and show fields including **API Key**, **Server URL**, and **Logging**.

* If the window is blank or shows no fields, there is a compiler error in the project. Fix all script errors first — the settings provider only renders when all editor scripts compile cleanly.
* If the window opens but **API Key** is empty, paste your key from the [Convai developer dashboard](https://convai.com/).

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

All three dependencies are pulled in automatically by UPM when you install the Convai SDK package. If any is missing or at the wrong version, assembly compilation fails.

| Dependency | Minimum version | Notes |
| --- | --- | --- |
| `com.unity.nuget.newtonsoft-json` | <code class="expression">space.vars.dep_newtonsoft_json_version</code> | JSON serialization — required by all SDK communication |
| `com.unity.ugui` | <code class="expression">space.vars.dep_ugui_version</code> | UI Toolkit module — required by all UI components |
| `com.unity.inputsystem` | <code class="expression">space.vars.dep_inputsystem_version</code> | New Input System — required by conversation input |

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

### Assembly recompile loop

If Unity enters an infinite recompile loop after installing the package, close Unity and delete the `Library/` folder, then reopen the project.

{% hint style="danger" %}
Deleting the `Library/` folder forces Unity to reimport the entire project from scratch. This process can take 5–30 minutes depending on project size. Close Unity completely before deleting the folder. Only do this if all other fixes have failed.
{% endhint %}

**Verify:** Unity completes asset import without entering another recompile loop.

## Troubleshoot installation failures

| Symptom | Likely cause | Fix | Verify |
| --- | --- | --- | --- |
| `Convai Bootstrapper: ConvaiSettings not found!` in Console | `ConvaiSettings.asset` missing or deleted | Open Edit → Project Settings → Convai SDK to recreate it automatically | Re-enter Play Mode — `Convai Bootstrapper: Initialization complete.` appears |
| `API key not configured` warning on Play | API key field is empty | Paste key from Convai dashboard into Edit → Project Settings → Convai SDK | Re-enter Play Mode — the `API key not configured` warning is gone |
| `The type or namespace 'Newtonsoft' could not be found` | Newtonsoft.Json package missing | Install `com.unity.nuget.newtonsoft-json` via Package Manager | Project compiles without Newtonsoft namespace errors |
| `The type or namespace 'InputSystem' could not be found` | Input System package missing or old version | Install `com.unity.inputsystem` <code class="expression">space.vars.dep_inputsystem_version</code>+ | Project compiles without InputSystem namespace errors |
| Package not found when adding via UPM name | Scoped registry not configured | Follow the UPM installation guide to add the Convai scoped registry to `manifest.json` | SDK package appears in Package Manager |
| Asset Store import fails with conflict errors | Files from a previous SDK version still present | Remove the old `Assets/Convai/` folder before reimporting | Package imports without conflict errors |
| Project Settings → Convai SDK window is blank | Script compilation errors exist | Fix all CS errors in the Console; the settings UI only renders when editor scripts compile cleanly | Edit → Project Settings → Convai SDK displays all fields |
| Settings asset exists but window shows no key | Asset is in wrong path | `ConvaiSettings.asset` must be at exactly `Assets/Resources/ConvaiSettings.asset` — no subfolders | Edit → Project Settings → Convai SDK shows the API Key field |
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
