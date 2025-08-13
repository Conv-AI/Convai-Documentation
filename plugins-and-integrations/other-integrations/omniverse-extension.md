---
description: >-
  This guide will show you how to integrate the Convai and NVIDIA Omniverse
  using the Convai Extension plugin.
hidden: true
---

# Omniverse Extension

{% embed url="https://www.youtube.com/playlist?list=PLn_7tCx0ChiqbU3J3JPIKagfiv6S3wK7i" %}
Extension Overview
{% endembed %}

### Installation

To install the Convai Omniverse Extension, follow these steps:

1. Download the [latest version](https://github.com/Conv-AI/ov_extension/archive/refs/tags/1.0.3.zip) of the extension.
2. Extract the zip file into your chosen directory.
3. Open the Omniverse app of your choice (e.g Code) and from the `Window` menu click `Extensions`.
4. In the `Extensions` tab, click the gear icon in the top right.\
   ![](<../../.gitbook/assets/image (102).png>)
5.  Click the green plus icon in the Edit column and add the absolute path to the `exts` folder found in the repository directory.\


    <figure><img src="../../.gitbook/assets/image (201).png" alt=""><figcaption></figcaption></figure>
6.  Select the `Third Party` tab and search for `Convai` in the top left search bar, make sure to check Enabled.\


    <figure><img src="../../.gitbook/assets/image (103).png" alt=""><figcaption></figcaption></figure>
7. The Convai window should appear, drag it and dock it in any suitable area of the UI.&#x20;
8.  If the Convai window does not appear, go to the `Window` menu and select `Convai` from the list.



## Configuration

To add your API Key and Character ID, follow these steps:

1. Sign up at [Convai](https://convai.com/).
2. On the website click the gear icon in the top-right corner of the playground then copy and paste the API key into the `Convai API Key` field in the Convai extension window.
3. Go to the [Dashboard](https://convai.com/pipeline/dashboard) and on the left panel and either create a new character or select a sample one.
4. Copy the Character ID and paste it in the `Character ID` field in the extension window.

## Interacting with the character

1. Click `Start Talking` to initiate the conversation
2. Click `Stop` when done talking for the character to respond.

### Running the Demo

1. Open your chosen Omniverse app (e.g., Code).
2. Go to `File->Open` and navigate to the repo directory.
3. Navigate to `<repo directory>/ConvaiDemoStage/ConvaiDemo.usd` and click \`open it.
4. Click the `play` button from the `Toolbar` menu on the left.\
   ![](<../../.gitbook/assets/image (95).png>)
5. Click `Start Talking` in the `Convai` window to talk to the character then click `Stop` to send the request.

## Actions

Actions can be used to trigger events with the same name as the action in the `Action graph`. They can be used to run animations based on the action received. To try out actions:

1. Add a few comma-separated actions to `Comma seperated actions` field (e.g jump, kick, dance, etc.).
2. The character will select one of the actions based on the conversation and run any event with the same name as the action in the `Action Graph`.

### Notes

* The demo stage includes only talk and idle animations. However, it is possible to add more animations and trigger them using the action selected by the character. More on that in the future.
