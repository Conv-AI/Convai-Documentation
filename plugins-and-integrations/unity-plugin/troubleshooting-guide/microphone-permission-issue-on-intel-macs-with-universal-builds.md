# Microphone Permission Issue on Intel Macs with Universal Builds

**Problem**:

When attempting to build a Unity project for macOS with the Universal build setting, users have reported an issue pertaining to microphone permissions. Specifically, while Apple Silicon Macs exhibit no problematic behavior, Intel Macs may not successfully access the microphone due to underlying architectural differences.

#### Symptoms:

* Lack of response or inaccessibility of the microphone.
* Possible error messages or prompts relating to microphone permissions.
* Potential application crashes when trying to utilize microphone features.
* No audio input detected or recorded within the application.

#### Cause:

The heart of this issue lies within the `grpc_csharp_ext.bundle`, a fundamental component for networking within Unity projects. Distinct versions of this DLL have been developed: one catering to the Intel architecture and another optimized for the Apple Silicon ARM64 framework. The challenges arise when attempting to cater to both architectures simultaneously:

* The inherent differences between the two DLL versions, driven by the vastly different architectures, prevent them from being seamlessly merged or universally applied.
* Presently, grpc does not offer dedicated support or resolution for these discrepancies, especially in the context of Unity or Xamarin.
* Efforts to modify the Universal app post-build to make it functional for Intel machines introduce further complications. macOS's security protocols interpret these modifications as potential threats, preventing the app from running on ARM machines.
* Introducing additional files to rectify the situation for ARM disrupts functionality for Intel, creating a cyclic challenge without a straightforward resolution.

#### Solutions:

1. **Standalone Build Settings for Intel Macs**:
   * If you are using an Intel Mac, the recommendation is clear: Opt for Standalone builds targeted specifically for the Intel architecture. This will ensure compatibility and seamless microphone access.
2. **Standalone Build Settings for Apple Silicon Macs**:
   * Even if you possess an Apple Silicon Mac, it's advisable to lean towards Standalone builds for the ARM64 framework. While Universal builds remain an option, Standalone builds guarantee optimal performance and functionality.
3. **Update Unity**:
   * Always ensure you are working with the latest or recommended version of Unity suitable for macOS builds. Some nuances or bugs might be addressed in newer releases or specific patches.
4. **External Plugins**:
   * If your project leverages external plugins or libraries, especially those interacting with the microphone, ensure they are up-to-date and compatible with the macOS version you aim to target.
   * Double-check if these plugins support Universal builds or if distinct versions exist for Intel and Apple Silicon.

**Please contact Convai Support at** [support@convai.com](mailto:support@convai.com) **if none of the solutions work**

#### Conclusion:

Building for macOS, given the coexistence of Intel and Apple Silicon architectures, presents unique challenges. When leveraging `grpc_csharp_ext.bundle`, the limitations become pronounced. For now, the Standalone build settings remain the safest and most effective path forward, ensuring both compatibility and functionality across architectures. As the landscape evolves, one can hope for more integrated solutions in the future.
