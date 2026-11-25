# Safe publishing and AI-agent rules

Every change to the documentation, by a person or an agent, reaches readers through one pull request
that a person reviews and merges. The agent prepares the files, opens the pull request through
`steps/publish.md`, and stops.

## The pull-request workflow

1. The change is made on a branch of its own, `docs/<slug>`, cut from the base branch.
2. One pull request goes from that branch to the base branch. Its body says what changed, the subject
   and commit each claim was checked against, the result of each check, and every open question. A
   pull request with an open question is a draft.
3. The pull request runs the documentation checks (`.github/workflows/convai-docs.yml`: the page linter
   on the changed pages and the site check on the whole repository) and gets GitBook's pull-request
   preview, where the changed pages are read as they will render.
4. A person reads the preview, approves, and merges.

The base branch is `publish.base_branch` in `settings.json`, and every tool reads it from there. The
documentation owner switches it when the open change requests have landed; nothing in this workflow
or in any rule changes when that happens.

Nothing AI-generated goes live without a rendered preview and a person's approval (CV-62, CV-64). The pull request names
its source of truth and every assumption (CV-63).

`tools/publish.py` makes the git and `gh` calls for the plugin and refuses, in code, to push to `main`,
merge, force-push, or delete a branch it did not create. Until the documentation owner sets
`publish.enabled`, it prints those calls and makes none of them.

## Change requests in the GitBook editor

An edit made in GitBook's own editor instead of through Git Sync goes through a change request, the
editor's equivalent of a pull request, with the same review.

| Step | Action |
|---|---|
| Draft | Open a change request for the new or revised page. |
| Review | Assign a reviewer. The reviewer checks against the quality checklist. |
| Merge rules | Require at least one reviewer approval before a change request can be merged. |
| Merge | Merge only after the reviewer approves and the page passes the quality checklist. |

Configure merge rules in **Space settings → Merge rules**: require reviewer approval (on); prevent
self-merge (on); required checks: pass the quality checklist before requesting review.

For AI-generated content, the change request description lists the AI tool used, the source of truth
for technical claims, and any assumptions, and a person, not the agent, gives the final approval.

## Safe AI-agent editing rules

The agent **must**:

- Preserve existing documentation unless the task explicitly asks for a specific revision.
- Never delete pages, folders, images, or GitBook configuration files without explicit approval.
- Avoid renaming files or moving pages unless the task is a navigation or restructuring task. A moved
  or removed page carries a `.gitbook.yaml` redirect in the same change (CV-65, CV-84).
- Update `SUMMARY.md` only when adding, removing, or moving a page in the sidebar.
- Keep `SUMMARY.md` sidebar labels identical to the `title` frontmatter of each linked page. When
  renaming a page title or file, update the corresponding `SUMMARY.md` label in the same change.
- Keep existing sidebar order unless the task explicitly asks to change navigation.
- List every changed, added, moved, or deleted file at the end of the work.
- Flag any missing technical context before drafting instead of inventing behavior.
- Publish only through `steps/publish.md`, which opens one pull request against
  `publish.base_branch` and stops.

The agent **must not**:

- Commit, push, or open a pull request any other way than through `steps/publish.md`.
- Push to `main` or to the base branch, force-push, merge a pull request, or delete a branch it did
  not create.
- Rewrite unrelated pages.
- Replace existing screenshots or assets without confirming that the new asset is correct.
- Remove frontmatter, GitBook blocks, content references, or page metadata from existing pages.
- Create orphan pages that are unreachable from `SUMMARY.md`, a hub page, or a related-page link.
- Name a private repository, source path, feature flag, gated route, or internal symbol in a pull
  request, a commit message, or a page. The documentation repository is public.

### Agents that do not load this plugin

Codex reads the generated `AGENTS.md` at the root of the documentation repository, and Cursor reads
`.cursor/rules/convai-docs.mdc`. Both say what to read, which checks to run, and how far the agent may
publish: neither tool has `tools/publish.py` to refuse a forbidden call, so the text states the limits
itself, and it follows `publish.enabled`. For any other tool, give it `AGENTS.md` as its standing
instruction.

## In-repo documentation is a lead, not a source of truth

A source repository often ships its own `docs/`, `README.md`, or `CLAUDE.md`. Read them — they are the
fastest way to learn what a system does and what its parts are called. Then verify everything you take
from them against the code.

They are prose written by a person at some point in the past, under the same pressures that make
published documentation go stale, and nothing recompiles when they drift. A constant renamed, a limit
raised, a field removed — none of that updates the repo's own docs. Treating them as settled fact
imports someone else's stale claim into ours and gives it our name on it.

Two rules follow:

- **Never state a fact on the strength of in-repo docs alone.** Find the constant, the interface, the
  handler, the label in the source, and cite that. If the code and the repo's docs disagree, the code
  wins and the disagreement is worth reporting.
- **Never copy their wording.** Our pages follow the voice, structure, and terminology in
  `references/`, not whatever style that repository happens to use. A paragraph lifted from a
  README will not match our standards and will not read like the rest of our documentation.

The same applies to an existing published page: it is evidence of what someone once believed, not proof.

## Source-of-truth rule

Use the SDK source code, existing docs, provided technical notes, and the current documentation plan
as the source of truth. Do not invent API names, component fields, behavior, requirements, limits, or
console messages. If required technical context is missing, stop and ask for it before drafting.

## Change-summary requirement

At the end of any task, produce a change summary that lists:

- Every changed, added, moved, or deleted file.
- Any assumptions made.
- The source of truth used for technical claims (the subject and the commit, or the existing page or
  notes provided).
- Any open questions or screenshot placeholders that block publishing.
