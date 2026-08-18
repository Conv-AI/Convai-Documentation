# Safe publishing and AI-agent rules

Use a staging-first workflow for AI-generated or AI-assisted documentation. The agent prepares file
changes only and stops for human review.

## Branch and Space workflow

| Environment | Git branch | GitBook Space | Purpose |
|---|---|---|---|
| Staging | `staging` | Staging Space | Draft, review, and validate generated documentation. |
| Production | `main` | Live Space | Publish reviewed documentation only. |

Required workflow:

1. Create or revise documentation only on the `staging` branch.
2. Sync the GitBook Staging Space from the `staging` branch.
3. Review the rendered pages in the Staging Space.
4. Open a pull request from `staging` to `main`.
5. Merge to `main` only after the Staging Space renders correctly.
6. Let the live GitBook Space sync from `main`.

Do not push AI-generated documentation directly to `main`.

## Change Requests and Merge Rules

When using GitBook's native editor (not Git Sync), use Change Requests as the quality gate equivalent
of a pull request.

| Step | Action |
|---|---|
| Draft | Open a Change Request for the new or revised page. |
| Review | Assign a reviewer. The reviewer checks against the quality checklist. |
| Merge Rules | Require at least one reviewer approval before a Change Request can be merged. |
| Merge | Merge only after the reviewer approves and the page passes the quality checklist. |

Configure Merge Rules in **Space settings → Merge rules**: require reviewer approval (on); prevent
self-merge (on); required checks: pass the quality checklist before requesting review.

Change Request rules for AI-generated content:

- Every AI-generated page must go through a Change Request before merging.
- The description must list the AI tool used, the source of truth for technical claims, and any assumptions.
- A human reviewer — not the AI agent — must perform the final approval.

## Safe AI-agent editing rules

The agent **must**:

- Work only on the `staging` branch.
- Preserve existing documentation unless the task explicitly asks for a specific revision.
- Never delete pages, folders, images, or GitBook configuration files without explicit approval.
- Avoid renaming files or moving pages unless the task is a navigation or restructuring task.
- Update `SUMMARY.md` only when adding, removing, or moving a page in the sidebar.
- Keep `SUMMARY.md` sidebar labels identical to the `title` frontmatter of each linked page. When
  renaming a page title or file, update the corresponding `SUMMARY.md` label in the same change.
- Keep existing sidebar order unless the task explicitly asks to change navigation.
- List every changed, added, moved, or deleted file at the end of the work.
- Flag any missing technical context before drafting instead of inventing behavior.
- Stop after preparing file changes and wait for explicit human approval before any commit, push,
  pull request, or merge.

The agent **must not**:

- Commit directly to `main`.
- Create any commit without explicit human approval.
- Push any branch without explicit human approval.
- Open a pull request without explicit human approval.
- Merge a pull request without explicit human approval.
- Rewrite unrelated pages.
- Replace existing screenshots or assets without confirming that the new asset is correct.
- Remove frontmatter, GitBook blocks, content references, or page metadata from existing pages.
- Create orphan pages that are unreachable from `SUMMARY.md`, a hub page, or a related-page link.

### Instruction block for an external agent

When handing this work to a tool that does not load this skill — a general-purpose assistant, a
one-off script, or a contractor's setup — paste this block verbatim as its standing instruction:

```text
You are editing the Convai documentation repository.

Work only on the staging branch. Prepare file changes and stop.

Do not commit, push, open a pull request, or merge. A human does all of those.

Do not delete or rename pages, folders, images, or GitBook configuration.
Do not rewrite pages unrelated to the task.
Do not remove frontmatter, GitBook blocks, content references, or page metadata.
Do not create a page that nothing links to.

Update SUMMARY.md only when a page is added to, removed from, or moved in the sidebar,
and keep each sidebar label identical to that page's title frontmatter.

Never invent an API name, field, default value, limit, behavior, or console message.
If a fact you need is missing, stop and ask for it.

Finish by listing every file you added, changed, moved, or deleted, the source you
verified technical claims against, and any assumption or open question.
```

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
- The source of truth used for technical claims (SDK source path, existing page, or provided notes).
- Any open questions or screenshot placeholders that block publishing.
