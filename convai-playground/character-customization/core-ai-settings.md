---
description: >-
  Learn how to configure moderation, foundation model selection, and temperature
  for your AI character
---

# Core AI Settings

## Introduction

The **Core AI Settings** section defines the foundational behavior of your AI character by controlling safety filters, the underlying language model, and the creativity level of its responses. These settings have a significant impact on how your character interacts with users, balancing safety, accuracy, and creativity.

<figure><img src="../../.gitbook/assets/image (29).png" alt=""><figcaption></figcaption></figure>

***

## Main Features

### 1. Enable Moderation Filter

* This setting allows you to filter out potentially harmful content, including hate speech, profanity, or inappropriate language. You can turn the moderation filter on or off using the toggle located at the top of the page. By default, this setting is enabled.

<figure><img src="../../.gitbook/assets/image (30).png" alt=""><figcaption></figcaption></figure>

{% hint style="warning" %}
Disabling the Moderation Filter makes some foundation models unavailable.
{% endhint %}

{% hint style="warning" %}
Features like **Narrative Design** and **Multilingual support** will not work when moderation is disabled.
{% endhint %}

***

### 2. Select Foundation Model

Choose from a variety of **Large Language Models (LLMs)** from leading providers:

* Anthropic
* Google
* LLaMA
* OpenAI

<figure><img src="../../.gitbook/assets/image (31).png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
&#x20;Model availability depends on whether the Moderation Filter is enabled.
{% endhint %}

***

### 3. Temperature Control

<figure><img src="../../.gitbook/assets/image (32).png" alt=""><figcaption></figcaption></figure>

* **Function:** Adjusts the randomness and creativity in the AI’s responses.
* **Slider Range:** `0.0` (most deterministic) to `1.0` (most creative).

| Temperature Range    | Behavior                                   | Use Case                                       |
| -------------------- | ------------------------------------------ | ---------------------------------------------- |
| **Low (0.0–0.3)**    | Deterministic, consistent                  | Factual Q\&A, compliance-critical interactions |
| **Medium (0.4–0.7)** | Balanced accuracy and creativity           | Conversational agents, customer support        |
| **High (0.8–1.0)**   | Diverse, creative, sometimes unpredictable | Storytelling, brainstorming, roleplay          |

{% hint style="info" %}
Lower temperature sharpens the probability distribution for more predictable word choices.&#x20;

Higher temperature flattens the distribution, allowing less likely words to appear more frequently.
{% endhint %}

***

## Conclusion

The Core AI Settings give you precise control over your character’s foundation model, safety filters, and response style. By adjusting these parameters, you can create an AI that balances safety, reliability, and creativity to suit your specific application.
