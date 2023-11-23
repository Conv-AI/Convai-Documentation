# OVR Lipsync Audio Loopback not Enabled

This error occurs when using Oculus Lip-Sync (default when importing Ready Player Me character). We can see the Lip-Sync happening and response is received and displayed as character transcript. But we cannot hear the response from the cahracter. This is could be due to the audio loopback not enabled in the OVRLipSyncContext component in the NPC GameObject.

To enable it, head to the NPC GameObject and scroll down to the OVR Lip Sync Context component and check the Audio Loopback flag.

&#x20;

<figure><img src="../../../.gitbook/assets/image (18).png" alt=""><figcaption></figcaption></figure>
