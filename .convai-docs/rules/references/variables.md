# GitBook variables

Use GitBook variables for values that appear across multiple pages and must stay synchronized: SDK
version numbers, minimum platform or engine version, package URLs, API endpoint base URLs. Never
hard-code such a value as plain text (CV-24). The variables each subject uses are in the
documentation repository's `.gitbook/vars.yaml`.

## How they work with Git Sync

1. **Define** the value in `.gitbook/vars.yaml`, committed to the repository:

```yaml
unity_sdk_version: 4.2.0
unity_min_version: "2023.1 or later"
sdk_package_id: com.convai.convai-sdk-for-unity
dashboard_url: https://convai.com
```

2. **Reference** it inline in Markdown with GitBook's expression syntax, as literal HTML exactly as
   written:

```html
<code class="expression">space.vars.unity_sdk_version</code>
```

3. **GitBook renders** the expression as the value from `vars.yaml` at publish time: the repository
   stores the expression, readers see the value. Do **not** use `{{ unity_sdk_version }}` or
   `{{ space.vars.unity_sdk_version }}`: GitBook does not render either, and they appear as raw text
   on the published page.

**Update flow** (for example a new SDK release): change the value in `.gitbook/vars.yaml` and publish
it like any other change, as a pull request against the base branch. Once it merges, GitBook syncs,
and every page using that expression updates automatically.

## Scope

| Scope | Definition | Reference syntax | Availability |
|---|---|---|---|
| Space-level | `.gitbook/vars.yaml` in the repo | `space.vars.variable_name` | Every page in the space |
| Page-level | `vars:` block in page frontmatter | `page.vars.variable_name` | That page only |

Use `space.vars` for values shared across pages, and `page.vars` for a value specific to one page:

```yaml
---
title: Configure lip sync
vars:
  component_name: ConvaiLipSync
---
```

Referenced as `<code class="expression">page.vars.component_name</code>` within that page.

## Rules

- Define `space.vars` in `.gitbook/vars.yaml` before referencing them in any page.
- Name variables in `snake_case`, lowercase English.
- Use `space.vars` only for values that must be byte-for-byte identical wherever they appear. If a
  value varies by context, use a conditional content block instead.
- Do not use the expression syntax for values that differ across content variants: a variable resolves
  to the same value in every variant.
- A historical version on a migration page ("retired in 4.2.0") is a frozen fact and stays a literal
  (CV-24).
