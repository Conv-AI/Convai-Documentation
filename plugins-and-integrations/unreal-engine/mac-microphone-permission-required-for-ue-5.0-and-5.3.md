---
description: >-
  The Convai plugin requires microphone access in Unreal Engine (UE) 5.0 and 5.3
  on macOS.
---

# Mac Microphone Permission: Required for UE 5.0 and 5.3

## Editor Mic **Permission Setup**

1. Temporarily Disable SIP - Follow the instructions provided in the [Disabling and Enabling SIP](https://developer.apple.com/documentation/security/disabling\_and\_enabling\_system\_integrity\_protection) guide - Note: make sure to run the command `csrutil disable`  in the terminal.
2. Clone the tccutil Repository - Open the Terminal, and enter the following command to clone the repository: \
   `git clone https://github.com/DocSystem/tccutil`&#x20;
3. Navigate to the tccutil Directory by entering `cd tccutil` into the terminal.
4. Ensure [Python is installed](https://www.dataquest.io/blog/installing-python-on-mac/) on your system. Run the tccutil command In the Terminal to allow microphone access for Unreal Engine:\
   `sudo python3 tccutil.py -e -id com.epicgames.UnrealEditor --microphone --enable`
5. Re-enable SIP Once the modifications are complete, [follow the same guide](https://developer.apple.com/documentation/security/disabling\_and\_enabling\_system\_integrity\_protection) to re-enable System Integrity Protection but this time run the command `csrutil enable`.

## Packaging the app with Convai (Not required for MacOS 14.x)

After packaging your game, if you notice any crash or microphone not working then proceed to doing the following steps

1. &#x20;locate the `Info.plist` file in the packaged game directory. This is typically found by right-clicking the package, selecting 'Show Package Contents', and editing `/Contents/Mac/Info.plist`.
2. Add the following entries to request microphone access:

```xml
<key>NSMicrophoneUsageDescription</key>
<string>Your custom message explaining why Convai needs microphone access</string>
```

<figure><img src="../../.gitbook/assets/image (20) (1).png" alt=""><figcaption><p>Example Info.plist after adding the microphone permission lines</p></figcaption></figure>

3. Save the changes to the `Info.plist` file.
