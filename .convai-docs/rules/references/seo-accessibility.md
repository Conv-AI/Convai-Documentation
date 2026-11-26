# SEO and accessibility

Search engines, GitBook Assistant and AI agents read the same page a person reads. Each standard
below is a numbered rule in `gitbook/styleguide.md`, so the linter, the reviewer and GitBook's agent
cite its id. The rule text lives there; this page says which rules make a page findable and readable.

## Findable

| Standard | Rule |
|---|---|
| The lead's first sentence and each section's first sentence answer the question the title or heading asks | CV-88 |
| One reader question per page, the one the title names | CV-89 |
| An SDK page states the SDK version it applies to | CV-90 |
| The title is specific, keyword-first and at most 60 characters | CV-33 |
| The title is unique within its space | CV-91 |
| The description is one outcome sentence of 120 to 160 characters | CV-34 |
| Headings are specific, with no vague or generic ones | CV-27, CV-28 |
| Product names and UI labels are spelled as the product spells them | CV-12 |
| Field, component and console-message names are inline code, so they match exactly | CV-18 |
| One claim per sentence | CV-8 |
| A hidden page still has a title, a description and an owner | CV-75 |
| No `noIndex` on a hub or section index page | CV-77 |

Three practices have no rule id, because they need judgement: phrase `##` headings as the reader's
question, and keep "it" and "this" from reaching across paragraphs (both in `writing-standards.md`),
and keep a warning that holds for every tab outside the tabs (`gitbook-blocks.md`).

A slug is lowercase, hyphenated and readable (`structure.md`, "File naming and location").
For versioned docs (v1, v2, /latest), set the canonical URL of every version page to the current
`/latest` page, so an outdated version does not outrank the current one.

## Readable

| Standard | Rule |
|---|---|
| Headings are in order and no level is skipped | CV-31 |
| Link text names the destination; never "click here" | CV-20 |
| Every image has alt text that describes what it shows | CV-48, CV-79 |
| Essential information, warnings included, is never only inside an image | CV-59 |
| Code, logs and configuration are text in a code block with a language, never a screenshot | CV-22, CV-47 |
| Tables carry tabular data, with real headers | CV-44 |
| Prerequisites and warnings are never hidden in an expandable section | CV-41 |
| Meaning is never carried by colour, position or direction alone | CV-58 |
