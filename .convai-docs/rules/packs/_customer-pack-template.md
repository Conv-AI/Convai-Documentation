# Customer pack template

For documentation written for one named customer: an enterprise integration guide, a bespoke runbook,
an onboarding pack for a specific deployment.

These pages carry a risk the other pack types do not. They describe one customer's configuration, and
some of what they contain — the customer's name, their deployment details, their negotiated limits,
their unreleased use case — must not reach the public documentation site. The default assumption in
this pack is therefore reversed: **nothing here is public until a human says which destination it goes
to.**

Copy this file to `packs/customers/<customer>.md` and fill every section. Replace every `TODO:`.

For a Convai product surface, use `_topic-pack-template.md`. For an SDK or plugin, use
`_pack-template.md`.

---

## Destination and visibility

Fill this section first. Until it is filled, no page may be written against this pack.

- **Customer:** TODO: the customer name as it may appear in the document, or the code name to use
  instead if the real name must not appear.
- **Destination:** TODO: exactly where these pages live — which repository, which GitBook space, or
  which delivery format if they are not published to a GitBook space at all. Do not assume the public
  `Convai-Documentation` repository. If the destination is unknown, stop and ask; do not pick one.
- **Visibility:** TODO: public, customer-only, or internal.
- **Confidentiality:** TODO: whether an NDA or contract restricts the content, and what that restricts.
- **Approver:** TODO: the named person who approves publication. Not the writer.

If any of these five is unknown, the writer stops and asks. A guess here is a contract problem, not a
documentation problem.

## What this pack covers

- TODO: The customer's use case and integration, in one sentence.
- TODO: The Convai products involved. Reference the relevant SDK or topic pack by name rather than
  restating its rules here — this pack layers on top of them, it does not replace them.
- TODO: What is explicitly out of scope.

## Audience

- TODO: Who at the customer reads this: their developers, their operators, their end users.
- TODO: What they already know, and what they do not. A customer's operations team usually has no
  Convai product knowledge and no engine knowledge.
- TODO: Whether the reader has access to the Convai dashboard, and at what permission level.

## Customer-specific facts

Everything true for this customer and not true generally. Each row needs a source, because these facts
are the ones a writer cannot check anywhere else.

| Fact | Value | Verified against | Confirmed by |
|---|---|---|---|
| TODO | TODO | TODO | TODO |

Typical rows: the deployment region, negotiated rate limits, custom endpoints, SSO arrangement, agreed
character or experience names, contracted support path.

## Source of truth and verification

- **Owner:** TODO: the named Convai person who confirms this customer's setup. Usually the solutions
  engineer or account engineer, not the writer.
- **What counts as proof:** TODO: the signed statement of work, the deployment configuration, written
  confirmation from the owner, or a screenshot of the customer's actual environment.
- **What does not count:** a sales conversation, a plan that was discussed but not signed, a
  configuration that exists in staging but not in the customer's environment.

Never state a limit, SLA, price, region, or contractual term that is not written in the row above with
a source. If it is missing, stop and ask the approver.

## What must never appear

- TODO: Any other customer's name, data, configuration, or screenshot.
- TODO: Real credentials, API keys, tokens, endpoints with embedded secrets, or personal data.
- TODO: Internal Convai architecture, repository names, ticket links, or Slack references.
- TODO: Unreleased Convai features not covered by this customer's agreement.
- TODO: Pricing or commercial terms unless the approver has explicitly cleared them.

Screenshots taken from a customer environment need the same treatment: check for other customers' data,
personal information, and credentials before including one.

## Reuse rule

Prefer linking to the public documentation over restating it. A customer page that duplicates a public
page goes stale the moment the public page changes, and the customer then reads a wrong instruction.

Write customer-specific content here; link everything general.

## Structure

- TODO: The page set for this customer and the order a reader moves through it.
- TODO: Where the hub or entry point is.

## Gold-standard example pages

- TODO: The closest existing page to model, from any section. If this is the first customer pack, say
  so and name the public page whose structure fits best.
