# Building for macOS Universal apps

## Overview

When building Unity projects for macOS, developers may encounter issues with microphone permissions, particularly when targeting both Intel and Apple Silicon Macs. This document outlines the problem, symptoms, causes, and solutions to help ensure successful access to the microphone across different Mac architectures.

### Problem Description

Some users have reported that while building macOS universal apps, Apple Silicon Macs handle microphone permissions without issue, while Intel Macs may fail to access the microphone due to differences in architecture. This can result in a lack of microphone response, DLL not found Exceptions, error messages, potential application crashes, or no audio input being detected.

### Cause

The issue stems from the `grpc_csharp_ext.bundle`, which is crucial for networking in Unity projects. There are separate versions of this DLL for Intel and Apple Silicon architectures, and they cannot be easily merged or applied universally. The grpc library currently lacks dedicated support for resolving these dll issues in Unity.

## Solutions

### Standalone Build Settings

* **For Intel Macs:** Use Standalone builds targeted specifically for the Intel architecture to ensure compatibility.
* **For Apple Silicon Macs:** Prefer Standalone builds for the ARM64 framework for optimal performance, although Universal builds are also an option.

<figure><img src="../../../.gitbook/assets/image (6) (1) (1) (1) (1).png" alt="" width="563"><figcaption></figcaption></figure>

### New Procedure for Universal Builds from Intel Macs

After completing a Universal build on an Intel Mac, you must manually update the `grpc_csharp_ext.bundle` to ensure proper functionality. Follow these steps:

1.  Locate the `.app` file generated by the build process.\


    <figure><img src="../../../.gitbook/assets/image (273).png" alt="" width="563"><figcaption></figcaption></figure>
2.  Right-click on the `.app` file and select "Show Package Contents."\
    \


    <figure><img src="../../../.gitbook/assets/image (1) (1) (1) (1) (1) (1) (1) (1).png" alt="" width="563"><figcaption></figcaption></figure>
3.  Navigate to the `Contents/Plugins` folder within the package.\
    \


    <figure><img src="../../../.gitbook/assets/image (2) (1) (1) (1) (1).png" alt="" width="563"><figcaption></figcaption></figure>
4.  Replace the contents of this folder with the components from the provided plugin folder ([link to plugin folder](https://drive.google.com/drive/folders/1oZSsFbd3SLSagJafwrLq1swdgL0Hr3Hm?usp=drive_link)).\


    <figure><img src="../../../.gitbook/assets/image (3) (1) (1) (1) (1) (1).png" alt="" width="563"><figcaption></figcaption></figure>

    <figure><img src="../../../.gitbook/assets/image (4) (1) (1) (1) (1) (1).png" alt="" width="563"><figcaption></figcaption></figure>

**Important:** The `grpc_csharp_ext.bundle` may not be included correctly in the final build when built from an Intel Mac. Always verify that the `Plugins` folder in the build contains the correct DLLs. If there is any confusion or the DLLs are missing, replace or add the contents of the `Plugins` folder with the one provided by us.

***

## Conclusion

Building for macOS requires careful consideration of the distinct Intel and Apple Silicon architectures. The current best practice is to use Standalone build settings tailored to the specific architecture of the target Mac. As we progress, we will have a more integrated solution for managing DLLs that will simplify the development process for universal macOS applications.

