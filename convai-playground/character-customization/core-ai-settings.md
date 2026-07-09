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

* OpenAI
* Anthropic
* Google
* Llama

<figure><img src="../../.gitbook/assets/image (31).png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
Model availability depends on whether the Moderation Filter is enabled.
{% endhint %}

***

### Supported LLMs

Below is a list of Large Language Models (LLMs) available in the Convai Playground under **Core AI Settings**.\
Models marked as ✅ _Flagship_ are the providers’ top-tier, most capable models — but usage of these is subject to the **Flagship Interaction Cap** based on your plan.

> **Flagship LLMs**\
> This is the limit on the number of interactions you can perform using Flagship LLMs.
>
> **Example:**\
> In the _Indie Dev_ plan, you have a total monthly quota of **3000 Interactions**. However, the **Flagship LLM Interaction Cap** is **1500**.\
> If you use GPT-4.1 after 1500 interactions, your Flagship LLM quota will be exhausted.\
> You will then need to switch to a non-Flagship LLM for the remaining 1500 interactions.

***

### Realtime / Live Models

#### OpenAI

<table><thead><tr><th>Model</th><th>Model Code</th><th data-type="checkbox">Flagship</th></tr></thead><tbody><tr><td>GPT Realtime 1.5 (beta)</td><td>gpt-realtime-1.5</td><td>false</td></tr><tr><td>GPT Realtime Mini (beta)</td><td>gpt-realtime-mini</td><td>false</td></tr></tbody></table>

#### Google

<table><thead><tr><th>Model</th><th>Model Code</th><th data-type="checkbox">Flagship</th></tr></thead><tbody><tr><td>Gemini 2.5 Flash Live (beta)</td><td>gemini-2.5-flash-live</td><td>false</td></tr><tr><td>Gemma 4 34B Fast (beta)</td><td>gemma-4-34b-fast</td><td>false</td></tr><tr><td>Gemma 4 26B A4B Fast (beta)</td><td>gemma-4-26b-a4b-fast</td><td>false</td></tr></tbody></table>

### Standard Models

#### OpenAI

<table><thead><tr><th>Model</th><th>Model Code</th><th data-type="checkbox">Flagship</th></tr></thead><tbody><tr><td>GPT-5.4</td><td>gpt-5.4</td><td>false</td></tr><tr><td>GPT-5.x (latest)</td><td>gpt-5.x</td><td>true</td></tr><tr><td>GPT-OSS-120B (beta)</td><td>gpt-oss-120b</td><td>false</td></tr><tr><td>GPT-5.1 (beta)</td><td>gpt-5.1</td><td>false</td></tr><tr><td>GPT-4.1</td><td>gpt-4.1</td><td>false</td></tr><tr><td>GPT-5.4-nano</td><td>gpt-5.4-nano</td><td>false</td></tr><tr><td>GPT-5.x-nano (latest)</td><td>gpt-5.x-nano</td><td>true</td></tr><tr><td>GPT-5.4-mini</td><td>gpt-5.4-mini</td><td>false</td></tr><tr><td>GPT-5.x-mini (latest)</td><td>gpt-5.x-mini</td><td>true</td></tr><tr><td>GPT-4.1-mini</td><td>gpt-4.1-mini</td><td>false</td></tr><tr><td>GPT-5.3 Instant</td><td>gpt-5.3-instant</td><td>false</td></tr><tr><td>GPT-4o</td><td>gpt-4o</td><td>false</td></tr><tr><td>GPT-4.1-nano</td><td>gpt-4.1-nano</td><td>false</td></tr><tr><td>GPT-4o-mini</td><td>gpt-4o-mini</td><td>false</td></tr></tbody></table>

#### Anthropic

<table><thead><tr><th>Model</th><th>Model Code</th><th data-type="checkbox">Flagship</th></tr></thead><tbody><tr><td>Claude 4.5 Sonnet (beta)</td><td>claude-4-5-sonnet</td><td>false</td></tr><tr><td>Claude 4.5 Haiku (beta)</td><td>claude-4-5-haiku</td><td>false</td></tr><tr><td>Claude Sonnet (latest)</td><td>claude-sonnet</td><td>true</td></tr><tr><td>Claude Haiku (latest)</td><td>claude-haiku</td><td>true</td></tr></tbody></table>

#### Google

<table><thead><tr><th>Model</th><th>Model Code</th><th data-type="checkbox">Flagship</th></tr></thead><tbody><tr><td>Gemini 3.5 Flash</td><td>gemini-3.5-flash</td><td>false</td></tr><tr><td>Gemini Flash (latest)</td><td>gemini-flash</td><td>true</td></tr><tr><td>Gemini 3.1 Flash Lite</td><td>gemini-3.1-flash-lite</td><td>false</td></tr><tr><td>Gemini Flash Lite (latest)</td><td>gemini-flash-lite</td><td>true</td></tr><tr><td>Gemini 2.5 Flash</td><td>gemini-2.5-flash</td><td>false</td></tr><tr><td>Gemini 2.5 Flash Lite</td><td>gemini-2.5-flash-lite</td><td>false</td></tr></tbody></table>

#### Qwen

<table><thead><tr><th>Model</th><th>Model Code</th><th data-type="checkbox">Flagship</th></tr></thead><tbody><tr><td>Qwen3.6 27B (beta)</td><td>qwen3.6-27b</td><td>false</td></tr><tr><td>Qwen3.6 35B A3B (beta)</td><td>qwen3.6-35b-a3b</td><td>false</td></tr></tbody></table>

#### Llama

<table><thead><tr><th>Model</th><th>Model Code</th><th data-type="checkbox">Flagship</th></tr></thead><tbody><tr><td>Llama 4 Maverick (beta)</td><td>llama-4-maverick</td><td>false</td></tr><tr><td>Llama 4 Scout (beta)</td><td>llama-4-scout</td><td>false</td></tr><tr><td>Llama3 70B</td><td>llama3-70b</td><td>false</td></tr></tbody></table>

#### xAI

<table><thead><tr><th>Model</th><th>Model Code</th><th data-type="checkbox">Flagship</th></tr></thead><tbody><tr><td>Grok 4.3</td><td>grok-4.3</td><td>false</td></tr></tbody></table>

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
Lower temperature sharpens the probability distribution for more predictable word choices.

Higher temperature flattens the distribution, allowing less likely words to appear more frequently.
{% endhint %}

***

## Conclusion

The Core AI Settings give you precise control over your character’s foundation model, safety filters, and response style. By adjusting these parameters, you can create an AI that balances safety, reliability, and creativity to suit your specific application.
