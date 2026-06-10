---
title: Advanced topics
description: Find production authentication, security, and integration guides for the Convai Unreal Engine plugin beyond the core setup path.
last_reviewed: "4.0.0-beta.21"
---

These pages cover workflows you need after the core setup path is working — especially when you ship a packaged application and must keep credentials out of the build. Start with the getting-started path if you have not installed the plugin or configured authentication yet.

## Guides

<table data-view="cards">
<thead>
<tr>
<th></th>
<th data-hidden data-card-target data-type="content-ref"></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Use personal access tokens</strong><br>Generate a short-lived token on your backend and pass it to the Unreal plugin so production builds do not ship a real API key.</td>
<td><a href="personal-access-token.md">personal-access-token.md</a></td>
</tr>
</tbody>
</table>

## Related setup pages

If you are still configuring authentication for the first time, start with the getting-started path before returning here.

{% content-ref url="../getting-started/configure-your-api-key.md" %}
[Configure your API key](../getting-started/configure-your-api-key.md)
{% endcontent-ref %}

{% content-ref url="../core-concepts/session-lifecycle.md" %}
[Session lifecycle](../core-concepts/session-lifecycle.md)
{% endcontent-ref %}
