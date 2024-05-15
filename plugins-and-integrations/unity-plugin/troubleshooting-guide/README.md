# Troubleshooting Guide

## Common Issues (FAQ)

### Q. I cannot see the Convai menu.

A. Please check if there are any errors in the console. Unity needs to be able to compile all the scripts to be able to display any custom editor menu options. Resolving all the console errors will fix this issue.&#x20;



### Q. Player Falling and Input Manager Error.

A.  [player-falling-and-input-manager-error.md](player-falling-and-input-manager-error.md "mention")



### Q. There are a lot of errors on my console.

A. Primarily, three issues cause errors in the console that can stem from the Convai Unity Plugin. You can use the links below to fix them quickly.&#x20;

1. [enabled-assembly-validation.md](enabled-assembly-validation.md "mention")
2. [missing-newtonsoft-json.md](missing-newtonsoft-json.md "mention")
3. [missing-animation-rigging.md](missing-animation-rigging.md "mention")



### Q. I am talking to the character, but I cannot see the user transcript and the character does not seem to be coherently responding to what I am saying.

A. This may indicate issues with the microphone. Please ensure that the microphone is connected correctly. You also need to ensure that the applications have permission to access the menu.

[microphone-permission-issues.md](microphone-permission-issues.md "mention")



### Q. My character seems to be saying something and I can see the transcript but I cannot hear the character.

A. If we are using OVR with our models, we might need to enable audio loopback so that the audio can play.&#x20;

[ovr-lipsync-audio-loopback-not-enabled.md](ovr-lipsync-audio-loopback-not-enabled.md "mention")



### Q. The animations for my characters are looking very weird.

A. The animation avatar that we are using might be incompatible with the character mesh. Fixing that can solve the issue.

[default-animations-incompatibility.md](default-animations-incompatibility.md "mention")



### Q. There are two Settings Panel Buttons in Mobile Transcript UI.

A. If you are using Unity 2021, unexpected prefab variant issues may arise. This is because Unity Mobile Transcript UIs are variants of the main transcript UI prefab. With changes in the Prefab system in Unity 2022, it works correctly in Unity 2022. If you are using Unity 2021, you may encounter issues with prefabs. You can remove the redundant Settings Panel Button to address this problem.



### Q: The lipsync is very faint or not visible.

**A:** The animations that we are using may be modifying facial animations. Editing the animations to remove facial animations should fix any issues related to lipsync.

[animations-have-facial-blendshapes.md](animations-have-facial-blendshapes.md "mention")

**A:** The script also needs the avatar to not be mapped to the jaw bone to be manipulate the jaw bones itself.&#x20;

[jaw-bone-in-avatar-is-not-free.md](jaw-bone-in-avatar-is-not-free.md "mention")



### **Q: I'm facing security permission issues using the `grpc_csharp_ext.bundle` DLL inside the Unity Editor on MacOS**

**A:** macOS's strict security measures can block certain external unsigned DLLs. To address this, you can manually allow the DLL in "Security & Privacy" settings, modify Gatekeeper's settings through Terminal, ensure correct file permissions for the DLL, check its settings in Unity, and update the Mac Configuration in Unity's Player Settings

[macos-permission-issues.md](macos-permission-issues.md "mention")



### **Q: I'm not able to talk to my character after building my Unity project for macOS (Intel64+Apple Silicon builds), especially on Intel Macs**

**A:** The issue is rooted in the `grpc_csharp_ext.bundle` used in Unity for networking. This DLL has separate versions optimized for Intel and Apple Silicon architectures. When trying to create a Universal build that serves both, compatibility problems arise, especially on Intel Macs. Presently, the best solution is to use Standalone build settings specific to each architecture.

[microphone-permission-issue-on-intel-macs-with-universal-builds.md](microphone-permission-issue-on-intel-macs-with-universal-builds.md "mention")



## Error Index

Follow this Table to navigate to our most common errors.

