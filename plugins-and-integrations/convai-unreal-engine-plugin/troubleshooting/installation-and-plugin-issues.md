---
title: Installation and plugin issues
description: Fix plugin-not-found errors, module load failures, Blueprint-only project limitations, and Android packaging errors in the Convai Unreal Engine plugin.
last_reviewed: "4.0.0-beta.21"
---

Use this page to resolve problems that occur during installation or when the plugin fails to load in the Unreal Editor. Issues that appear after the plugin loads — such as API key or audio errors — are covered in the other troubleshooting pages.

## First-line check

Before investigating specific symptoms, run through these three checks. They confirm whether Unreal can discover the plugin and load the runtime module.

{% stepper %}
{% step %}
### Confirm the plugin appears in the Plugins list

Open **Edit > Plugins** and search for `Convai`. The plugin entry must appear and be enabled (checkbox checked). If it does not appear, the folder structure is incorrect — see [Plugin does not appear in the Plugins list](#plugin-does-not-appear-in-the-plugins-list).
{% endstep %}

{% step %}
### Check the Output Log for LogConvai entries

Open **Window > Output Log** and type `LogConvai` in the search field. A failed native library load appears as `Failed to load %s from %s`. If no Convai log categories appear, Unreal may not have discovered the plugin.
{% endstep %}

{% step %}
### Verify the plugin folder structure

For a project-level install, the plugin root must be at `<YourProject>/Plugins/Convai/` and must contain `ConvAI.uplugin`. For an engine-level install, the plugin root is under the engine's `Engine/Plugins/Marketplace/Convai/` folder.
{% endstep %}
{% endstepper %}

## Plugin does not appear in the Plugins list

**Symptom:** After copying the plugin folder into the project or engine, the Convai entry does not appear under **Edit > Plugins**.

**Cause — incorrect installation location or folder structure:** The extracted folder does not contain `ConvAI.uplugin` at the plugin root, or the folder was placed in a location Unreal does not scan.

**Fix:** Move the extracted plugin folder to one supported location, then restart the Unreal Editor:

| Install type | Folder |
| --- | --- |
| Project-level install | `<YourProject>/Plugins/Convai/` |
| Engine-level install | `<UnrealEngine>/Engine/Plugins/Marketplace/Convai/` |

The selected folder must contain `ConvAI.uplugin` at its root.

**Verify:** Open **Edit > Plugins**, search for `Convai`, and confirm the entry appears. Enable it if it is not already enabled, then restart the editor when prompted.

---

**Cause — Fab or Marketplace install not propagated:** When the plugin was acquired through [Fab](https://www.fab.com/listings/ba3145af-d2ef-434a-8bc3-f3fa1dfe7d5c), the Epic Games Launcher must install it to the engine before the editor can detect it.

**Fix:** Open the Epic Games Launcher, go to your Library, locate the Convai plugin entry, and click **Install to Engine** for the engine version you are using.

**Verify:** Relaunch the Unreal Editor. The plugin should appear in **Edit > Plugins** under the **Runtime** category.

## Plugin enabled but editor does not restart cleanly

**Symptom:** You enable the Convai plugin and click **Restart Now**, but the editor crashes or shows a compile dialog on restart.

**Cause — C++ project requires a recompile:** Unreal Engine may recompile project code when a source plugin is added at the project level. If compilation fails, the editor will not start.

**Fix:** Open the project in Visual Studio (or your configured IDE), select **Build > Build Solution**, resolve any compile errors, then launch the editor again.

**Verify:** The editor opens without a compile dialog, and the Convai components appear in the **Add Component** menu when editing a Blueprint.

## Blueprint-only project cannot load the plugin

**Symptom:** The plugin is installed correctly but the editor crashes on restart, or shows a dialog saying it cannot compile modules. You are using a Blueprint-only project with no C++ source files.

**Cause:** A project-level source plugin can require Unreal Build Tool to compile modules such as `Convai`, `ConvaiEditor`, and `ConvaiVisionBase`. Blueprint-only projects have no generated C++ target, so Unreal cannot compile a project-level source plugin.

{% hint style="warning" %}
Blueprint-only projects should use the Fab or engine-level install path for the Convai plugin. Use project-level installation when the project has a C++ build target.
{% endhint %}

**Fix — option A (recommended): Convert to a C++ project**

In the Unreal Editor, select **File > New C++ Class**, accept the default `None` parent class and the default file name, and click **Create Class**. This generates the project files and sets up the build environment. After the IDE opens, build the solution, then relaunch the editor.

**Fix — option B: Engine-level installation**

Install the plugin into the engine directory instead of the project directory. Place the plugin folder at:

```text
C:\Program Files\Epic Games\UE_5.x\Engine\Plugins\Marketplace\Convai\
```

Replace `5.x` with your engine version. The engine already has a build environment, so engine-level plugins do not require a per-project compile step.

**Verify:** The editor restarts cleanly after the build completes. Convai components appear in the **Add Component** menu.

## `ConvaiEditor` module not available

**Symptom:** On Unreal Engine 5.1 or earlier, the Convai editor window does not appear. The Output Log shows `ConvaiEditor: Editor UI disabled - requires UE 5.2 or later`.

**Cause:** The `ConvaiEditor` module requires a property-binding editor feature that is not available in UE 5.1 and earlier. The module is intentionally disabled on those engine versions.

**Fix:** Upgrade to Unreal Engine 5.2 or later to use the Convai editor window. On UE 5.1 and earlier, configure the API key manually by setting `API_Key` in `Config/DefaultEngine.ini` under the `[/Script/Convai.ConvaiSettings]` section.

**Verify:** After setting the key in the config file, open **Edit > Project Settings > Plugins > Convai** and confirm the `API Key` field shows the value you set.

Plugin version <code class="expression">space.vars.unreal_plugin_version</code> supports all Unreal Engine 5.x versions from 5.0 onward; `ConvaiEditor` is the only component that requires 5.2 or later.

## `AudioCapture` plugin dependency missing

**Symptom:** The editor shows an error referencing a missing `AudioCapture` module, or the plugin fails to load with a dependency error.

**Cause:** The `AudioCapture` engine plugin is a required dependency. It may be disabled in the project's plugin configuration.

**Fix:** Open **Edit > Plugins**, search for `Audio Capture`, and enable it. Restart the editor.

**Verify:** The Convai plugin loads without errors. Check the Output Log for `LogConvai` messages at startup — there should be no missing-module errors.

## Plugin loads on Windows but not on Android

**Symptom:** The plugin works in the Windows editor and in Windows packaged builds, but fails to load or causes errors when packaging for an Android target.

**Cause — missing Android SDK or NDK configuration:** A packaging failure can occur when the Android NDK or SDK path is not configured, or when the `AndroidPermission` plugin dependency is disabled in the project.

**Fix:**
1. Confirm that the Android NDK and SDK paths are set in **Edit > Project Settings > Platforms > Android SDK**.
2. Open **Edit > Plugins**, search for `Android Permission`, and enable it.
3. Rebuild the project for the Android target.

**Verify:** The packaging log completes without module-not-found errors for `Convai` or `ConvaiVisionBase`.

---

**Cause — missing native libraries in the APK:** The plugin's Android APL copies `libconvai_client.so`, `libconvai_http_helper.so`, and `libwebrtc.jar` into the Android build. If a custom packaging step removes these files, the real-time connection can fail on-device.

**Fix:** This is handled automatically by the plugin's `Convai_AndroidAPL.xml`. If you are seeing native-load failures, confirm that:
1. The plugin's `Convai_AndroidAPL.xml` file is present at `Plugins/Convai/Source/Convai/` and has not been removed or modified.
2. Your ProGuard or R8 configuration does not override the keep rules inserted by the plugin. The APL includes rules for WebRTC JNI classes and native methods:

```proguard
-keepattributes Signature
-dontskipnonpubliclibraryclassmembers
-keep class **.jni_zero.** { *; }
-keep class **.webrtc.** { *; }
-keepclasseswithmembernames class * {
    native <methods>;
}
```

**Verify:** Run `adb shell ls /data/app/<your.package.name>/lib/arm64/` after installing the APK. You should see `libconvai_client.so` and `libconvai_http_helper.so` listed.

{% hint style="danger" %}
Deleting the `Intermediate/` and `Binaries/` folders forces a full recompile and can resolve corrupted build state — but only do this as a last resort. Close the editor and IDE before deleting these folders, as open file handles can cause the delete to fail or leave the project in a partially cleaned state. Rebuild from the IDE before relaunching the editor.
{% endhint %}

## Next steps

{% content-ref url="connection-and-api-key-issues.md" %}
[Connection and API key issues](connection-and-api-key-issues.md)
{% endcontent-ref %}

{% content-ref url="diagnostics-and-log-export.md" %}
[Diagnostics and log export](diagnostics-and-log-export.md)
{% endcontent-ref %}
