---
title: Create a session
description: Open a conversation session and receive the session identifier that every following request in the conversation must include.
---

<!--
API ENDPOINT TEMPLATE. Diataxis mode: reference.

One endpoint per page. Contract first, narrative never.

Verify every field name, type, requirement, status code, and error string against the handler and
its request/response models in the source. Do not describe a field you have not read. Do not
state a rate limit, timeout, or size cap you cannot point at.

If an OpenAPI source exists, use the OpenAPI block instead of hand-writing the schema tables —
hand-written schemas drift from the implementation. Use this template when no spec is published.

Base URLs and versions come from GitBook variables, never literals.
Replace all content. No body `#`. Delete this comment before publishing.
-->

<Lead paragraph: what this endpoint does and when a caller uses it. One or two sentences. Name
what it returns, because that is what the reader is here for.>

## Endpoint

```http
POST <code class="expression">space.vars.api_base_url</code>/<path>
```

## Authentication

<Required header and token format, in inline code. Link to the authentication page rather than
restating how to obtain a key.>

| Header | Value | Required |
|---|---|---|
| `<Header-Name>` | `<format>` | Yes |

## Request

### Path parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `<name>` | `<type>` | Yes | <What it identifies.> |

### Body

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `<field>` | `<type>` | Yes | — | <What it controls.> |
| `<field>` | `<type>` | No | `<default>` | <What it controls.> |

```json
{
  "<field>": "<value>"
}
```

## Response

<State the success status code and what the caller does with the result.>

| Field | Type | Description |
|---|---|---|
| `<field>` | `<type>` | <What it holds.> |

```json
{
  "<field>": "<value>"
}
```

## Errors

| Status | Condition | Response | Retry |
|---|---|---|---|
| `400` | <What the caller did wrong.> | `<exact error body or code>` | No — fix the request. |
| `401` | <Auth failure condition.> | `<exact error body or code>` | No. |
| `429` | <Rate limit condition.> | `<exact error body or code>` | Yes, after the interval the response indicates. |
| `5xx` | <Server-side condition.> | `<exact error body or code>` | Yes, with backoff. |

## Example

{% tabs %}
{% tab title="curl" %}
```bash
curl -X POST "<url>" \
  -H "<Header-Name>: <value>" \
  -H "Content-Type: application/json" \
  -d '{"<field>": "<value>"}'
```
{% endtab %}

{% tab title="JavaScript" %}
```javascript
// <Equivalent request. Must be the same call, not a different workflow.>
```
{% endtab %}

{% tab title="Python" %}
```python
# <Equivalent request.>
```
{% endtab %}
{% endtabs %}

## Next steps

{% content-ref url="<next-endpoint>.md" %}
[<Next endpoint title>](<next-endpoint>.md)
{% endcontent-ref %}
