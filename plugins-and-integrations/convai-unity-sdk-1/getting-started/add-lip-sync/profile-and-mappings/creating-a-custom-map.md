---
description: >-
  Create a ConvaiLipSyncMapAsset to route stream blendshape channels to your
  character's actual SkinnedMeshRenderer blendshape names, with per-channel
  multiplier and clamp tuning.
---

# Creating a Custom Map

### Route Stream Channels to Your Rig's Blendshapes

A lip sync map routes source blendshape channels (from the transport stream) to the actual blendshape names on your character's `SkinnedMeshRenderer`. Create a custom map when your rig uses different blendshape names than the bundled passthrough maps expect, or when you need to tune weights for your specific character.

{% stepper %}
{% step %}
**Create the Asset**

In the Project window, navigate to the folder where you want to store the map. Right-click and select **Create > Convai > Lip Sync Map**. Name the asset descriptively — for example, `ConvaiLipSyncMap_MyRig_FromARKit`.
{% endstep %}

{% step %}
**Configure Top-Level Fields**

Select the new asset to open it in the Inspector.

**Top-Level Fields:**

| Field                          | Default   | Description                                                                             |
| ------------------------------ | --------- | --------------------------------------------------------------------------------------- |
| **Target Profile ID**          | _(empty)_ | The profile ID this map targets (e.g., `arkit`, `metahuman`, or your custom profile ID) |
| **Description**                | _(empty)_ | Optional designer notes — not used at runtime                                           |
| **Global Multiplier**          | `1.0`     | Scale applied to all output weights before writing (0–3)                                |
| **Global Offset**              | `0.0`     | Offset added to all output weights (-1–1)                                               |
| **Allow Unmapped Passthrough** | `true`    | Channels with no explicit mapping entry are written using their source name directly    |

**Mapping Entries:**

Click **+** in the **Mappings** list to add a new entry. Each entry maps one source channel to one or more target blendshape names.

| Entry Field                 | Default        | Description                                                               |
| --------------------------- | -------------- | ------------------------------------------------------------------------- |
| **Source Blendshape**       | _(empty)_      | Name of the channel as it arrives from Convai (e.g., `jawOpen`)           |
| **Target Names**            | _(empty list)_ | Names of the blendshapes on your `SkinnedMeshRenderer` to drive           |
| **Multiplier**              | `1.0`          | Per-entry scale applied before the global multiplier (0–5)                |
| **Offset**                  | `0.0`          | Per-entry offset (-1–1)                                                   |
| **Enabled**                 | `true`         | Toggle this entry on or off without deleting it                           |
| **Clamp Min Value**         | `0.0`          | Minimum output value (0–1)                                                |
| **Clamp Max Value**         | `1.0`          | Maximum output value (0–1)                                                |
| **Use Override Value**      | `false`        | When enabled, always write **Override Value** instead of the stream value |
| **Override Value**          | `0.0`          | Constant value written when **Use Override Value** is on                  |
| **Ignore Global Modifiers** | `false`        | Skip **Global Multiplier** and **Global Offset** for this entry           |

{% hint style="info" %}
**Allow Unmapped Passthrough** is useful when most of your blendshape names match the source channels — you only need to add entries for the ones that differ. Unmapped channels write directly using their source name.
{% endhint %}
{% endstep %}

{% step %}
**Assign the Map to the Component**

In the `ConvaiLipSyncComponent` Inspector, drag your new map asset into the **Mapping** field.

Enter Play Mode and speak to the character. All mapped blendshapes animate. Check the Unity Console for any warnings about unresolved blendshape names.
{% endstep %}
{% endstepper %}

***

### Usage Examples

#### Example 1: ARKit Stream to a Custom Rig

**Scenario:** A simulation character was rigged by an artist who used snake\_case names (`jaw_open`, `mouth_smile_left`) instead of the ARKit standard camelCase names (`jawOpen`, `mouthSmileLeft`).

**Setup:**

* Create `ConvaiLipSyncMap_CustomRig_FromARKit.asset`
* Target Profile ID: `arkit`
* Allow Unmapped Passthrough: `false` (all names differ)
* Add entries for each blendshape:

| Source Blendshape                    | Target Names        |
| ------------------------------------ | ------------------- |
| `jawOpen`                            | `jaw_open`          |
| `mouthSmileLeft`                     | `mouth_smile_left`  |
| `mouthSmileRight`                    | `mouth_smile_right` |
| _(continue for all needed channels)_ |                     |

**Expected outcome:** The character's mouth animates correctly despite using different naming conventions than the ARKit standard.

***

#### Example 2: Reducing Jaw Movement Intensity

**Scenario:** An AI receptionist character's jaw opens too wide during speech, which looks unnatural.

**Setup:**

* Duplicate the bundled `ConvaiLipSyncDefaultMap_ARKit.asset` and rename it
* Find the `jawOpen` entry
* Set **Multiplier** to `0.6` and **Clamp Max Value** to `0.7`

**Expected outcome:** The character's jaw opens only 60–70% as much as the raw stream value, resulting in more restrained, naturalistic mouth movement.

***

### Next Steps

With lip sync configured, validate your complete scene setup.

{% content-ref url="/broken/pages/aa73f8fe7b06d68723814824592577bd33583185" %}
[Broken link](/broken/pages/aa73f8fe7b06d68723814824592577bd33583185)
{% endcontent-ref %}
