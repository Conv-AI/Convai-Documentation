---
description: Explore how Convai's new credit based usage and billing system works.
---

# Convai Credits: How Usage and Billing Work

Convai is moving to a single, unified way of measuring what you use: **credits**. One balance brings together the usage of the models, voices and services that power your characters.

Your configuration and usage determine how quickly that balance is spent. Conversation turns, connected sessions and file processing each contribute to the total.

This guide explains how the charges work, how to estimate a project, and what happens to your balance throughout a billing cycle.

### Why credits <a href="#why-credits" id="why-credits"></a>

A Convai character is rarely just one service. A single spoken reply might use speech recognition, a language model, a voice, lip-sync animation, long-term memory and a knowledge base. Those services measure usage differently: seconds of audio, tokens, characters, frames or queries.

Credits give those different units a common measure. Instead of managing separate service quotas, you can track one balance and see which components contribute to your spending.

**Every plan can use any supported model, voice and metered capability.** Your plan provides the credits; you choose the components that fit your application and budget. Request-rate limits still apply—a credit balance does not remove those limits.

### What a credit is worth <a href="#what-a-credit-is-worth" id="what-a-credit-is-worth"></a>

The conversion is simple: **1000 credits = $1.**

Every dollar of plan value gives you 1,000 credits. A charge of 18 credits is therefore $0.018, or 1.8 cents. Divide a credit amount by 1,000 to express it in dollars.

A credit is a unit of usage, not a fixed number of conversations. Different configurations can use different amounts of credits for the same interaction.

### What spends credits <a href="#what-spends-credits" id="what-spends-credits"></a>

There are three categories to include in your budget: **conversation turns, session infrastructure, and file processing**.

#### Conversation turns <a href="#conversation-turns" id="conversation-turns"></a>

For the examples in this guide, a **turn** means one user input and one character response. A conversation can contain many turns.

The turn's charge combines the billable usage of the components involved in processing the input and producing the response.

| Component                                                     | What is measured                                   |
| ------------------------------------------------------------- | -------------------------------------------------- |
| **Hearing the user** — speech recognition                     | Seconds of input audio                             |
| **Thinking** — the language model                             | Input and output tokens, at their respective rates |
| **Speaking** — text-to-speech generation                      | Characters of text used for speech generation      |
| **Moving** — lip sync and facial animation                    | Frames                                             |
| **Remembering** — long-term memory                            | Save and retrieval operations                      |
| **Looking things up** — knowledge base                        | Queries                                            |
| **Orchestration** — the base server coordinating the response | One orchestration charge per turn                  |

A token is a unit of text processed by a language model; it is not the same as a word. Model input can include character instructions, conversation history and other context, as well as the user's latest message. The total input token count therefore reflects the full context sent to the model, not just the user’s latest message.

A turn only includes the components it uses. A text-only interaction does not incur speech-recognition or voice-generation charges; an interaction without long-term memory does not incur memory-operation charges. The turn is one combined charge, not a flat fee that makes every component cost the same.

#### Session infrastructure <a href="#session-infrastructure" id="session-infrastructure"></a>

A live voice or streaming session also uses connection and server infrastructure. This is charged separately from the components used to produce each reply.

The session charge is based on how long the session remains open, including time spent listening, speaking or sitting idle. **A silent session can still consume credits.** When estimating a conversation, include the full connected duration—not just the time someone is speaking.

#### File processing <a href="#file-processing" id="file-processing"></a>

Processing uploaded documents and assets consumes credits through a one-time processing charge. These charges are separate from knowledge-base queries during a turn. Stored content counts toward your plan's knowledge-base or asset size limit; the section below explains how those limits work.

### How a turn's charge is calculated <a href="#how-a-turns-charge-is-calculated" id="how-a-turns-charge-is-calculated"></a>

**You pay for the components your turn uses, based on how much of each you consume.** Each component is charged at its applicable rate, with no minimum usage threshold—for example, two seconds of audio are charged as two seconds. Components you do not use do not contribute to the charge: a text-only interaction has no speech-recognition or voice-generation cost, and a turn without long-term memory has no memory-operation cost.

These component costs, including orchestration, are combined into a single turn charge, with the final total rounded up once to a whole credit.

