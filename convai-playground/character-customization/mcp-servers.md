---
description: >-
  Connect your character to your tools and services through MCP servers for
  enhanced abilities.
---

# MCP Servers

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io) integration lets your character use tools from MCP servers during conversations. Your character can:

* Connect to any MCP-compatible server you host or subscribe to
* Discover the server's tools automatically at the start of each conversation
* Call tools mid-conversation and use the results in its replies

This lets your character look up data, search a knowledge source, or trigger an action in your systems, without a custom integration for each service.

### Prerequisites

Your MCP server must:

* Be reachable over **public HTTPS**. Local servers (stdio) and servers on private networks are not supported.
* Speak **Streamable HTTP** transport. SSE is supported as a legacy fallback.
* Authenticate with **static HTTP headers** (bearer token, API key), or no auth. OAuth-based servers are not supported yet.

### Add an MCP server

1. Open your character in the Playground and go to the **MCP and APIs** tab.
2. Click **Create Server**.
3. Fill in the server settings:

| Field         | Notes                                                                                                                                          |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Name          | Shown in the tool list. Short and descriptive.                                                                                                 |
| Description   | Optional, for your own reference.                                                                                                              |
| Server URL    | The full MCP endpoint, including the path, typically ending in `/mcp`.                                                                         |
| Protocol      | Streamable HTTP (recommended). Use SSE only if your server doesn't support Streamable HTTP.                                                    |
| Authorization | Header name/value pairs sent with every request, e.g. `Authorization: Bearer <token>`. Values are encrypted at rest.                           |
| Timeout       | Maximum seconds to wait for a single tool call (1–300, default 30). Keep it low, since the character can't reply until the tool call finishes. |

4. The **Available Tools** section connects to your server and lists the tools it exposes. This is also your connection test: an unreachable server or a wrong auth header shows its error here.
5. Uncheck any tools the character should not have. Only checked tools are offered to the LLM.
6. Turn on **Connected to this character** and click **Save**.

Servers are registered at the account level: the same server can be connected to multiple characters. **Disconnect** removes the server from the current character; **Delete** removes it from your account.

{% hint style="info" %}
Tools are discovered when a conversation session starts, not mid-session. After adding or editing a server, start a new session (reset the Playground chat session) before testing. All configuration changes apply from the next session.
{% endhint %}

### Compatible servers&#x20;

Any MCP server that authenticates with static headers, or no headers at all. This can be a server you build yourself with an MCP SDK ([Python](https://github.com/modelcontextprotocol/python-sdk), [TypeScript](https://github.com/modelcontextprotocol/typescript-sdk), FastMCP), or a hosted server that accepts an API key in a header, such as [Firecrawl](https://docs.firecrawl.dev/mcp), [Context7](https://context7.com), [GitHub](https://github.com/github/github-mcp-server) (personal access token), or [Atlassian](https://www.atlassian.com/platform/remote-mcp-server) (API token). Check the provider's docs for the endpoint URL and header format.

#### How tool calls work in conversation

At session start, Convai connects to each attached server and fetches its tool list. If a server is down or slow, it is skipped after a short connection budget and the conversation starts without its tools; a server outage does not prevent your character from talking.

During the conversation, the LLM decides when to call a tool based on its name and description. When it does:

* **The reply waits for the tool call.** In voice, the character is silent while the tool runs. Keep tools fast, under a couple of seconds.
* If the call times out or errors, the character is told and responds accordingly.
* Several tools can be called in one turn; the calls run in parallel.

#### Writing tools that work well in voice

Descriptions are prompts, so one clear sentence about what the tool does and when to use it beats an exhaustive spec. Expose few tools rather than many (large tool sets slow the model and cause wrong picks). Return short results fast, and fail with a message ("no orders found for that email") rather than an empty result.



{% hint style="info" %}
Tool permissions are set before the conversation: the per-tool checklist is the approval surface. There are no per-call approval prompts, so only enable tools you're comfortable having called on any turn.
{% endhint %}

### Security and data

#### Credentials

Authorization header values are encrypted at rest and used only to connect to your server.&#x20;

#### Who can trigger tools

Tools run under the credentials you configured, no matter who is talking to the character.

{% hint style="warning" %}
If the character is **public**, anyone who converses with it can trigger tool calls under your credentials. Only attach tools that are safe to expose to strangers: read-only, rate-limited, free of sensitive data.
{% endhint %}

#### Data flow

Tool arguments (which can include things the user just said) are sent to your MCP server, and results enter the model's context. That data leaves Convai and is subject to your server's own logging and retention. Tool descriptions and results are untrusted text entering the model's prompt; a malicious server can attempt to steer your character. Connect only servers you control or trust.

### Troubleshooting

| Symptom                                  | Cause and fix                                                                                                                                                                                                          |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Load tools: 401 / unauthorized           | The server rejected your auth header. Check the header name, the value format (many servers need the `Bearer` prefix), and that the token is active.                                                                   |
| Load tools: timeout / connection error   | The URL isn't a reachable MCP endpoint. Include the MCP path (typically `/mcp`); confirm the transport; confirm it's publicly reachable (`curl -i <url>` responds). Private/localhost URLs are rejected; use a tunnel. |
| Load tools: 0 tools                      | Connection worked but the server registers no tools. Check the server side.                                                                                                                                            |
| Tools don't appear in conversation       | The session started before you saved. Start a new session. If it persists: check the Connected switch is on and at least one tool is checked.                                                                          |
| Character says the tool failed           | Timeout (default 30 s), a server-side error (check your server logs for the `tools/call`), or an expired credential (re-run Load tools; a 401 there confirms it).                                                      |
| "Stored credentials cannot be decrypted" | Saved header values can no longer be read. The configuration is intact; re-enter the values and save.                                                                                                                  |
| Tool ignored or misused                  | Sharpen the tool description, reduce the number of enabled tools, add prompt guidance ("for order questions, use `lookup_order`"), and trim long results server-side.                                                  |
