# SEO and accessibility

## SEO standards

| Item | Standard |
|---|---|
| Page title | Unique, specific, keyword-aware, sentence case. |
| Description | 120–160 characters target (hard max 200); one sentence; describes the outcome. |
| Slug | Lowercase, hyphenated, readable. |
| Lead paragraph | Uses the main topic naturally in the first sentence. |
| Headings | Descriptive and task/concept specific. |
| Internal links | Point to the source of truth for related tasks and concepts. |
| Canonical URL | For versioned docs (v1, v2, /latest): set canonical on all version pages pointing to the current `/latest` equivalent. Consolidates ranking signals and prevents outdated versions outranking current docs. |
| Hidden pages | Use intentionally for drafts, deprecated pages, duplicate pages, or private support content. |
| AI / GEO readiness | Well-structured docs with precise headings, factual prose, and no ambiguity rank better in LLM-based search (Perplexity, ChatGPT, Gemini). The heading and writing standards already satisfy this. |

## Accessibility standards

| Content | Standard |
|---|---|
| Headings | Semantic, ordered, and not skipped. |
| Links | Descriptive text. Never "click here." |
| Images | Meaningful alt text unless decorative. |
| Screenshots | Do not contain the only copy of essential instructions. |
| Tables | Clear headers. No layout tables. |
| Warnings | Written as text, not only embedded in images. |
| Code | Provided as selectable text with language labels. |
| Tabs | Do not hide critical warnings or prerequisites in one tab only. |

## Writing for AI readability

GitBook Assistant answers questions by reading your documentation. Poorly structured pages produce
hallucinated or evasive answers even when the correct information exists. To write pages the Assistant
answers correctly:

- Put the direct answer to the most likely reader question in the first sentence of the relevant
  section — not buried in the third paragraph.
- Use specific `##` headings that match how a reader would phrase a question: `Configure the API key`
  answers "how do I set my API key?"
- Avoid ambiguous pronoun references and vague section titles. The Assistant cannot resolve "it" or
  "this" across paragraphs.
- Quote exact console messages, field names, and component names in inline code — the Assistant
  matches these exactly.
- Keep one claim per sentence. Lists of tightly packed facts in a single sentence are harder to parse
  than short separate sentences.
