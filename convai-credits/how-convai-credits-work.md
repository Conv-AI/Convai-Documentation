---
title: How Convai credits work
description: Understand what a Convai credit is worth, which parts of a conversation use credits, and how Convai calculates the charge for each turn.
---

Convai measures everything your characters use in a single unit: credits. Each turn of a conversation adds up the credits for the services it used, such as speech recognition, the language model, and the voice. Knowing how that total is built helps you choose a configuration that fits your budget.

## Why Convai uses credits

Credits put every service a character uses on one balance. A single spoken reply can use several services, and each one measures usage differently: speech recognition counts seconds of audio, a language model counts tokens, and a voice counts the length of the speech it produces. A token is a small piece of text that a language model reads or writes, often part of a word. Credits convert all of these units into one number, so you track one balance instead of a separate allowance for each service.

Your plan gives you credits for each billing cycle. The models, voices, and features you choose for a character decide how quickly those credits are spent.

## What a credit is worth

<code class="expression">space.vars.credits_per_dollar</code> credits are worth one US dollar. To convert a credit amount to dollars, divide it by <code class="expression">space.vars.credits_per_dollar</code>. A turn that costs 19 credits costs $0.019, a little under two cents.

A credit measures usage, not conversations. Two characters can use very different amounts of credits for the same conversation, depending on the model, voice, and features each one uses.

## What uses credits

Credits are used in three ways: by each turn of a conversation, by the time a session stays connected, and by processing files you upload.

### Turns

A turn is one message from an end user and the character's reply to it. The credit calculator calls a turn an interaction. A conversation is made of many turns.

Each turn is charged for the services it uses. The [credit calculator](https://credit-calculator.convai.com) names those services as follows:

| Component | What it covers | What is measured |
| --- | --- | --- |
| **Voice Input** | Speech recognition, which turns the end user's speech into text | Seconds of speech |
| **Prompt Size** | Everything the language model reads: the character's instructions, the conversation so far, and the new message | Input tokens |
| **AI Processing** | The language model writing the reply | Output tokens |
| **Voice Output** | Text-to-speech, which turns the reply into speech | Length of the generated speech |
| **Animation** | Lip sync and facial animation that follow the speech | Length of the animation |
| **Memory** | Saving and recalling long-term memory | Each use |
| **Knowledge** | Searching the character's knowledge bank | Each use |
| **Platform Fee** | Coordinating the services that produce the reply | <code class="expression">space.vars.platform_fee_credits</code> credits per turn |

The language model reads the character's instructions and the conversation so far on every turn, so longer instructions and longer conversations raise **Prompt Size** on each turn, not only on the first.

A turn is charged only for the components it uses. A text conversation has no **Voice Input** or **Voice Output** charge, and a character without long-term memory has no **Memory** charge.

### Session duration

A session is one continuous connection to a character, such as a voice conversation in the Playground or in your own application. While a session is connected, Convai charges for its duration in addition to the turns inside it. Duration counts the whole time the session is open, including time when nobody is speaking.

{% hint style="warning" %}
An open session uses credits even when it is silent. End a conversation when you are finished with it, rather than leaving it connected in the background.
{% endhint %}

The credit calculator does not include session duration. You can see the duration charge for each real session on the **Credits** tab; see [Credit balance and billing cycle](credit-balance-and-billing-cycle.md).

### File processing

Processing a file you upload, such as a document for a knowledge bank, uses credits. This is separate from the **Knowledge** charge on a turn, which covers searching the knowledge bank during a conversation. Uploaded files also count toward your plan's knowledge bank size limit, which is listed for each plan on the [Pricing](https://convai.com/pricing) page.

## How a turn's charge is calculated

Convai adds up the exact cost of every component a turn uses, including the **Platform Fee**, and then rounds the total up to the next whole credit. Rounding happens once, on the turn's total, and never on individual components. A component used for 2 seconds is charged for 2 seconds.

Because only the total is rounded, a turn never costs more than one credit above its exact cost. The credit calculator shows the exact cost before rounding, so a real turn can cost up to one credit more than the calculator shows.

## Example: one spoken reply

In this example, an end user speaks for 8 seconds. The language model reads 4,000 input tokens, which include the character's instructions and the conversation so far, and writes a 60-token reply. The character speaks the reply in 16 seconds. The charge for that turn breaks down as follows:

| Component | Service | Usage | Credits |
| --- | --- | --- | ---: |
| **Voice Input** | Soniox STT (streaming) | 8 seconds | 0.267 |
| **Prompt Size** | GPT-4o mini | 4,000 input tokens | 0.600 |
| **AI Processing** | GPT-4o mini | 60 output tokens | 0.036 |
| **Voice Output** | ElevenLabs Flash v2.5 | 16 seconds | 11.947 |
| **Platform Fee** | — | 1 turn | 6.000 |
| Total before rounding | | | 18.849 |
| **Charge for the turn** | | | **19** |

Component figures are rounded to three decimal places, so they add up to slightly more than the exact total. The figures use the credit calculator's rates in September 2026. Rates change, so use the calculator for current figures.

### The same turn with a different voice

The next table keeps everything the same except the voice, which changes from ElevenLabs Flash v2.5 to Convai TTS (managed):

| Component | Service | Usage | Credits |
| --- | --- | --- | ---: |
| **Voice Input** | Soniox STT (streaming) | 8 seconds | 0.267 |
| **Prompt Size** | GPT-4o mini | 4,000 input tokens | 0.600 |
| **AI Processing** | GPT-4o mini | 60 output tokens | 0.036 |
| **Voice Output** | Convai TTS (managed) | 16 seconds | 0.480 |
| **Platform Fee** | — | 1 turn | 6.000 |
| Total before rounding | | | 7.383 |
| **Charge for the turn** | | | **8** |

Changing only the voice lowers the turn from 19 credits to 8, because **Voice Output** was the largest component. That is specific to this configuration. With a much longer prompt, a larger language model, or animation turned on, a different component can dominate the total.

## Related pages

Credits leave your balance at every turn, so the next thing to understand is how that balance behaves across a billing cycle and what happens when it reaches zero.

{% content-ref url="credit-balance-and-billing-cycle.md" %}
[Credit balance and billing cycle](credit-balance-and-billing-cycle.md)
{% endcontent-ref %}

{% content-ref url="estimate-credit-usage.md" %}
[Estimate credit usage for a project](estimate-credit-usage.md)
{% endcontent-ref %}
