---
description: >-
  Learn how to upload, manage, and connect knowledge files to your AI character
  using Knowledge Bank — including RAG and In-Context retrieval and multimodal
  files.
---

# Knowledge Bank

{% embed url="https://www.youtube.com/watch?v=MCbBHA2BKLM" %}

{% endembed %}

## Introduction

The **Knowledge Bank** is where you store and manage information that your AI character can access during conversations. By uploading documents or adding text directly, you can give your character specific domain knowledge, enabling more accurate, relevant, and context-aware responses.

All files uploaded to your Knowledge Bank are linked to your Convai account and can be connected to any of your characters. This makes it an essential tool for training characters to respond with company-specific, product-specific, or topic-specific information.

<figure><img src="../../.gitbook/assets/image (19).png" alt=""><figcaption></figcaption></figure>

***

## Retrieval modes: RAG and In-Context

The Knowledge Bank offers two ways for your character to use connected knowledge. You pick the mode at the top of the Knowledge Bank tab.

* **RAG** — The classic mode. Connected files are indexed and the character retrieves only the most relevant passages for each user message. Best for **large** text knowledge bases where only a fraction is relevant to any one question. RAG accepts **text files only** (`.txt`, `.csv`).
* **In-Context** — The whole connected knowledge base is placed directly in the character's context every turn (and cached for efficiency). Best for **compact, high-value** knowledge you want the character to always have in full — and it supports **multimodal** files (images, PDF, audio, video) in addition to text, depending on the selected LLM.

{% hint style="info" %}
In-Context KB is available only on **supported LLMs**. When you enable In-Context, the character's LLM is automatically set to a supported model. If you later switch to a model that doesn't support In-Context KB, Convai asks you to confirm — switching turns In-Context off and falls back to RAG (text-only).
{% endhint %}

***

## Supported file types

The file types you can upload and connect depend on the retrieval mode and, for In-Context, on the selected LLM.

| Mode | Supported files |
| ---- | --------------- |
| **RAG** | Text only — `.txt`, `.csv` |
| **In-Context** | Text (`.txt`, `.csv`), **images**, **PDF**, **audio**, **video** — subject to the selected model's capabilities |

Not every In-Context model supports every modality. For example, some self-hosted models accept only text and images. The Knowledge Bank tab shows a **"Supported file types for the selected model"** line so you always know what the current model accepts before you pick a file. The upload picker and drag-and-drop only accept those types.

{% hint style="warning" %}
Office documents (`.doc`, `.docx`, `.ppt`, `.pptx`, `.xls`, `.xlsx`, …) are **not** supported. The models can't read them raw and they aren't text-extracted for this feature. Convert them to `.txt`/`.csv` or PDF first.
{% endhint %}

### In-Context size limit

In-Context KB places the whole connected knowledge base in the prompt, so it has a **fixed size limit**. If your connected files exceed the limit, the Knowledge Bank tab shows an over-limit warning and blocks further uploads until you remove documents to get back under the cap. RAG has no such per-prompt limit (overall storage still depends on your plan).

***

## Knowledge Bank Sections

### 1. My Documents

* Displays all files uploaded to your account.
* Information shown:
  * **Name** – File name.
  * **Type** – The file's modality (text, image, PDF, audio, or video).
  * **Size** – File size.
  * **Status** – Whether the file is **Available** (ready to use) and whether it is **Connected** to the current character.
* Actions available:
  * **Connect** – Attach the file to the current character.
  * **Disconnect** – Detach the file from the character (it stays in your Knowledge Bank, inactive).
  * **Edit** – Modify a text file's content.
  * **Download** – Save the file locally.
  * **Delete** – Remove the file permanently.

<figure><img src="../../.gitbook/assets/image (21).png" alt=""><figcaption></figcaption></figure>

### 2. Upload Knowledge

* Upload files from your computer.
* In **RAG** mode, only `.txt`/`.csv` are accepted. In **In-Context** mode, the picker accepts the file types the **selected model** supports (text, images, PDF, audio, video).
* Once uploaded, files are stored in your account's Knowledge Bank for use with any character.

<figure><img src="../../.gitbook/assets/image (22).png" alt=""><figcaption></figcaption></figure>

### 3. Add Knowledge

* Create a new text file by entering **plain text** directly into the editor.
* Name the file and save it in `.txt` format.

<figure><img src="../../.gitbook/assets/image (23).png" alt=""><figcaption></figcaption></figure>

{% hint style="success" %}
While a file is processing, its status reads "Learning…". Refresh occasionally until the status becomes **Available**. Raw media in In-Context mode (images, audio, video) is available immediately — no indexing wait.
{% endhint %}

***

## Using the Knowledge Bank with Your Character

### Example

We uploaded a file named **Employee Onboarding Guide.txt** with the following content:

```
This document provides step-by-step guidance for new hires.
Complete HR documentation within the first 3 days of joining.
Attend the mandatory orientation session.
Set up company email and access credentials via IT Support.
Review the Code of Conduct and Data Privacy Policy.
```

<figure><img src="../../.gitbook/assets/image (24).png" alt=""><figcaption></figcaption></figure>

### Testing Without Connecting the File

* Open the **Chatbox**.
* Ask: _"I'm a new hire. What should I do during my first week here?"_
* Result: The character responds using its general personality and AI model knowledge, not the uploaded file.

<figure><img src="../../.gitbook/assets/Screenshot 2025-08-08 194114.png" alt=""><figcaption></figcaption></figure>

### Testing by Connecting the File

* Go to **Knowledge Bank** → **My Documents**.
* Click **Connect** on the file.
* In the Chatbox, click **Reset Chat** (top left) to start a new session.
* Ask the same question again.

**Result:** This time, the character's response is based on the exact steps provided in the **Employee Onboarding Guide** file.

<figure><img src="../../.gitbook/assets/Screenshot 2025-08-08 194207.png" alt=""><figcaption></figcaption></figure>

***

## Best Practices

{% hint style="info" %}
Always **reset the chat session** after connecting a new knowledge file so the latest data is used.
{% endhint %}

{% hint style="info" %}
Use **RAG** for large text knowledge bases and **In-Context** for compact, always-relevant knowledge or when you need multimodal files (images, PDF, audio, video).
{% endhint %}

{% hint style="info" %}
The **total storage size** for uploaded files depends on your Convai subscription plan. See the [**Pricing**](https://convai.com/pricing) page for limits. In-Context KB additionally has a fixed per-prompt size cap.
{% endhint %}

***

## Conclusion

The Knowledge Bank is a powerful way to give your characters precise and reliable information. Choose **RAG** to retrieve the most relevant passages from a large text corpus, or **In-Context** to give your character its full knowledge base — including images, PDFs, audio, and video — every turn. Either way, connecting domain-specific knowledge ensures your AI not only has personality but also the expertise to answer questions with accuracy and authority.