You can refer to the following credit calculator for checking out the prices for different configurations : [click here](http://credit-calculator.convai.com/).

### A worked example: the components of one spoken reply <a href="#a-worked-example-the-components-of-one-spoken-reply" id="a-worked-example-the-components-of-one-spoken-reply"></a>

A player speaks for 8 seconds. The character processes 4000 input tokens, generates a 60-token reply, and uses 240 characters for speech generation.

The 4000 input tokens represent the full model input in this example, including instructions and context—not just the player's 8 seconds of speech. The token and character counts are example usage measurements, not a fixed conversion between the two units.

| Component                                 | Usage                                       | Rate                      | Component cost in credits |
| ----------------------------------------- | ------------------------------------------- | ------------------------- | ------------------------- |
| Speech recognition — Soniox STT           | 8 seconds                                   | 0.0333 credits/ second    | 0.27                      |
| Model input — GPT-4o mini                 | 4000 tokens                                 | 0.00015 credits/token     | 0.60                      |
| Model output — GPT-4o mini                | 60 tokens                                   | 0.0006 credits/token      | 0.04                      |
| Speech generation — ElevenLabs Flash v2.5 | 240 characters (assuming 4 chars per token) | 0.04978 credits/character | 11.95                     |
| Base server                               | 1 turn                                      | 6 credits / turn          | 6.00                      |
| **Turn total, before rounding**           |                                             |                           | 18.86                     |
| **Final turn charge, rounded up once**    |                                             |                           | 19                        |

Using the retained rates, the speech and model components total **18.86 credits**. The complete turn charge includes the base-server cost as well; it is rounded only after all components have been added.

This example does not use animation, memory, session infrastructure or knowledge-base operations.

#### The same usage with a Convai Voice <a href="#the-same-usage-with-a-convai-voice" id="the-same-usage-with-a-convai-voice"></a>

Now replace ElevenLabs Flash v2.5 with a **Convai Voice** while keeping the other example inputs unchanged, including the base server charge.

| Component                              | Usage                                       | Rate                    | Component cost in credits |
| -------------------------------------- | ------------------------------------------- | ----------------------- | ------------------------- |
| Speech recognition — Soniox STT        | 8 seconds                                   | 0.0333 credits/ second  | 0.27                      |
| Model input — GPT-4o mini              | 4000 tokens                                 | 0.00015 credits/token   | 0.60                      |
| Model output — GPT-4o mini             | 60 tokens                                   | 0.0006 credits/token    | 0.04                      |
| Speech generation — Convai Voice       | 240 characters (assuming 4 chars per token) | 0.002 credits/character | 0.48                      |
| Base server                            | 1 turn                                      | 6 credits / turn        | 6.00                      |
| **Turn total, before rounding**        |                                             |                         | 7.39                      |
| **Final turn charge, rounded up once** |                                             |                         | 8                         |

The retained speech-recognition and model costs total **0.91 credits**, before adding voice generation and base server. The Convai Voice costs 0.48 credits for 240 characters, leading to a total turn cost of 8 credits.

In this example, changing the voice has the largest effect on the overall turn cost. That will not be true of every application: a larger model input, a different language model, animation or additional retrieval operations can change the balance.

Both examples include the same per-turn orchestration component and exclude animation, memory and knowledge-base operations. Session infrastructure and file processing remain separate from the turn charge.

### What a month can look like <a href="#what-a-month-can-look-like" id="what-a-month-can-look-like"></a>

Once you have the complete charge for your configuration, the budgeting calculation is straightforward:

**Conversation credits = the sum of its turn charges + its session-infrastructure charge.**

Consider a five-minute conversation with twelve turns. To illustrate the budgeting method, suppose one complete configuration costs **19 credits per turn**, and another costs **8 credits per turn**, with the base server cost already included in both figures.

At the example session rate of **0.0133 credits per second**, five minutes produces:

**300 seconds × 0.0133 credits/second = 3.99 \~ 4 credits.**

The table below treats that accumulated session amount as one charge rounded upward to **4 credits**. This states the rounding assumption used in the example; it does not imply that each second is rounded separately.

| Item                                                       | Configuration costing 19 credits/turn | Configuration costing 8 credits/turn |
| ---------------------------------------------------------- | ------------------------------------- | ------------------------------------ |
| Twelve turns, including orchestration                      | 12 × 19 = 228 credits                 | 12 × 8 = 96 credits                  |
| Five-minute session, using the example rounding assumption | 4 credits                             | 4 credits                            |
| **One five-minute conversation**                           | **232 credits ($0.232)**              | **100 credits ($0.1)**               |
| **Complete conversations within 99,000 credits**           | **426**                               | **990**                              |

These are illustrative workloads, not a guarantee of how many conversations a plan will support. The calculation assumes the full 99,000-credit budget is available for these conversations, with no other account usage or file-processing charges.

Actual turns can differ within a conversation. Longer replies, larger prompts, additional operations and longer connected sessions all affect the result. Use your complete configuration and representative usage when estimating a project.

### Your balance through the billing cycle <a href="#your-balance-through-the-billing-cycle" id="your-balance-through-the-billing-cycle"></a>

Your **billing cycle** is your subscription's period—monthly, quarterly or annual—running from your own start date rather than the start of a calendar month.

Plan credits are granted at the beginning of that cycle. An annual plan grants the full year's credits up front rather than a monthly slice, allowing a busy month and a quieter month to balance out within the year.

**Unused credits expire at the end of the cycle.** They do not carry over into the next one.

#### Notifications and exhausted balances <a href="#notifications-and-exhausted-balances" id="notifications-and-exhausted-balances"></a>

You receive an email when usage reaches **80%, 95% and 100%** of the cycle's credits. The first two are advance warnings; the 100% notification indicates that the balance has been exhausted.

When exhaustion is detected, services stop. A reply in progress may be interrupted. Because usage recording and enforcement are not instantaneous, a busy conversation can briefly take the balance below zero.

Receiving the next cycle's allocation restores credit access. Running out of credits does not itself delete or reset your data. Restored access should not be read as a promise that an interrupted reply automatically resumes; check your application's connection before restarting the interaction.

#### Negative balances and overages <a href="#negative-balances-and-overages" id="negative-balances-and-overages"></a>

**We do not currently support credit overages.** Services stop when credit exhaustion is detected, rather than continuing with additional usage charges. Any temporary negative balance is cleared at the end of the cycle without an additional charge.

### Knowledge bases, assets and storage <a href="#knowledge-bases-assets-and-storage" id="knowledge-bases-assets-and-storage"></a>

Each plan includes **separate size limits for your knowledge base and assets**. Uploaded files count toward the corresponding limit.

**A one-time processing charge applies when uploaded files are processed.** This charge does not recur in subsequent billing cycles.

**Deleting files restores the available size quota** by freeing the space those files occupied, allowing you to upload more content within the same plan limits.

File-processing charges are separate from knowledge-base queries during a turn. When planning your usage, account for processing and query costs, and ensure your content stays within your plan's size limits.

### Common questions <a href="#common-questions" id="common-questions"></a>

<details>

<summary>I have a paid plan. How will it be migrated to the new credit system?</summary>

When your account moves to credits, the value of the **time remaining in your current subscription period** is converted into a credit balance at the same 1,000-credits-per-dollar rate.

The calculation is:

**Migration credits = plan value for the current period × remaining fraction of that period × 1,000.**

For example, halfway through a $99 monthly subscription period, the remaining $49.50 becomes **49,500 credits**.

This is time-based proration. It does not depend on how many interactions you have already used, and it is not a one-for-one conversion of an unused interaction quota. The number of conversations those credits support depends on your chosen components and actual usage.

**Your renewal date does not change.** Your next payment starts a fresh cycle with the full credit allocation for your plan. There is nothing you need to do to initiate the conversion.

</details>

<details>

<summary>Can I use a premium model on a lower-priced plan?</summary>

Yes. Every plan can use the supported models, voices and metered capabilities. You need enough credits for the usage, and any applicable request-rate limits still apply.

</details>

<details>

<summary>Why did a very short interaction still cost 1 credit?</summary>

The complete turn charge is rounded upward to a whole credit. A positive combined cost below 1 credit therefore becomes 1 credit. There are no separate minimum usage thresholds for its individual components.

</details>

<details>

<summary>Can an idle session still use credits?</summary>

Yes. Session infrastructure is charged while the session remains open, including silent periods. This is separate from the component usage of individual replies.

</details>

<details>

<summary>Can I see where my credits went?</summary>

Yes. Usage is broken down by day and by component so you can see which models, voices and features contribute most to your spending.

</details>

<details>

<summary>How do I estimate a project before building it?</summary>

Use the [credit calculator](https://credit-calculator.convai.com/) to choose your models, voices and features, then enter a representative conversation length and expected volume. Include the complete model input, reply length, orchestration, connected-session duration and any optional services. Budget for file processing separately, and check your plan's knowledge-base and asset size limits.

Start with an estimate, then compare it with representative actual usage before setting your production budget.

</details>
