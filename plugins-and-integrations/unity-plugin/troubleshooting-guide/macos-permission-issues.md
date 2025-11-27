---
description: >-
  macOS security permission issue with custom DLLs in Unity and Mac
  Configuration in build settings
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/plugins-and-integrations/unity-plugin/troubleshooting-guide/macos-permission-issues
---

# macOS Permission Issues

## Allowing the grpc\_csharp\_ext.bundle dll file in macOS

Using external DLLs in Unity on MacOS can lead to security permission issues due to Apple's strict security measures. Here's a step-by-step guide to resolving this common problem.

1.  **Verify the Problem**:



    <figure><img src="../../../.gitbook/assets/Screenshot 2023-09-09 205554.png" alt=""><figcaption></figcaption></figure>
2.  **Manually Allow Blocked DLLs**:

    * Open System Preferences on your Mac.
    * Navigate to "Security & Privacy".

    <img src="../../../.gitbook/assets/Screenshot 2023-09-09 205654.png" alt="" data-size="original">

    * Under the "Security" tab, you might see a message at the bottom about the DLL being blocked. Click "Allow Anyway" or "Open Anyway" and enter password if asked.

    ![](<../../../.gitbook/assets/Screenshot 2023-09-09 205734 (1).png>)![](<../../../.gitbook/assets/Screenshot 2023-09-09 205753.png>)


3. **Modify Gatekeeper settings**: MacOS's Gatekeeper can prevent unidentified developers' software from running. To allow the DLL:
   * Open the Terminal (found in Applications > Utilities).
   * Type `sudo spctl --master-disable` and press Enter.
   * This command will allow apps to be downloaded from anywhere.
   * Now, try running the Unity project again.
   * After you're done, you should re-enable Gatekeeper with `sudo spctl --master-enable`  to avoid any malware.
4. **Check File Permissions**: Ensure the DLL has the correct file permissions.
   * In Finder, right-click (or control-click) on the DLL file and choose "Get Info".
   * Under “Sharing & Permissions”, ensure that your user account has "Read & Write" permissions.
5. **Review Unity's Plugin Settings**:
   * In the Unity editor, select the DLL in the Project view.
   * In the Inspector window, make sure the appropriate platform (in this case, Mac OS X) and architecture (Apple Silicon, Intel-64) is selected for the DLL.
   * Ensure that the "Load on Startup" and other pertinent options are checked (should be enabled by default)



## Mac Configuration in Player Settings during build

*   **Update Mac Configuration:**

    * In Unity, navigate to `Edit > Project Settings > Player`.
    * Scroll down and click on `Other Settings`

    <figure><img src="../../../.gitbook/assets/Screenshot 2023-09-09 205901.png" alt=""><figcaption></figcaption></figure>

    * Scroll down again to find Mac Configuration section

    <figure><img src="../../../.gitbook/assets/Screenshot 2023-09-09 205922.png" alt=""><figcaption></figcaption></figure>



    * Update the Mac Configuration section (follow the below Screenshot)



    <figure><img src="../../../.gitbook/assets/Screenshot 2023-09-09 205958 (1).png" alt=""><figcaption></figcaption></figure>
