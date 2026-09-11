---
title: Estimate credit usage for a project
description: Estimate how many credits your character uses per turn and per month with the Convai credit calculator, so you can choose a plan that fits.
---

Estimate what a project will use in credits before you choose a plan, with the credit calculator and a few numbers about how people will talk to your character. At the end, you have a cost per turn, a monthly total, and a plan that covers it.

## Before you start

* The language model and voice your character uses, and whether it uses long-term memory, a knowledge bank, or animation
* A typical conversation: how many turns it has, and roughly how long the end user and the character each speak per turn
* How many conversations you expect in a month

If you are new to credits, read [How Convai credits work](how-convai-credits-work.md) first. It explains each component the calculator lists.

## Estimate the cost of one turn

The credit calculator estimates one turn at a time, which it calls an interaction.

{% stepper %}
{% step %}
### Open the credit calculator

Go to the [credit calculator](https://credit-calculator.convai.com).
{% endstep %}

{% step %}
### Choose your character's services

Under **AI Brain**, select your character's language model in **AI Model**. Under **Senses**, select the speech recognition service in **Voice Input**. Under **Expression**, select the voice in **Voice Output** and the animation in **Animation**.
{% endstep %}

{% step %}
### Turn on memory and knowledge if you use them

Turn on **Memory** and **Knowledge** only if your character uses long-term memory or a knowledge bank. Each one adds to the cost of every turn.
{% endstep %}

{% step %}
### Describe a typical turn

Set **Prompt Size** to the number of tokens the language model reads per turn, and **Response Size** to the length of the character's reply in tokens. The calculator counts about four characters of text as one token.

Set the seconds next to **Voice Input** to how long the end user speaks, and the seconds next to **Voice Output** to how long the character speaks.

**Prompt Size** includes the character's instructions and the conversation so far, so base it on a turn from the middle of a typical conversation rather than the first one. For a reference point, the example in [How Convai credits work](how-convai-credits-work.md#example-one-spoken-reply) uses 4,000 input tokens.
{% endstep %}

{% step %}
### Read the cost per turn

The calculator shows the cost of each row next to it, adds the **Platform Fee**, and shows the total credits for one interaction. The row with the highest cost is where a different model or voice saves the most.
{% endstep %}
{% endstepper %}

{% hint style="info" %}
The calculator shows each turn's exact cost. Convai rounds each turn's total up to the next whole credit, so round the calculator's figure up before you multiply it.
{% endhint %}

## Estimate a month of usage

Multiply the credits per turn by the number of turns in a typical conversation, then by the number of conversations you expect in a month.

The following example uses the two configurations from [How Convai credits work](how-convai-credits-work.md), with 12 turns per conversation and a Professional plan's 99,000 monthly credits:

| Estimate | ElevenLabs Flash v2.5 voice | Convai TTS (managed) voice |
| --- | ---: | ---: |
| Credits per turn | 19 | 8 |
| Credits per 12-turn conversation | 228 | 96 |
| Conversations that 99,000 credits cover | 434 | 1,031 |

These figures cover turns only. Add the two charges the calculator leaves out:

* **Session duration.** Every connected session is charged for its whole length, including silent time. To measure it, hold one representative test conversation with your character in the Playground, then read its **Duration credits** on the **Credits** tab. Multiply that by the number of sessions you expect in a month.
* **File processing.** Processing an uploaded file, such as a knowledge bank document, is charged when the file is processed, not on every turn. It does not grow with the number of conversations.

## Choose a plan

Under **How Many Interactions Do You Get?**, the credit calculator shows how many interactions each plan covers at your cost per turn. Compare that with your monthly total, including session duration.

To see the plans available to your account, select your profile avatar in the top-right corner of the Playground, then select **Pricing**.

Leave headroom above your estimate. Unused credits expire at renewal, but running out stops a conversation immediately, and Convai does not support overages.

## Compare the estimate with real usage

Once your character is live, check the estimate against real sessions. In the Convai Playground, select **Project Settings** in the sidebar, open the **Credits** tab, and review the **Session Usage** panel. For each session, **Turn credits** and **Duration credits** show what it used.

If real usage is higher than your estimate, check **Prompt Size** first. Long character instructions and long conversations raise the input tokens on every turn.

## Next steps

{% content-ref url="credit-balance-and-billing-cycle.md" %}
[Credit balance and billing cycle](credit-balance-and-billing-cycle.md)
{% endcontent-ref %}

{% content-ref url="how-convai-credits-work.md" %}
[How Convai credits work](how-convai-credits-work.md)
{% endcontent-ref %}
