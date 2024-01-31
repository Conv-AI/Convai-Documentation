---
description: >-
  This guide will help you integrate Convai's WebGL capabilities into your Unity
  projects, enabling you to bring to life AI characters with human-like
  conversational abilities.
---

# Building for WebGL

## Description

Convai's Unity WebGL SDK is designed to complement the standalone application capabilities of our Unity Asset Store version. With this specialized SDK, you can build and deploy interactive WebGL applications that leverage Convai's advanced conversation pipeline.

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

## Development and Testing

### WebGL Incompatibility with Unity Editor

When attempting to play the scene in the Unity Editor, you may encounter the following error:

{% code overflow="wrap" %}
```
WebGL SDK does not run in Unity Editor. Please build and run in WebGL.
```
{% endcode %}

This error occurs because the WebGL SDK cannot be tested directly within the Unity Editor. To test your WebGL application, you must create a development build.

### Building for WebGL

1. Go to `File` > `Build Settings` and switch the platform to WebGL.
2. Check the `Development Build` option for faster iterations.
3. Click on `Switch Platform`.

<figure><img src="../../.gitbook/assets/image (297).png" alt=""><figcaption></figcaption></figure>

### Configuring Player Settings

Once the platform conversion is complete,

1. Open the file`Player Settings`.
2. Navigate to the page`WebGL settings`.
3. Under the`Resolution and Presentation` tab, select the`Convai PWA Template`.

<figure><img src="../../.gitbook/assets/image (299).png" alt=""><figcaption></figcaption></figure>

### Running the Build

1. Select the folder where you want the build to be located.
2.

    <figure><img src="../../.gitbook/assets/image (300).png" alt=""><figcaption></figcaption></figure>
3. A web page with the WebGL version of the game will open. Allow microphone access when prompted.

<figure><img src="../../.gitbook/assets/image (23).png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
The first build may take some time.\
For subsequent builds and runs, use the Unity shortcut key Ctrl + B.
{% endhint %}

{% hint style="info" %}
When you are ready with your production build, just uncheck the Development Build field in the Build Settings before publishing
{% endhint %}

