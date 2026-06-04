---
title: Installation and plugin issues
description: Fix plugin-not-found errors, module load failures, and engine version conflicts when installing the Convai Unreal Engine plugin.
last_reviewed: 2026-06-04
---

Use this page to resolve problems that occur during installation or when the plugin fails to load in the Unreal Editor. Issues that appear after the plugin loads — such as API key or audio errors — are covered in the other troubleshooting pages.

## Plugin does not appear in the Plugins list

**Symptom:** After copying the plugin folder into the project or engine, the Convai entry does not appear under **Edit > Plugins**.

**Cause — incorrect installation location:** The plugin folder was placed inside the engine `Plugins` directory instead of the project `Plugins` folder, or the folder name was changed from `Convai`.

**Fix:** Move the extracted plugin folder to `<YourProject>/Plugins/Convai/`. The folder must be named `Convai` and must contain `ConvAI.uplugin` at its root. Restart the Unreal Editor.

**Verify:** Open **Edit > Plugins**, search for `Convai`, and confirm the entry appears. Enable it if it is not already enabled, then restart the editor when prompted.

---

**Cause — Fab or Marketplace install not propagated:** When the plugin was acquired through [Fab](https://www.fab.com/listings/ba3145af-d2ef-434a-8bc3-f3fa1dfe7d5c), the Epic Games Launcher must install it to the engine before the editor can detect it.

**Fix:** Open the Epic Games Launcher, go to your Library, locate the Convai plugin entry, and click **Install to Engine** for the engine version you are using.

**Verify:** Relaunch the Unreal Editor. The plugin should appear in **Edit > Plugins** under the **Runtime** category.

## Plugin enabled but editor does not restart cleanly

**Symptom:** You enable the Convai plugin and click **Restart Now**, but the editor crashes or shows a compile dialog on restart.

**Cause — C++ project requires a recompile:** Unreal Engine must recompile project code when a new plugin is added. If compilation fails, the editor will not start.

**Fix:** Open the project in Visual Studio (or your configured IDE), select **Build > Build Solution**, resolve any compile errors, then launch the editor again.

**Verify:** The editor opens without a compile dialog, and the Convai components appear in the **Add Component** menu when editing a Blueprint.

---

**Cause — binary-only project without Build Tools:** The project was created as a Blueprint-only project and has no C++ source, so the Unreal Build Tool cannot recompile it.

**Fix:** In the Unreal Editor (before it crashes), select **File > New C++ Class** to add a minimal C++ file and generate the project files. Then build from the IDE and relaunch.

**Verify:** The editor restarts cleanly after the build completes.

## `ConvaiEditor` module not available

**Symptom:** On Unreal Engine 5.1 or earlier, the Convai editor window does not appear and the log shows a message that the `ConvaiEditor` module is disabled.

**Cause:** The `ConvaiEditor` module requires a property-binding editor feature that is not available in UE 5.1 and earlier. The module is intentionally disabled on those engine versions.

**Fix:** Upgrade to Unreal Engine 5.2 or later to use the Convai editor window. On UE 5.1 and earlier, configure the API key manually by setting `API_Key` in `Config/DefaultEngine.ini` under the `[/Script/Convai.ConvaiSettings]` section.

**Verify:** After setting the key in the config file, open **Edit > Project Settings > Convai** and confirm the `API Key` field shows the value you set.

{% hint style="info" %}
The plugin version <code class="expression">space.vars.unreal_plugin_version</code> supports all Unreal Engine 5.x versions from 5.0 onward. The `ConvaiEditor` module is the only component that requires 5.2 or later.
{% endhint %}

## `AudioCapture` plugin dependency missing

**Symptom:** The editor shows an error referencing a missing `AudioCapture` module, or the plugin fails to load with a dependency error.

**Cause:** The `AudioCapture` engine plugin is a required dependency. It may be disabled in the project's plugin configuration.

**Fix:** Open **Edit > Plugins**, search for `Audio Capture`, and enable it. Restart the editor.

**Verify:** The Convai plugin loads without errors. You can confirm by checking the Output Log for `LogConvai` messages at startup — there should be no missing-module errors.

## Plugin loads on Windows but not on Android

**Symptom:** The plugin works in the Windows editor and in Windows packaged builds, but fails to load or compile for an Android target.

**Cause:** The `Convai` and `ConvaiVisionBase` modules explicitly allow only `Win64` and `Android` in their platform lists. A packaging failure usually means the Android NDK or SDK path is not configured, or the `AndroidPermission` plugin is disabled.

**Fix:**
1. Confirm that the Android NDK and SDK paths are set in **Edit > Project Settings > Platforms > Android SDK**.
2. Open **Edit > Plugins**, search for `Android Permission`, and enable it.
3. Rebuild the project for the Android target.

**Verify:** The packaging log completes without module-not-found errors for `Convai` or `ConvaiVisionBase`.

## Next steps

{% content-ref url="connection-and-api-key-issues.md" %}
[Connection and API key issues](connection-and-api-key-issues.md)
{% endcontent-ref %}

{% content-ref url="diagnostics-and-log-export.md" %}
[Diagnostics and log export](diagnostics-and-log-export.md)
{% endcontent-ref %}
