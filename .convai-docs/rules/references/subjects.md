# Subject files

A subject is one thing the documentation covers: an SDK, a product, or one customer's deployment.
Each has one file, `subjects/<name>.json` in the plugin, holding only what code cannot answer and where
to look for the rest. Everything the source can say (component names, modules, tab labels, routes) is
read from the source by the file's recipes each time the subject is used, and never written down.

`tools/subjects.py validate` checks every file against this schema, and every tool that reads a subject
validates it first, so a broken file stops the run instead of being half read.

## Keys

| Key | Holds | Required |
| --- | --- | --- |
| `name` | The subject id, the same as the file name: lowercase letters, digits and hyphens | Yes |
| `kind` | `sdk` (claims settled against source), `product` (against the product or its owner) or `customer` | Yes |
| `product_name` | The exact product name pages use | Yes; null only with a reason (below) |
| `short_name` | The allowed short form after first mention, such as "the Playground" | Yes; may be null |
| `audience` | Who the pages are for, in one sentence | Yes; null only with a reason (below) |
| `docs_paths` | Folders in the documentation repository that hold this subject's pages; the first is its section | Yes; may be empty |
| `sources` | Repositories to read: `owner`, `repo`, optional `ref` (branch; default the repository's), `root` (the package folder recipes are relative to) and `why`. Recipes run against the first; any further source is read by a person | Yes; empty for a subject with no source |
| `extract` | How the source is read (below) | Yes |
| `terminology` | Preferred terms: each `{"use": ..., "reject": [...], "why": ...}`; `reject` is optional | Yes; may be empty |
| `must_exist` | Names whose disappearance from the source is an error | Yes; needs a source |
| `must_not_exist` | Names whose appearance, in the source or on any page, is an error | Yes |
| `decisions` | Business decisions code cannot settle: each `{"decision", "date", "by"}`, plus `about` when the decision explains a null field | Yes; may be empty |
| `evidence` | `owner` (a name, or null when nobody is named), `proof` (what counts as proof), `source_does_not_settle`, `open_questions` | Required when `sources` is empty |
| `capture` | Screenshot capture for this subject's pages: the product's address, the fixture account rule, masks, the POST calls that only read, and the source globs behind each captured surface. Described in `references/capture.md`, validated by `tools/shots.py` | No; its `surfaces` need a source |

Any key may have a sibling `<key>_why` holding the reason for its value. Any other key is an error.

### Null fields

`product_name` and `audience` may be null only when the file says why: a decision whose `about` is that
key, or an `evidence.open_questions` entry starting with that key and a colon
(`"audience: who are these pages for?"`). An unknown fact stays a listed question; it is never a guess.

### Decisions

`date` is `YYYY-MM-DD` and `by` names who decided. A decision carried over from 2.x whose date and
decider were never recorded keeps the date of the last 2.x review that stated it, and `by` says the
decider was not recorded.

### Terminology

Every variant in a `reject` list is a banned word on the subject's pages when the linter runs with
`check_page.py --subject <name>`. Keep variants specific: a reject list matches whole words anywhere in
prose, so a common word rejects legitimate sentences too.

## `extract`

| Key | Holds |
| --- | --- |
| `recipes` | `{name: recipe}`. Required when the subject has a source |
| `version` | `{"file", "field"}`: where the source records its version, plus `docs_var`, the `vars.yaml` variable that states the documented version. With `docs_var`, the release watch compares the two and runs `release` when the source is newer. `paused`, `{"why": ...}`, stops that: the watch shows the subject as a `paused` row with the reason, never due and never needing a person, until the key is removed |
| `documented_sets` | Recipes whose every member the documentation must mention (a missing module is a gap) |
| `coverage_sets` | Recipes reported as one coverage ratio |
| `symbol_prefixes` | Prefixes that mark a name on a page as one of this subject's symbols |
| `coverage_ignore_prefixes` | Prefixes of names pages use that are deliberately outside the surface |
| `historical_pages` | Page globs whose job is to name what changed, where a retired name is correct |
| `release_skip` | Recipes a release does not compare, with a `release_skip_why`. A release compares every other recipe's set. Each entry must be a recipe, and none may be in `documented_sets` or `coverage_sets` |
| `interface_map` | For a product screen: `tabs` (the recipe holding the tab records), `docs_url`, and `explicit_pages`, one validated entry per tab no rule in `tools/interface_map.py` can match |

A recipe has exactly one of `glob` (with `**` for any depth, and a trailing `/` for folders) or `file`,
a `capture`, the keys its capture needs, and a `why` naming the claim it settles. The captures are
listed in `tools/extract_surface.py`. `name_pattern` narrows any capture to names matching a regular
expression.

`match` says how coverage finds the recipe's names on a page: `identifier` (a code symbol in
backticks), `code` (the exact name in backticks, any shape), `phrase` (the name as written, whole
words, in prose, headings or code) or `route` (an HTTP route's path, with or without a host). An
`http_route` recipe defaults to `route` and a `key_value_string` recipe to `phrase`; give `match`
only when the names are written another way than their capture suggests, such as platform names
read with `json_field`.

**Every recipe must find something.** A recipe that matches nothing is an error wherever the subject
is used: in `extract_surface.py`, in `check subjects`, and in the weekly job. A stale path cannot stay
silent.

## The surface

The names the recipes find are the subject's surface. It is generated on demand and cached at
`~/.convai-docs/cache/surfaces/<name>@<commit>.json`, reused only for the same commit and the same
recipes, and never committed.

For the `ts_export`, `csharp_type`, `attributed_type` and `python_class` captures, the surface also
records each captured type's public members (methods, properties, options, fields) under `members`,
so a release sees a renamed method or a new option on a type whose own name did not change. No
recipe may be named `members`. C++ members are not read yet.

## A subject with no file

`tools/new_subject.py <name> --docs <documentation-repo>` creates one without asking anything: docs
paths from folder names that carry the subject's words (or `--docs-path`), `product_name` and
`audience` from the first docs path's `README.md`, and, with `--repo` or `--source`, recipes proposed
for the source's language, keeping only those that find something. What it cannot read becomes an open
question. The file goes to `~/.convai-docs/cache/subjects/`, where every tool finds it by name for the
current run, and `--propose` opens a draft pull request adding it to the tooling repository on branch
`subjects/<name>`.

## Example pages

`tools/pick_example.py <name> --type <template> --docs <documentation-repo>` chooses the page a writer
imitates: under the subject's `docs_paths`, a page whose shape matches the template and that the linter
passes with no finding, the most recently committed first. With none, it is
`references/gold-standard-example.md`. Nobody keeps a list.

## Watching for drift

`.github/workflows/subject-drift.yml` runs `tools/check_subjects.py --issues` every Monday. For each
subject where a recipe matched nothing, a `must_exist` name is gone or a `must_not_exist` name has
appeared, it opens an issue, or comments on the open one, and never opens a pull request.

## Kept out of the public repository

The documentation repository is public, and a subject file describes private repositories. The bundle
`scripts/sync_agent_rules.py` copies there never includes `subjects/`.
