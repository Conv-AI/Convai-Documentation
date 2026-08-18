---
description: >-
  Limits that apply to External API everywhere — supported models, Python
  runtime, libraries, input schema, and per-character caps.
---

# External API limitations

These limits apply whether you configure External API in the [Playground](external-api.md) or through the [API](../../api-reference/core-api-reference/character-crafting-apis/external-api.md).

## Supported models

External API only runs when the character's model can call tools. That depends on the path you use:

| Path | Supported models |
| ---- | ---------------- |
| **Live API (WebRTC)** | OpenAI, Claude, and Gemini. Popular open-source models that support tools — including Grok and the DeepSeek family — work here too. Others may work if they support tool calling; check [models.dev](https://models.dev). |
| **gRPC** | OpenAI, Claude, and Gemini family models only. |

If the model doesn't support tools, the character still chats normally — it just won't call your External API functions.

## Runtime

| Rule | Detail |
| ---- | ------ |
| Language | Python only (`"language": "python"`) |
| Runtime | Python 3.11 |
| Standard library | Allowed (`json`, `datetime`, `math`, `re`, `urllib`, and the rest of the stdlib) |
| Third-party packages | **`requests` only** for now |
| Source code size | At most 400 lines |
| Entry point | Must define `def handle_event(inputs):` (single argument; name is fixed) |
| Return value | JSON-serializable, usually a `dict` |
| State | No shared mutable state across calls — each run is independent |

Anything outside the standard library and `requests` fails at runtime.

## Input description

`input_description` is a **JSON string** (not a nested object in the API body). After parsing, it must look like:

```json
{
  "parameters": {
    "city": {
      "type": "string",
      "description": "Name of the city to look up"
    }
  },
  "required": ["city"]
}
```

| Rule | Detail |
| ---- | ------ |
| Top-level keys | `parameters` and `required` are both required |
| Parameter names | `^[a-zA-Z_][a-zA-Z0-9_]*$` |
| Parameter fields | Each parameter needs `type` and `description` |
| Allowed types | `string`, `integer`, `boolean`, `object`, `array` |
| Extra keys under `parameters` | Not allowed |

Keep descriptions concrete. The model fills arguments from that text, so vague wording produces bad calls.

## Character limits

| Rule | Detail |
| ---- | ------ |
| Active functions per character | At most **128** |
| Unlink vs delete | `"status": "inactive"` only disconnects a character; delete removes the function from the account and every link |

## Related

* [External API (Playground)](external-api.md) — UI setup and examples
* [External API (API reference)](../../api-reference/core-api-reference/character-crafting-apis/external-api.md) — create, list, link, unlink, delete
