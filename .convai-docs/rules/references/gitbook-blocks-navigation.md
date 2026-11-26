# GitBook blocks for navigation pages

Cards and columns, which route and compare, and the page options a hub or top-level page sets.
`page-types.md` says which page types read this file.

| Content need | Block |
|---|---|
| Hub or section index navigation | Cards |
| Side-by-side comparison | Columns, only when mobile readability remains acceptable |

## Cards

Use cards for hub pages and section index pages, to route readers to the main child pages instead of a
dense bullet list of links.

```html
<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Install the Unity SDK</strong><br>Install the package and verify that Unity loads it correctly.</td>
<td><a href="install-the-unity-sdk.md">install-the-unity-sdk.md</a></td>
</tr>
<tr>
<td><strong>Configure the API key</strong><br>Add authentication settings required for SDK requests.</td>
<td><a href="configure-the-api-key.md">configure-the-api-key.md</a></td>
</tr>
</tbody>
</table>
```

Cards are for routing. Do not use them inside dense procedural pages.

## Columns

Use columns only when a side-by-side comparison improves comprehension and the page still reads well
on mobile. Never for content the reader must read in order.

```md
{% columns %}
{% column width="50%" %}
**Inspector**

Use this path for scene-based setup.
{% endcolumn %}

{% column %}
**C#**

Use this path for runtime configuration.
{% endcolumn %}
{% endcolumns %}
```

## Page options and rendering

The frontmatter keys a page may set are in `page-structure.md`. These are the remaining options.

| GitBook feature | Standard |
|---|---|
| Page icon | Every top-level page and every hub page has one, from the space's allowed list (CV-81). |
| Cover image | Use only on a section landing page, and only when the image carries meaning. A decorative cover pushes the lead paragraph below the fold. |
| Tags | Apply the tags the section already uses. Do not invent a new tag vocabulary for one page. |
| Page outline | Make the `##` and `###` structure useful enough to navigate from the outline alone. |
| Sidebar label | Short but meaningful. Avoid vague labels like `Setup`, `Basics`, `Advanced`. Must match the page `title` exactly (CV-38). |
| Page link title | Set a separate link title only when the full page title does not fit the sidebar. Make the link title shorter, never vaguer. |
| Next/previous links | Keep enabled for linear getting-started and tutorial flows. Disable only for custom landing pages or standalone reference surfaces. |
| Layout width | Default for normal prose and procedures. Wide for cards, wide tables, OpenAPI blocks, or horizontally dense code (CV-74). |
| Page metadata | Use canonical and alternate URLs for duplicate, versioned, or localized pages. Do not canonicalize pages that are only related but materially different. |
| Hidden pages | Use intentionally for drafts, private support pages, reusable content, or deprecated pages. Hidden pages still need a clear owner and review state (CV-75). |
| Search indexing | Do not hide production-useful support, troubleshooting, migration, or reference pages from search without a specific reason. |
