---
description: >-
  Enable real-time conversational AI with Convai’s Interaction API. Send text
  messages to your AI character and receive natural, streaming responses using
  Server-Sent Events (SSE).
hidden: true
---

# Interaction API (Beta)

{% hint style="danger" %}
This API is available only on the Professional Plan and above.
{% endhint %}

## Overview

The **Interaction API** provides real-time conversational capabilities via a lightweight **REST + SSE** interface.\
It allows your application to send user messages and receive streaming character responses with minimal latency.

This API supports continuous conversation context through session IDs and streams all outputs as **Server-Sent Events (SSE)** for smooth, live feedback.

***

## Authentication <a href="#authentication" id="authentication"></a>

All API requests require authentication using an API key in the header:

```http
X-API-Key: your_api_key_here
```

***

## Endpoint <a href="#endpoint" id="endpoint"></a>

<mark style="color:green;">`POST`</mark> `https://live.convai.com/connect/stream` &#x20;

Send a text query to an AI character and receive a streaming response.

**Request Format:** `multipart/form-data`

<table><thead><tr><th width="220">Parameter</th><th width="109.666748046875">Type</th><th>Description</th></tr></thead><tbody><tr><td>character_id<mark style="color:red;">*</mark></td><td>UUID</td><td>Unique identifier for the AI character</td></tr><tr><td>text_input<mark style="color:red;">*</mark></td><td>string</td><td>Your text query/message to the character</td></tr><tr><td>character_session_id</td><td>string</td><td>Session ID to continue an existing conversation</td></tr></tbody></table>

### Example Requests

{% tabs %}
{% tab title="cURL" %}
```shell
curl -X POST https://live.convai.com/connect/stream \
  -H "X-API-Key: YOUR_API_KEY" \
  -F "character_id=7bd3274c-1745-11ee-a3af-42010a400002" \
  -F "text_input=Hello, how are you?" \
  --no-buffer
```
{% endtab %}

{% tab title="Python" %}
```python
import httpx
import json

async with httpx.AsyncClient(timeout=30.0) as client:
    async with client.stream(
        'POST',
        'https://live.convai.com/connect/stream',
        headers={'X-API-Key': 'YOUR_API_KEY'},
        data={
            'character_id': '7bd3274c-1745-11ee-a3af-42010a400002',
            'text_input': 'Hello, how are you?'
        }
    ) as response:
        async for line in response.aiter_lines():
            if line.startswith('data: '):
                data = json.loads(line[6:])
                if data.get('type') == 'bot-llm-text':
                    print(data['data']['text'], end='', flush=True)

```
{% endtab %}

{% tab title="JavaScript" %}
```javascript
const formData = new FormData();
formData.append('character_id', '7bd3274c-1745-11ee-a3af-42010a400002');
formData.append('text_input', 'Hello, how are you?');

const response = await fetch('https://live.convai.com/connect/stream', {
  method: 'POST',
  headers: { 'X-API-Key': 'YOUR_API_KEY' },
  body: formData,
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;

  const chunk = decoder.decode(value);
  const lines = chunk.split('\n');

  for (const line of lines) {
    if (line.startsWith('data: ')) {
      const data = JSON.parse(line.slice(6));
      if (data.type === 'bot-llm-text') {
        console.log(data.data.text);
      }
    }
  }
}
```
{% endtab %}
{% endtabs %}

**Response:** Server-Sent Events (SSE) stream

```
data: {"type": "connection-started", "message": {"session_id": "abc123", "transport": "sse", "character_session_id": "def456"}}

data: {"label": "rtvi-ai", "type": "bot-llm-started"}

data: {"label": "rtvi-ai", "type": "bot-llm-text", "data": {"text": "Hello"}}

data: {"label": "rtvi-ai", "type": "bot-llm-text", "data": {"text": "! I'm doing great, thank you for asking."}}

data: {"label": "rtvi-ai", "type": "bot-transcription", "data": {"text": "Hello! I'm doing great, thank you for asking."}}

data: {"label": "rtvi-ai", "type": "bot-llm-stopped"}

data: {"type": "connection-stoppped"}
```

***

{% hint style="warning" %}
**Important Points**

* The request body must be `multipart/form-data` format. Use `-F` flag in cURL (not `-d`).
* Skip `character_session_id` to start a new conversation. Add it to continue an existing conversation.
* Character Session IDs are strings. Do not send `-1` or other placeholder values.
* Responses are streamed via Server-Sent Events (SSE). Set timeout to 30+ seconds.
* All interactions are subject to content moderation policies. Repeated violations may result in API key suspension.
* Requests are rate-limited per API key. Implement exponential backoff for rate limit errors.
{% endhint %}

## Resume Conversation <a href="#conversation-continuity" id="conversation-continuity"></a>

To maintain conversation context, save the `character_session_id` from the first response and include it in subsequent requests.

### Example Requests

{% tabs %}
{% tab title="cURL" %}
**First Request:**

```bash
curl -X POST https://live.convai.com/connect/stream \
  -H "X-API-Key: YOUR_API_KEY" \
  -F "character_id=7bd3274c-1745-11ee-a3af-42010a400002" \
  -F "text_input=My name is Alice" \
  --no-buffer
```

**Response includes:**

```json
{"type": "connection-started", "message": {"character_session_id": "9a98ab9b-5a6c-406e-9721-cc5bb0d527bb", ...}}
```

**Second Request (with session ID):**

