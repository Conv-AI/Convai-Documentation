---
description: >-
  This guide will help you integrate Convai's WebGL capabilities into your Unity
  projects, enabling you to bring to life AI characters with human-like
  conversational abilities.
---

# Building for WebGL

## Description

Convai's Unity WebGL SDK is designed to complement the standalone application capabilities of our Unity Asset Store version. With this specialized SDK, you can build and deploy interactive WebGL applications that leverage Convai's advanced conversation pipeline. Please see the instructions below or check out our [_latest tutorial video_](https://youtu.be/JXjcHEnEPCQ) on YouTube.

{% embed url="https://youtu.be/JXjcHEnEPCQ" %}

## Getting Started

### Download the SDK and Demos

{% hint style="info" %}
[**Download the WebGL version of the Convai Unity SDK here.**](https://drive.google.com/file/d/1mSgdWNnttNXjjA5Qvclwyy2\_33zncefv/view?usp=sharing)
{% endhint %}

{% hint style="info" %}
[**Download the Complete  WebGL Demo here.**](https://github.com/Conv-AI/Unity-WebGL-Demo-Game)
{% endhint %}

{% hint style="info" %}
[**Try out the Demo on itch.io here.**](https://convai.itch.io/webgl-demo)
{% endhint %}

### Prerequisites

{% hint style="warning" %}
Please ensure that Git is installed on your computer prior to proceeding.\
[**Download Git from here.**](https://git-scm.com/downloads)
{% endhint %}

### Import and Setup Instructions

Follow the Import and Setup Instructions from [import-and-setup.md](import-and-setup.md "mention") and [setting-up-unity-plugin.md](setting-up-unity-plugin.md "mention").&#x20;

### WebGL Incompatibility with Unity Editor

When attempting to play the scene in the Unity Editor, you may encounter the following error:

{% code overflow="wrap" %}
```
WebGL SDK does not run in Unity Editor. Please build and run in WebGL.
```
{% endcode %}

This error occurs because the WebGL SDK cannot be tested directly within the Unity Editor. To test your WebGL application, you must create a development build.

## Switching to WebGL

Now, your Unity setup is done, let's setup WebGL

Head on over to `File` → `Build Settings`, then:

1. Click on `WebGL`.
2. Check the `Development Build` box.
3. Select `Switch Platform.`

Patience, remember? This shift takes a bit.

After the platform is switched to WebGL, click on `Player Settings`.This is where the fun begins:

<figure><img src="../../.gitbook/assets/image (297).png" alt=""><figcaption></figcaption></figure>

### Configuring Player Settings

Once the platform conversion is complete,

1. Open the file`Player Settings`.
2. Navigate to the page`WebGL settings`.
3. Under the`Resolution and Presentation` tab, select the`Convai PWA Template`.

<figure><img src="../../.gitbook/assets/image (299).png" alt=""><figcaption></figcaption></figure>

## Importing Characters and Building the Scene

After the reloads is completed, check if the settings have changed. then, close all the open menus and follow these steps :

<figure><img src="https://cdn.videotap.com/6608/screenshots/RM98hWOigrswo0Uksw8F-202.29.png" alt=""><figcaption></figcaption></figure>

1. Double-click the `Convai folder` and go to scenes.
2. Open the `Convey Demo WebGL` scene.
3. Head to Convai's website, grab your API key, and input it back in Unity via `Convai` → `Convai Setup`.
4. Now, head again to the Convai’s website and grab your favourite character’s id and paste it to `Convai` → `Character Importer`.

Remember, Unity's editor won't let us test WebGL directly. But fear not, there's a `Build and Run` option:

<figure><img src="https://cdn.videotap.com/6608/screenshots/suKZ4w5jIDskFWyBqyO1-261.69.png" alt=""><figcaption></figcaption></figure>

1. Go back to `File` → `Build Settings`.
2. Click `Add Open Scenes` and then `Build and Run`.

Choose a folder for the build output, make a new one if needed, and name it "WebGL."

<figure><img src="https://cdn.videotap.com/6608/screenshots/z5kMvyZPsvD8V5dvudCN-274.6.png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
The First build may take some time.\
For subsequent builds and runs, use the Unity shortcut key Ctrl + B.
{% endhint %}

The first build is the longest, so feel free to stretch a bit – but don't venture too far. Soon, you'll greet our demo character, Amelia, or any other character you brought into your digital oasis. Just give your Microphone permissions and here you go!

## Engaging with your Convai AI NPCs

Now the magic happens. Press and hold 'T' to chat with your carefully cultivated character. Or click on the text box to type out a question. And for the attention to detail – press F10 to access the settings panel where you can change your name and the UI style to your liking.

<figure><img src="https://cdn.videotap.com/6608/screenshots/hnaNRdZthU6yzX7gmIvw-318.59.png" alt=""><figcaption></figcaption></figure>

Feeling accomplished? You should! You now have a successfully working WebGL build in your browser. Curious developers can take a step further by downloading the project files from GitHub, available for all who desire to peek behind the curtain.

{% hint style="info" %}
When you are ready with your production build, just uncheck the Development Build field in the Build Settings before publishing
{% endhint %}