<table><thead><tr><th width="160">Name</th><th width="232">Sample Error</th><th width="211">Reason for Error</th><th></th><th data-hidden>Sample Error Log</th><th data-hidden>Link to Solution</th><th data-hidden>Reason</th></tr></thead><tbody><tr><td>Enabled Assembly Validation</td><td><pre data-overflow="wrap"><code>Assembly 'Assets/Convai/Plugins/Grpc.Core.Api/lib/net45/Grpc.Core.Api.dll' will not be loaded due to errors: 
Grpc.Core.Api references strong named System.Memory Assembly references: 4.0.1.1 Found in project: 4.0.1.2.
</code></pre></td><td>Unity, by default, checks for exact version numbers for the included assemblies. For our plugin, this is not necessary, since we use the latest libraries.</td><td><a data-mention href="enabled-assembly-validation.md">enabled-assembly-validation.md</a></td><td>Assembly 'Assets/Convai/Plugins/Grpc.Core.Api/lib/net45/Grpc.Core.Api.dll' will not be loaded due to errors: Grpc.Core.Api references strong named System.Memory Assembly references: 4.0.1.1 Found in project: 4.0.1.2.</td><td><a data-mention href="enabled-assembly-validation.md">enabled-assembly-validation.md</a></td><td>Unity by defa</td></tr><tr><td>Missing NewtonSoft Json</td><td><pre data-overflow="wrap"><code>Assets\Convai\Plugins\GLTFUtility\Scripts\Spec\GLTFPrimitive.cs(8,4): error CS0246: The type or namespace name 'JsonPropertyAttribute' could not be found (are you missing a using directive or an assembly reference?)
</code></pre></td><td>Our plugin needs Newtonsoft Json as a dependency. It is often present as part of Unity but occasionally, it can be missing. </td><td><a data-mention href="missing-newtonsoft-json.md">missing-newtonsoft-json.md</a></td><td></td><td></td><td></td></tr><tr><td>Missing Animation Rigging</td><td><pre data-overflow="wrap"><code>Assets\Convai\Scripts\Utils\HeadMovement.cs (2,30): error CS0234: The type or namespace name 'Rigging' does not exist in the namespace 'UnityEngine.Animations' (are you missing an assembly reference?)
</code></pre></td><td>We use the Animation Rigging package for Eye and Neck tracking. If Unity does not automatically add it, we need to add it manually from the package manager.</td><td><a data-mention href="missing-animation-rigging.md">missing-animation-rigging.md</a></td><td></td><td></td><td></td></tr><tr><td>Microphone Permission Issues</td><td>The microphone icon lights up but there is no user transcript in the chat UI. The character seemingly not replying to what the user is saying.</td><td>The plugin requires microphone access which is sometimes not enabled by default.</td><td><a data-mention href="microphone-permission-issues.md">microphone-permission-issues.md</a></td><td></td><td></td><td></td></tr><tr><td>OVR Lip-sync Audio Loopback not Enabled</td><td>There is not sound coming from the character but transcripts are visible.</td><td></td><td><a data-mention href="ovr-lipsync-audio-loopback-not-enabled.md">ovr-lipsync-audio-loopback-not-enabled.md</a></td><td></td><td></td><td></td></tr><tr><td>Default Animations Incompatibility</td><td>The default animations that ship with the plugin seems broken. The hands seem to intersect with the body.</td><td>The animation avatar is incompatible with the character mesh.</td><td><a data-mention href="default-animations-incompatibility.md">default-animations-incompatibility.md</a></td><td></td><td></td><td></td></tr><tr><td>Animations have Facial Blendshapes</td><td>The Lip-sync from characters are either not visible or are very faint.</td><td>Some types of animations control facial blendshapes. These animations prevent the lip-sync scripts to properly edit the facial blendshapes.</td><td><a data-mention href="animations-have-facial-blendshapes.md">animations-have-facial-blendshapes.md</a></td><td></td><td></td><td></td></tr><tr><td>Jaw Bone in Avatar is not Free</td><td>The Lip-sync from characters are either not visible or are very faint.</td><td>The animation avatar for the character may be using the Jaw Bone. If we set the mapping free to none, the script will be able to manipulate the jaw bone freely. </td><td><a data-mention href="jaw-bone-in-avatar-is-not-free.md">jaw-bone-in-avatar-is-not-free.md</a></td><td></td><td></td><td></td></tr><tr><td>Mac Security Permission Issue</td><td>Security Permission Issues with <code>grpc_csharp_ext.bundle</code> DLL in Unity on MacOS.</td><td>MacOS's security protocols can prevent certain unsigned external DLLs, like <code>grpc_csharp_ext.bundle</code>, from functioning correctly in Unity.</td><td><a data-mention href="macos-permission-issues.md">macos-permission-issues.md</a></td><td></td><td></td><td></td></tr><tr><td>Microphone Permission Issue with Universal Builds on Intel Macs in Unity</td><td>No Microphone access request pops up</td><td>Incompatibility between Intel and Apple Silicon versions of <code>grpc_csharp_ext.bundle</code> when attempting a Universal build.</td><td><a data-mention href="microphone-permission-issue-on-intel-macs-with-universal-builds.md">microphone-permission-issue-on-intel-macs-with-universal-builds.md</a></td><td></td><td></td><td></td></tr></tbody></table>

For any other issues, please feel free to reach out to [support@convai.com](mailto:support@convai.com) or on our [Discord Server](https://discord.gg/pCKPxpn352).
