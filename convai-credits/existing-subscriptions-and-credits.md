---
title: How existing subscriptions move to credits
description: Find out how Convai converts a paid subscription to a credit balance, how many credits you receive, and why your renewal date stays the same.
---

If you had a paid Convai subscription before credits, Convai converts it to a credit balance for you. You do not need to do anything, and your renewal date does not change.

## How many credits you receive

You receive credits for the time left in your current billing period. Convai works out what share of the period remains and gives you that share of your plan's credits. The result is the unused value of your period converted at <code class="expression">space.vars.credits_per_dollar</code> credits per dollar.

For example, a monthly Professional plan costs $99 and provides 99,000 credits. If your account moves to credits halfway through the month, half the period remains, and you receive 49,500 credits: the value of the remaining $49.50.

The same rule applies to quarterly and annual subscriptions. You receive the share of the period's credits that matches the time remaining.

The conversion depends only on time. Before credits, plans counted usage in interactions, and the conversion does not look at how many of those you used.

## What happens at renewal

Your renewal date stays the same. When your subscription renews, a full cycle starts with your plan's complete credit allocation. From then on, your balance works the same as any other credit plan.

## Related pages

{% content-ref url="credit-balance-and-billing-cycle.md" %}
[Credit balance and billing cycle](credit-balance-and-billing-cycle.md)
{% endcontent-ref %}

{% content-ref url="how-convai-credits-work.md" %}
[How Convai credits work](how-convai-credits-work.md)
{% endcontent-ref %}
