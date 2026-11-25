# Page types

Which template a page starts from, and what to read before writing it. A template's opening comment
holds the rules of its page type; `diataxis.md` explains the modes.

Every page reads `writing-standards.md`, `page-structure.md`, and its template. A new page also reads
`structure.md`, to place it. Then read the row's other files and nothing else: the linter and the
reviewer check every page against `linter-rules.md` and `quality-checklist.md`.

| The reader wants to | Template | Mode | Also read |
|---|---|---|---|
| Follow a task step by step | `how-to.md` | how-to | `gitbook-blocks.md`, `variables.md` |
| Do one task on a product screen, such as a Playground tab | `interface-task.md` | how-to | `gitbook-blocks.md`, `image-markup.md` |
| Learn it for the first time, end to end | `tutorial.md` | tutorial | `gitbook-blocks.md`, `variables.md` |
| Look up exact details of a class, component, or setting | `reference.md` | reference | `gitbook-blocks.md`, `variables.md` |
| Look up every field on one panel of a product screen | `field-reference.md` | reference | `gitbook-blocks.md`, `image-markup.md` |
| Find their way around one product screen | `interface-tour.md` | reference | `gitbook-blocks.md`, `image-markup.md` |
| Look up one REST or realtime endpoint | `api-endpoint.md` | reference | `gitbook-blocks.md`, `variables.md` |
| See what changed in a release | `release-notes.md` | reference | `gitbook-blocks.md`, `variables.md` |
| Understand how or why it works | `explanation.md` | explanation | `gitbook-blocks.md` |
| Know what a term means | `glossary.md` | explanation | `gitbook-blocks.md` |
| Fix an error they are hitting | `troubleshooting.md` | how-to | `gitbook-blocks.md`, `variables.md` |
| Move a project between versions | `migration.md` | how-to | `gitbook-blocks.md`, `variables.md` |
| Find their way to other pages | `hub.md` | — | `gitbook-blocks.md`, `gitbook-blocks-navigation.md` |
| Get answers to scattered one-off questions | `faq.md` | — | `gitbook-blocks.md` |

Also read `gitbook-blocks-more.md` for a task list, snippet, conditional content, file, or embed;
`gitbook-blocks-navigation.md` for cards or columns; `variables.md` when the page states a version or
URL; `images.md` and `image-markup.md` when an SDK page needs an image.

Reach for `faq.md` last: anything a reader searches for by task name belongs on a real page. A request
that covers more than one row is more than one page: recommend the split and write one at a time. Never
mix modes on one page (CV-36).
