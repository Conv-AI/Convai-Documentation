---
description: >-
  Learn the different ways to test your AI character in Convai Playground,
  including text chat, voice input, and video call with an avatar.
---

# Testing a Character

## Introduction

Once you have created a character, it's important to test how it interacts. Convai provides multiple ways to test your characters — from quick text and voice interactions to fully immersive video calls with custom avatars. This ensures you can refine personality, responsiveness, and interaction style before final deployment.

***

## Testing Options

### Text and Voice Chat

To test your character via text or voice, open the character's chat interface:

* From your **Dashboard**, click on the character card you want to test.
* The chat interface opens as a full conversation view, with your messages on the right (green) and the character's responses on the left (white).
* Type a message in the **"Type a message..."** input at the bottom and press enter to send.
* Or click the **microphone button** on the right side of the input bar, speak, and send your voice input.

Each message shows a timestamp. A small **eye icon** appears below each message — click it to open **Mindview** for that specific exchange.

<figure><img src="../../.gitbook/assets/image (9).png" alt=""><figcaption></figcaption></figure>

***

#### Mindview for Playground Chat

**Mindview** lets you inspect how the character processed a specific message. Click the **eye icon** below any message to open it.

Mindview displays:

* **User Query** and **Response** at the top — the exact exchange being inspected.
* **Model and Character ID** — the LLM and character version used for that response.
* **Structured / Raw toggle** — switch between a readable structured view and the raw prompt output.
* **Static Prompt** — the fixed parts of the character's prompt, broken into:
  * **Core Description** – the character's base personality and instructions.
  * **Languages** – the languages the character is configured to respond in.
  * **Output Format** – the response style instruction given to the model.
* **Dynamic Prompt** — the context injected at runtime for that specific exchange, including **Context Setting** and other dynamic elements.

Mindview is useful for debugging unexpected responses, verifying that your character description and knowledge bank are being applied correctly, and understanding exactly what the model receives for any given turn. Read the detailed [Mindview Docs](https://docs.convai.com/api-docs/convai-playground/character-customization/mindview) to learn more.

<figure><img src="../../.gitbook/assets/Screenshot 2026-05-08 144842.png" alt=""><figcaption></figcaption></figure>

***

#### Chat Interface Controls

**Left sidebar icons (top-left of the chat):**

| Icon             | Function                                               |
| ---------------- | ------------------------------------------------------ |
| **Audio toggle** | Mute or unmute the character's voice output            |
| **Copy**         | Copy the conversation text                             |
| **Reset**        | Restart the session and clear the conversation history |

**Top-right icons:**

| Icon       | Function                              |
| ---------- | ------------------------------------- |
| **Camera** | Start a video call with the character |
| **Share**  | Share the character                   |

***

#### Quick Replies

After each character response, a **Quick replies** section appears below the message with contextually generated reply suggestions. Click any chip to send that reply instantly without typing.

Quick replies are dynamically generated based on the ongoing conversation, so they update with each new character response.

***

### **2. Video Call**

You can test your character in a **video call** for both visual and voice interaction.

**From the Dashboard:**

* Locate the character's card.
* Click the **green camera icon** on the card to start a video call instantly.

<figure><img src="../../.gitbook/assets/image (11).png" alt=""><figcaption></figcaption></figure>

**From the Character Page:**

* Click the character’s card to open its details.
* In the top-right section, under the character’s thumbnail, click the **video call button**.

The video call gives you a real-time view of the character's visual appearance and voice together, offering a more immersive test environment.

<figure><img src="../../.gitbook/assets/image (12).png" alt=""><figcaption></figcaption></figure>

This method allows you to experience both the character’s **visual appearance** and **voice** in real-time, offering a more immersive test environment.

<figure><img src="../../.gitbook/assets/image (13).png" alt=""><figcaption></figcaption></figure>

***

## Conclusion

Convai's testing options make it easy to evaluate and refine your characters. Whether you prefer a fast text-based interaction with quick reply suggestions, a voice conversation, or a full video call with your custom avatar, you can ensure your AI character behaves as intended before deployment. Use Mindview on any message to inspect the underlying prompt and debug character behavior at any point in the conversation.
