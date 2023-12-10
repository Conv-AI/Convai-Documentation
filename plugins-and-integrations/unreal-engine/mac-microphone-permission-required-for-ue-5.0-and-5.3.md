---
description: >-
  The Convai plugin requires microphone access in Unreal Engine (UE) 5.0 and 5.3
  on macOS.
---

# Mac Microphone Permission: Required for UE 5.0 and 5.3

## Editor Mic **Permission Setup**

1. Temporarily disable SIP following instructions on [Disabling and Enabling SIP](https://developer.apple.com/documentation/security/disabling\_and\_enabling\_system\_integrity\_protection).
2. Clone the `tccutil` repository from GitHub: [tccutil on GitHub](https://github.com/DocSystem/tccutil).
3. Open a terminal and cd into the directory where `tccutil.py` is found.
4. Make sure [Python is installed](https://www.dataquest.io/blog/installing-python-on-mac/) and run the command: `sudo python3 tccutil.py -e -id com.epicgames.UnrealEditor --microphone.`
5. [Reenable SIP](https://developer.apple.com/documentation/security/disabling\_and\_enabling\_system\_integrity\_protection).

## Packaging Games with Convai

1. After packaging your game, locate the `Info.plist` file in the packaged game directory. This is typically found by right-clicking the package, selecting 'Show Package Contents', and editing `/Contents/Mac/Info.plist`.
2. Add the following entries to request microphone access:

```xml
<key>NSMicrophoneUsageDescription</key>
<string>Your custom message explaining why Convai needs microphone access</string>
```

<figure><img src="../../.gitbook/assets/image (259).png" alt=""><figcaption><p>Example Info.plist after adding the microphone permission lines</p></figcaption></figure>

3. Save the changes to the `Info.plist` file.
