---
title: Migrate Your Unreal Engine 5.5 Convai Assets to 5.8
description: Migrate an existing Unreal Engine 5.5 Convai asset project to the current supported Unreal Engine version using the Asset Uploader tool.
last_reviewed: "5.8"
hidden: true
---

Migrate an existing Unreal Engine 5.5 Convai asset project to Unreal Engine <code class="expression">space.vars.asset_uploader_unreal_version</code> using the Asset Uploader tool. Use this page after Convai updates its plugins and toolchain for the new engine version. At the end, the project opens in Unreal Engine <code class="expression">space.vars.asset_uploader_unreal_version</code> with the asset updated through the `AssetUploader` editor utility.

## Prerequisites

* An existing Convai asset project created in Unreal Engine 5.5
* The Asset Uploader tool (`ConvaiAssetUploader.exe`)
* Unreal Engine <code class="expression">space.vars.asset_uploader_unreal_version</code> installed

***

## Migrate the project

{% hint style="warning" %}
Run `ConvaiAssetUploader.exe` in the parent directory of your asset project, not inside the project folder itself. For example, if your project is at `C:/ConvaiAsset/Avatar1`, run the tool in `C:/ConvaiAsset/`.
{% endhint %}

{% stepper %}
{% step %}
### Run the Asset Migration Tool

Navigate to the parent directory of your project and run `ConvaiAssetUploader.exe`.
{% endstep %}

{% step %}
### Select the migration option

If the tool detects valid Convai projects, it presents three options:

```text
What do you want to do?
1. Upload a new asset
2. Update and existing asset
3. Migrate an existing asset to 5.8 UE version
Enter your choice (1, 2, or 3):
```

Enter `3` and press Enter.
{% endstep %}

{% step %}
### Select the project to migrate

The tool displays a list of all detected projects. Select the project to migrate to Unreal Engine <code class="expression">space.vars.asset_uploader_unreal_version</code>.
{% endstep %}

{% step %}
### Let the tool prepare the project

The tool creates a copy of the existing project as a backup and downloads all required dependencies.
{% endstep %}

{% step %}
### Finalize the migration in Unreal Engine

Open the newly copied project in Unreal Engine <code class="expression">space.vars.asset_uploader_unreal_version</code>, run the `AssetUploader` editor utility inside the Unreal Engine Editor, and click **Update Asset**.
{% endstep %}
{% endstepper %}

***

## Verify the migration

The migration is complete once the `AssetUploader` editor utility finishes updating the asset in Unreal Engine <code class="expression">space.vars.asset_uploader_unreal_version</code> without errors.

***

## Manual migration steps

<details>
<summary>Migrate the project manually if the automated process encounters an issue</summary>

The automated tool performs the following steps internally. Follow them manually if the automated migration fails.

1. **Back up the project.** Copy the existing asset project to a safe location.
2. **Update modding project components.** Run `ConvaiAssetUploader.exe` to update the necessary plugins and related components.
3. **Switch the Unreal Engine version.** Right-click the `.uproject` file, select **Switch Unreal Engine version...**, and choose <code class="expression">space.vars.asset_uploader_unreal_version</code>.

   {% hint style="warning" %}
   **Screenshot required before publishing:** Capture the **Switch Unreal Engine version...** dialog with Unreal Engine 5.8 selected in the version list. The image must show the exact dialog title and the full list of available engine versions.
   {% endhint %}

   <figure><img src="../../.gitbook/assets/TODO-switch-unreal-engine-version-5-8.png" alt="Switch Unreal Engine version dialog with Unreal Engine 5.8 selected"><figcaption><p>TODO: Replace with a screenshot of the Switch Unreal Engine version dialog with 5.8 selected.</p></figcaption></figure>

4. **Install the cross-compile toolchain.** Download and install the cross-compile toolchain for Unreal Engine <code class="expression">space.vars.asset_uploader_unreal_version</code>. The recommended compiler is <code class="expression">space.vars.asset_uploader_toolchain_compiler_version</code>. Download it from [the Linux cross-compile toolchain for Unreal Engine](https://cdn.unrealengine.com/CrossToolchain_Linux/v26_clang-20.1.8-rockylinux8.exe).
5. **Clean up the project folders.** Delete all folders in the project directory except `Config`, `Content`, `ConvaiEssentials`, `Plugins`, `Source`, and the `.uproject` file.
6. **Open the project in Unreal Engine <code class="expression">space.vars.asset_uploader_unreal_version</code>.** Open the Unreal Engine project using the <code class="expression">space.vars.asset_uploader_unreal_version</code> editor.
7. **Update the asset.** Run the `AssetUploader` editor utility, then click **Update Asset** to complete the migration.

</details>

***

## Next steps

{% content-ref url="README.md" %}
[Asset Uploader](README.md)
{% endcontent-ref %}
