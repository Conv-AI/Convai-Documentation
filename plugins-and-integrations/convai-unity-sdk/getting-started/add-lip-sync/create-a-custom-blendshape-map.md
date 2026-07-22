---
title: Create a custom lip sync map
description: >-
  Create a lip sync map that routes incoming blendshape channels to your
  character's mesh, with per-channel weight and clamp tuning.
last_reviewed: "4.4.0"
---

A lip sync map routes source blendshape channels (from the transport stream) to the actual blendshape names on your character's `SkinnedMeshRenderer`. Create a custom map when your rig uses different blendshape names than the bundled passthrough maps expect, or when you need to tune weights for your specific character.

{% hint style="warning" %}
As of SDK 4.4.0, `ConvaiLipSyncMapAsset` no longer exposes `ClearMappings()`, `InitializeWithDefaults()`, or `AutoDetectFromMeshes()` as public runtime methods. These operations now run only from the asset's Inspector — see **Populate mapping entries** below. Existing map assets keep working unchanged; only the ability to call these operations from your own C# code was removed.
{% endhint %}

{% stepper %}
{% step %}
### Create the asset

In the Project window, navigate to the folder where you want to store the map. Right-click and select **Create > Convai > Lip Sync > Lip Sync Map**. Name the asset descriptively — for example, `ConvaiLipSyncMap_MyRig_FromARKit`.
{% endstep %}

{% step %}
### Configure top-level fields

Select the new asset to open it in the Inspector, and expand the **Configuration** section.

| Field                          | Default   | Description                                                                             |
| ------------------------------ | --------- | --------------------------------------------------------------------------------------- |
| **Target Profile ID**          | _(empty)_ | The profile ID this map targets (e.g., `arkit`, `metahuman`, or your custom profile ID) |
| **Description**                | _(empty)_ | Optional designer notes — not used at runtime                                           |
| **Global Multiplier**          | `1.0`     | Scale applied to all output weights before writing (0–3)                                |
| **Global Offset**              | `0.0`     | Offset added to all output weights (-1–1)                                               |
| **Allow Unmapped Passthrough** | `true`    | Channels with no explicit mapping entry are written using their source name directly    |

{% hint style="info" %}
**Allow Unmapped Passthrough** is useful when most of your blendshape names match the source channels — you only need to add entries for the ones that differ. Unmapped channels write directly using their source name.
{% endhint %}
{% endstep %}

{% step %}
### Populate mapping entries

Expand the **Tools** section in the same Inspector to add mapping entries. This section replaces the runtime `ClearMappings()`, `InitializeWithDefaults()`, and `AutoDetectFromMeshes()` calls used in earlier SDK versions — every mapping operation now runs from the Inspector.

**From a mesh:** Add one or more `SkinnedMeshRenderer` references under **Preview Mesh**, then click **Auto-Detect From Mesh** and choose a match mode:

| Match mode                        | Behavior                                                                                                             |
| ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **Exact Match**                    | Requires case-insensitive name equality between the source channel and a mesh blendshape                              |
| **Contains Match (Recommended)**   | Falls back to substring matching when no exact match is found                                                          |
| **Fuzzy Match**                    | Falls back to matching after stripping common rig-tool prefixes (for example `CTRL_expressions_`, `bs_`, `CC_Base_`) when contains matching also fails |

**From mapping text:** Click **Import Mapping File...** to load a mapping file from disk, or **Paste Mapping Text** to import JSON already on the clipboard. Both accept only canonical version-1 mapping JSON — a JSON object with `"version": 1`, a `mappings` array, and the same field names as the asset's serialized entries:

```json
{
  "version": 1,
  "targetProfileId": "arkit",
  "mappings": [
    {
      "sourceBlendshape": "jawOpen",
      "targetNames": ["jaw_open"],
      "multiplier": 1.0
    }
  ]
}
```

Use **Copy Mapping JSON** to export the current asset's mappings in this same format, for example to share a map between assets or check it into version control as text.

**Other mapping actions:** **Initialize Defaults** clears all existing mappings and creates one disabled entry per known source channel for the asset's **Target Profile ID**. **Clear All** removes every mapping entry. **Sort A-Z** reorders entries alphabetically by source channel. **+ Add Entry** adds a single blank entry to hand-edit.

Each entry — however it was added — maps one source channel to one or more target blendshape names, with the following fields:

| Entry field                 | Default        | Description                                                               |
| --------------------------- | -------------- | ------------------------------------------------------------------------- |
| **Source Blendshape**       | _(empty)_      | Name of the channel as it arrives from Convai (e.g., `jawOpen`)           |
| **Target Names**            | _(empty list)_ | Names of the blendshapes on your `SkinnedMeshRenderer` to drive           |
| **Multiplier**              | `1.0`          | Per-entry scale applied before the global multiplier (0–5)                |
| **Offset**                  | `0.0`          | Per-entry offset (-1–1)                                                   |
| **Response Curve**          | `1.0`          | Exponent applied to the incoming value before scaling (0.25–4)            |
| **Enabled**                 | `true`         | Toggle this entry on or off without deleting it                           |
| **Clamp Min Value**         | `0.0`          | Minimum output value (0–1)                                                |
| **Clamp Max Value**         | `1.0`          | Maximum output value (0–1)                                                |
| **Use Override Value**      | `false`        | When enabled, always write **Override Value** instead of the stream value |
| **Override Value**          | `0.0`          | Constant value written when **Use Override Value** is on                  |
| **Ignore Global Modifiers** | `false`        | Skip **Global Multiplier** and **Global Offset** for this entry           |
{% endstep %}

{% step %}
### Assign the map to the component

In the `ConvaiLipSyncComponent` Inspector, drag your new map asset into the **Mapping** field.

Enter Play Mode and speak to the character. All mapped blendshapes animate. Check the Unity Console for any warnings about unresolved blendshape names.
{% endstep %}
{% endstepper %}

## Usage examples

### Example 1: ARKit stream to a custom rig

**Scenario:** A simulation character was rigged by an artist who used snake\_case names (`jaw_open`, `mouth_smile_left`) instead of the ARKit standard camelCase names (`jawOpen`, `mouthSmileLeft`).

**Setup:**

* Create `ConvaiLipSyncMap_CustomRig_FromARKit.asset`
* Target Profile ID: `arkit`
* Allow Unmapped Passthrough: `false` (all names differ)
* Add entries for each blendshape:

| Source blendshape                    | Target names        |
| ------------------------------------ | ------------------- |
| `jawOpen`                            | `jaw_open`          |
| `mouthSmileLeft`                     | `mouth_smile_left`  |
| `mouthSmileRight`                    | `mouth_smile_right` |
| _(continue for all needed channels)_ |                     |

**Expected outcome:** The character's mouth animates correctly despite using different naming conventions than the ARKit standard.

### Example 2: Reducing jaw movement intensity

**Scenario:** An AI receptionist character's jaw opens too wide during speech, which looks unnatural.

**Setup:**

* Duplicate the bundled `ConvaiLipSyncDefaultMap_ARKit.asset` and rename it
* Find the `jawOpen` entry
* Set **Multiplier** to `0.6` and **Clamp Max Value** to `0.7`

**Expected outcome:** The character's jaw opens only 60–70% as much as the raw stream value, resulting in more restrained, naturalistic mouth movement.

## Next steps

With lip sync configured, validate your complete scene setup.

{% content-ref url="../validate-your-setup.md" %}
[Validate your setup](../validate-your-setup.md)
{% endcontent-ref %}