```bash
curl -X POST https://live.convai.com/connect/stream \
  -H "X-API-Key: YOUR_API_KEY" \
  -F "character_id=7bd3274c-1745-11ee-a3af-42010a400002" \
  -F "text_input=What is my name?" \
  -F "character_session_id=9a98ab9b-5a6c-406e-9721-cc5bb0d527bb" \
  --no-buffer
```

**Bot remembers:** "Your name is Alice."
{% endtab %}

{% tab title="Python" %}
```python
import httpx
import json
import asyncio

session_id = None

async def chat(message):
    global session_id

    data = {
        'character_id': '7bd3274c-1745-11ee-a3af-42010a400002',
        'text_input': message,
    }

    if session_id:
        data['character_session_id'] = session_id

    async with httpx.AsyncClient(timeout=30.0) as client:
        async with client.stream(
            'POST',
            'https://live.convai.com/connect/stream',
            headers={'X-API-Key': 'YOUR_API_KEY'},
            data=data,
        ) as response:
            async for line in response.aiter_lines():
                if line.startswith('data: '):
                    msg = json.loads(line[6:])

                    if msg.get('type') == 'connection-started':
                        session_id = msg['message']['character_session_id']
                    elif msg.get('type') == 'bot-llm-text':
                        print(msg['data']['text'], end='', flush=True)
            print()

# Usage
await chat('My name is Alice')
await chat('What is my name?')  # Bot remembers: "Your name is Alice"
```
{% endtab %}

{% tab title="JavaScript" %}
```javascript
let sessionId = null;

async function chat(message) {
  const formData = new FormData();
  formData.append('character_id', '7bd3274c-1745-11ee-a3af-42010a400002');
  formData.append('text_input', message);

  if (sessionId) {
    formData.append('character_session_id', sessionId);
  }

  const response = await fetch('https://live.convai.com/connect/stream', {
    method: 'POST',
    headers: { 'X-API-Key': 'YOUR_API_KEY' },
    body: formData,
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop();

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = JSON.parse(line.slice(6));

        if (data.type === 'connection-started') {
          sessionId = data.message.character_session_id;
        } else if (data.type === 'bot-llm-text') {
          process.stdout.write(data.data.text);
        }
      }
    }
  }
  console.log();
}

// Usage
await chat('My name is Alice');
await chat('What is my name?');  // Bot remembers: "Your name is Alice"
```
{% endtab %}
{% endtabs %}

## Response Message Types <a href="#response-message-types" id="response-message-types"></a>

#### connection-started <a href="#connection-started" id="connection-started"></a>

Sent when the connection is established.

```json
{
  "type": "connection-started",
  "message": {
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "transport": "sse",
    "character_session_id": "660e8400-e29b-41d4-a716-446655440001"
  }
}
```

**Fields:**

* `session_id`: Unique identifier for this connection
* `transport`: Transport type (always "sse")
* `character_session_id`: **Save this to continue the conversation in future requests**

#### bot-llm-started <a href="#bot-llm-started" id="bot-llm-started"></a>

Sent when the LLM starts generating a response.

```json
{
  "label": "rtvi-ai",
  "type": "bot-llm-started"
}
```

#### bot-llm-text <a href="#bot-llm-text" id="bot-llm-text"></a>

Bot response text, streamed in chunks as they are generated.

```json
{
  "label": "rtvi-ai",
  "type": "bot-llm-text",
  "data": {
    "text": "Hello there!"
  }
}
```

**Fields:**

* `text`: A chunk of the bot's response text

#### bot-transcription <a href="#bot-transcription" id="bot-transcription"></a>

Complete transcription of the bot's response (sent after all text chunks).

```json
{
  "label": "rtvi-ai",
  "type": "bot-transcription",
  "data": {
    "text": "Hello there! Complete response text."
  }
}
```

**Fields:**

* `text`: The complete bot response text

#### bot-llm-stopped <a href="#bot-llm-stopped" id="bot-llm-stopped"></a>

Sent when the LLM finishes generating.

```json
{
  "label": "rtvi-ai",
  "type": "bot-llm-stopped"
}
```

#### connection-stoppped <a href="#connection-stoppped" id="connection-stoppped"></a>

Sent when the response is complete and connection is closing.

```json
{
  "type": "connection-stoppped"
}
```

***

## Error Responses <a href="#error-responses" id="error-responses"></a>

All endpoints return standard HTTP error codes:

<table><thead><tr><th width="174">Status Code</th><th>Description</th></tr></thead><tbody><tr><td><code>400</code></td><td>Bad Request - Invalid parameters</td></tr><tr><td><code>401</code></td><td>Unauthorized - Invalid or missing API key</td></tr><tr><td><code>404</code></td><td>Not Found - Character not found</td></tr><tr><td><code>422</code></td><td>Unprocessable Entity - Validation error</td></tr><tr><td><code>429</code></td><td>Too Many Requests - Rate limit exceeded</td></tr><tr><td><code>500</code></td><td>Internal Server Error</td></tr></tbody></table>

**Error Response Format:**

```json
{
  "detail": "Error message describing what went wrong"
}
```

**Example:**

```json
{
  "detail": "Invalid API key"
}
```

## Conclusion

The **Interaction API (Beta)** enables dynamic, real-time communication with your Convai characters over text.\
By combining streaming responses, context persistence, and SSE-based delivery, it provides a responsive and low-latency conversational experience suitable for chat, games, and interactive AI applications.
