---
description: >-
  This guide will walk you through the process of installing Convai-powered
  Unity applications on iOS and iPadOS devices.
---

# Building for iOS/iPadOS

## Prerequisites

Before you begin, make sure you have the following:

* Unity 2022.3 or later
* Xcode (latest version recommended)
* Apple Developer account
* Project with Convai's Unity SDK integrated and running properly
* MacBook for building and deploying to iOS/iPadOS

### Step 1: Prepare Your Unity Project

1. Open your Convai-powered Unity project.
2. Ensure you have the latest version of the Convai Unity SDK [imported](../setting-up-unity-plugin.md)[ and setup](../setting-up-unity-plugin.md) into your project.

<figure><img src="../../../.gitbook/assets/image (3).png" alt=""><figcaption><p>Unity project with Convai SDK imported</p></figcaption></figure>

### Step 2: Configure Build Settings

1. In Unity, go to `File` → `Build Settings`.
2. Select `iOS` as the target platform.
3. Click `Switch Platform` if it's not already selected.
4. Check the `Development Build` option for testing purposes.

<figure><img src="../../../.gitbook/assets/image (3) (1).png" alt=""><figcaption><p>Unity Build Settings window with iOS selected and Development Build checked</p></figcaption></figure>



{% hint style="info" %}
If you wish to add a few required files manually, follow step 3. If you want it to be done automatically, jump to step 4
{% endhint %}

### Step 3: Manually add Required Files

#### Add link.xml

1. Create a new file named `link.xml` in your project's `Assets` folder.
2. Add the following content to the file:

```xml
<linker>
  <assembly fullname="UnityEngine">
    <type fullname="UnityEngine.Application" preserve="fields">
      <property name="platform"/>
    </type>
  </assembly>
</linker>
```

<figure><img src="../../../.gitbook/assets/image (4).png" alt=""><figcaption><p>Unity project view showing the link.xml file in the Assets folder</p></figcaption></figure>

This file prevents potential `FileNotFoundException` errors related to the `libgrpc_csharp_ext.x64.dylib` file.

#### Add BuildIos.cs Script

1. Create a new C# script in `Assets/Convai/Scripts` named `iOSBuild.cs`.
2. Add the following content to the script:

```csharp
#if UNITY_EDITOR && UNITY_IOS
using System.IO;
using UnityEditor;
using UnityEditor.Callbacks;
using UnityEditor.iOS.Xcode;
using UnityEngine;

public class iOSBuild : MonoBehaviour
{
    [PostProcessBuild]
    public static void OnPostProcessBuild(BuildTarget target, string path)
    {
        string projectPath = PBXProject.GetPBXProjectPath(path);
        PBXProject project = new PBXProject();
        project.ReadFromString(File.ReadAllText(projectPath));
#if UNITY_2019_3_OR_NEWER
        string targetGuid = project.GetUnityFrameworkTargetGuid();
#else
        string targetGuid = project.TargetGuidByName(PBXProject.GetUnityTargetName());
#endif
        project.AddFrameworkToProject(targetGuid, "libz.tbd", false);
        project.SetBuildProperty(targetGuid, "ENABLE_BITCODE", "NO");
        File.WriteAllText(projectPath, project.WriteToString());
    }
}
#endif
```

### Step 4: Install required gRPC dlls for iOS:

1. Go to Convai -> Custom Package Installer
2. Click on `Install iOS Build Package`
3. Attach the  script `iOSBuild.cs` to any GameObject in your scene.

<figure><img src="../../../.gitbook/assets/image (5).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../../.gitbook/assets/image (10).png" alt=""><figcaption></figcaption></figure>

### Step 5: Build the Xcode Project

1. In Unity, go to `File` → `Build Settings`.
2. Click `Build` and choose a location to save your Xcode project.
3. Wait for Unity to generate the Xcode project.

### Step 6: Configure and Build in Xcode

1. Open the generated Xcode project.
2. In Xcode, select your project in the navigator.
3. Select your target under the "TARGETS" section.
4. Go to the "Signing & Capabilities" tab.
5. Ensure that "Automatically manage signing" is checked.
6. Select your Team from the dropdown (you need an Apple Developer account for this).
7. If needed, change the Bundle Identifier to a unique string.

<figure><img src="../../../.gitbook/assets/image (6).png" alt=""><figcaption><p>Xcode window showing the Signing &#x26; Capabilities tab with Team and Bundle Identifier fields highlighted</p></figcaption></figure>

### Step 7: Build and Run

1. Connect your iOS device to your Mac.
2. In Xcode, select your connected device as the build target.
3. Click the "Play" button or press `Cmd + R` to build and run the app on your device.

<figure><img src="../../../.gitbook/assets/image (8).png" alt=""><figcaption><p>Xcode toolbar showing the connected device selected and the "Play" button highlighted</p></figcaption></figure>

### Troubleshooting

* If you encounter any build errors, ensure all the steps above have been followed correctly.
* Check that your Apple Developer account has the necessary provisioning profiles and certificates.
* If you face any GRPC-related issues, verify that the `libgrpc_csharp_ext.a` and `libgrpc.a` files are correctly placed in the `Assets/Convai/Plugins/gRPC/Grpc.Core/runtime/ios` folder.

<figure><img src="../../../.gitbook/assets/image (9).png" alt=""><figcaption></figcaption></figure>
