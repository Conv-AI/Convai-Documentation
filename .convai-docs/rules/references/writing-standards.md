# Writing standards

Voice, tone, terminology, GitBook variables, version tracking, and deprecation. SDK-specific product
names, backend phrasing, and the list of synchronized variables come from the SDK pack.

## Voice and tone

- Write directly and concretely.
- Use second person for tasks: "Add your API key."
- In tutorials, use collaborative first-person plural: "We will add the component" rather than "You
  will learn how to add." This reflects that the tutorial guides the reader through a shared activity,
  not a lesson.
- Use active voice and present tense.
- Prefer short sentences. Keep one claim per sentence.
- Explain first-use terms or link to concept pages.
- Use American English spelling.
- Format class names, methods, fields, file paths, asset paths, package names, console messages, and
  literal values as `inline code`.

### Terminology

Product naming and backend phrasing are SDK-specific — always take them from the SDK pack. The
cross-SDK rule: refer to Convai's backend as "Convai" (for example "streams audio to Convai", "Convai
responds", "sent to Convai"). Do not write "Convai cloud", "cloud backend", "cloud pipeline",
"Convai's servers", or "cloud-powered".

### Avoid

- Marketing language: "powerful", "seamless", "robust", "cutting-edge".
- Setup promises: "up and running in minutes", "just one API key".
- Filler: "In this guide, we will explore...".
- Hedging: "you may want to", "you could try".
- Dismissive words: "simply", "just", "easy".
- Vague labels: "Overview", "More information", "Miscellaneous".
- "Click here" links.
- "Cloud", "cloud AI", "cloud backend", "cloud pipeline", "cloud-powered", "Convai's servers", or
  "Convai's cloud".

### Task wording

| Weak | Better |
|---|---|
| `API key setup` | `Configure the API key` |
| `Using the component` | `Add the component to a character` |
| `Step 1` | `Open Package Manager` |
| `More information` | `Next steps` or the exact related topic |
| `Common issues` | `Troubleshoot microphone input` |

## GitBook variables

Use GitBook variables for values that appear across multiple pages and must stay synchronized: SDK
version numbers, minimum platform/engine version, package URLs, API endpoint base URLs.

### How GitBook variables work (Git Sync workflow)

1. **Define** in `.gitbook/vars.yaml`, committed to the repository:

```yaml
unity_sdk_version: 4.2.0
unity_min_version: "2023.1 or later"
sdk_package_id: com.convai.convai-sdk-for-unity
dashboard_url: https://convai.com
```

2. **Reference** inline in Markdown using GitBook's expression syntax:

```html
<code class="expression">space.vars.unity_sdk_version</code>
```

   This is **literal HTML** that appears in your Markdown file exactly as written. GitBook renders
   the expression as the resolved value at publish time. The Git repository stores the raw HTML;
   readers see the value. Do **not** use `{{ unity_sdk_version }}` or
   `{{ space.vars.unity_sdk_version }}` — those syntaxes are not rendered by GitBook and will appear
   as raw text on the published page.

3. **GitBook renders** the expression as the value from `vars.yaml` at publish time. The repository
   stores the expression syntax; the published site shows the resolved value.

**Update flow** (for example a new SDK release): change the value in `.gitbook/vars.yaml`, commit and
push to `staging`, and GitBook syncs — every page using that expression updates automatically.

### Variable scope

| Scope | Definition | Reference syntax | Availability |
|---|---|---|---|
| Space-level | `.gitbook/vars.yaml` in the repo | `space.vars.variable_name` | Every page in the Space |
| Page-level | `vars:` block in page frontmatter | `page.vars.variable_name` | That page only |

Use `space.vars` for values shared across pages. Use `page.vars` for values specific to a single page:

```yaml
---
title: Configure lip sync
vars:
  component_name: ConvaiLipSync
---
```

Referenced as `<code class="expression">page.vars.component_name</code>` within that page.

### Rules

- Define `space.vars` in `.gitbook/vars.yaml` before referencing them in any page.
- Name variables in `snake_case`, lowercase English.
- Use `space.vars` only for values that must be byte-for-byte identical wherever they appear. If a
  value varies by context, use a Conditional content block instead.
- Do not hard-code version numbers, package URLs, or other change-prone values in page body text when
  a space variable covers them.
- Do not use GitBook's expression syntax for values that differ across Content Variants — variables
  resolve the same value in every variant.

The set of variables available for each SDK is listed in that SDK's pack.

## Version tracking

For pages whose accuracy depends on a specific SDK or engine version, add a `last_reviewed` field to
the frontmatter:

```yaml
---
title: Configure lip sync
description: Configure blend-shape lip sync on a Convai character in Unity.
last_reviewed: "4.2.0"
---
```

Update `last_reviewed` whenever you verify the page against the current SDK version. Pages with a
`last_reviewed` version more than one major release behind the current SDK must be reviewed before the
next publish cycle.

## Deprecated content

When an API, component, or workflow is deprecated:

1. Add a `{% hint style="warning" %}` block at the top of the page stating what is deprecated, what
   replaces it, and from which SDK version.
2. Update all inbound links to point to the replacement page when one exists.
3. Keep the deprecated page for at least one major SDK version after deprecation.
4. Do not silently delete deprecated pages. Mark them first, then remove after the retention period.

```md
{% hint style="warning" %}
**Deprecated in SDK 4.0.** `ConvaiLegacyAudioManager` is replaced by `ConvaiAudioManager`. See [Configure audio](../guides/configure-audio.md).
{% endhint %}
```

## Examples

Every feature page should include examples unless the page is purely conceptual or a short reference
entry. Each example must include a scenario name, a one-sentence context, concrete setup (Inspector
configuration or code), and the expected runtime outcome. Recommended order: minimal working example,
common production-style example, optional advanced variation.

Primary domain: learning and training simulations. Use scenarios such as industrial safety drills,
medical training, military simulation, corporate onboarding, and procedural assessment. Secondary
domains are allowed when they fit the feature better; use the ordering "training simulations,
interactive experiences, and games" when describing broad applicability. Avoid "game-world"
terminology — use "in-scene" instead.
