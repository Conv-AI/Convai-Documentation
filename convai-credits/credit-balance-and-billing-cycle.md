---
title: Credit balance and billing cycle
description: >-
  Understand when your plan's credits arrive and expire, which usage alerts
  Convai sends, and what happens when your credits run out mid-conversation.
---

# Credit balance and billing cycle

Your plan gives you a set number of credits at the start of each billing cycle, and every [turn](how-convai-credits-work.md#turns) and [session](how-convai-credits-work.md#session-duration) draws from that balance. Knowing when credits arrive, when they expire, and what happens at zero helps you keep a conversation from stopping unexpectedly.

### Where to see your balance

In the Convai Playground, select **Project Settings** in the sidebar, then open the **Credits** tab. The tab shows **Credits used** for the current cycle, the percentage of the cycle's credits you have used, and how many credits remain.

The **Session Usage** panel on the same tab lists your sessions by day. For each session, **Turn credits** shows the credits its turns used, and **Duration credits** shows the credits for the time it stayed connected.

### When you receive credits

Your billing cycle starts on the day your subscription started, not on the first day of a calendar month. At the start of each cycle, Convai gives you your plan's full credit allocation.

A cycle is always 1 month long, regardless of your subscription period. At every cycle renewal, your monthly credit allocation is added: an annual Professional plan receives 99,000 credits added each month, for a total of 1,188,000 credits across the year. Credits must be used within the cycle they're added — unused credits do not carry forward to the next cycle.

### When credits expire

Unused credits expire when the cycle renews. They do not carry over to the next cycle. Each renewal starts a fresh cycle with your plan's full monthly allocation, whatever was left from the previous one.

For example, if a Professional plan has 20,000 credits left when it renews, those 20,000 credits expire, and the next cycle starts with 99,000.

### Usage alerts

Convai emails you when your usage reaches 80%, 95% and 100% of the credits for your current cycle. The 80% and 95% emails are advance warnings. The 100% email means your credits are used up. Each alert is sent at most once per cycle.

### What happens when credits run out

When your credits are used up, Convai stops the character and ends the session. Convai checks your usage periodically while a conversation is running, so this can happen in the middle of a reply.

{% hint style="warning" %}
When your credits run out during a conversation, the character stops speaking immediately, even in the middle of a word, and the session disconnects. Act on the 80% and 95% alerts before a live demo or training session, so it is not cut off.
{% endhint %}

Convai decides whether a turn can start by looking at the credits you have left, but a turn's cost is known only once the turn is done. So the turn that uses your last credits can take your balance slightly below zero. For example, with 8 credits left, a turn that costs 10 credits can still start, and your balance becomes −2 credits. The overshoot is limited to that single turn. After it, your credits count as used up, and Convai refuses new turns and new sessions.

Your credits come back when your next billing cycle starts, or when you move to a plan with more credits.&#x20;

If you build your own application on the Live APIs, the server sends a `usage-limit-reached` message before it closes the session. See [Server-to-client messages](../api-reference/core-api-reference/live-apis-beta/server-to-client-messages.md#usage-limit-reached) for its fields.

### Get more credits

To get more credits within a cycle, move to a plan with a larger allocation. In the Playground, select your profile avatar in the top-right corner, then select **Pricing** to compare plans.

### Related pages

To avoid running out, estimate what your project uses before you choose a plan.

{% content-ref url="estimate-credit-usage.md" %}
[estimate-credit-usage.md](estimate-credit-usage.md)
{% endcontent-ref %}

{% content-ref url="how-convai-credits-work.md" %}
[how-convai-credits-work.md](how-convai-credits-work.md)
{% endcontent-ref %}

If you had a paid subscription before Convai moved to credits, see how it converts to a credit balance.

{% content-ref url="existing-subscriptions-and-credits.md" %}
[existing-subscriptions-and-credits.md](existing-subscriptions-and-credits.md)
{% endcontent-ref %}
