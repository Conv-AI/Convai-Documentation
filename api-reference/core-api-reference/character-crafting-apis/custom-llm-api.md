---
description: >-
  Manage your private LLM integrations on Convai. Register, update, or delete
  OpenAI-compatible custom models securely through simple API endpoints.
hidden: true
---

# Custom LLM API

## Introduction

The **Convai Custom LLM Models API** allows developers and enterprises to register and manage their own **custom large language models (LLMs)** on the Convai platform.\
With these endpoints, you can connect private, OpenAI-compatible LLMs, control access, and manage lifecycle events such as registration, updates, and removal.

All endpoints are **POST** requests and both accept and return **JSON** objects.

***

## Base URL

```
https://api.convai.com
```

***

## Authentication

Each request must include your Convai API key in the header. Without it, requests return **401 Unauthorized**.

| Header             | Description               | Example                      |
| ------------------ | ------------------------- | ---------------------------- |
| **CONVAI-API-KEY** | Required on every request | `245a4u6864dj6848516l2dr6df` |

Example error for missing/invalid key:

```json
{
  "status": "error",
  "message": "Unauthorized: missing or invalid CONVAI-API-KEY",
  "transactionID": "..."
}
```

***

## Common Response Fields

All endpoints share the following base structure in their responses.

| Field             |       Type |          Description          |
| ----------------- | :--------: | :---------------------------: |
| **status**        |   string   |      "success" or "error"     |
| **message**       |   string   |     Human-readable summary    |
| **transactionID** |   string   | Unique identifier for tracing |
| **...**           |      —     |     Endpoint-specific data    |

***

## Endpoint Reference

| #                                                                     | Method & Path                 | Purpose                                       |
| --------------------------------------------------------------------- | ----------------------------- | --------------------------------------------- |
| [**2.1 Register a Model**](custom-llm-api.md#id-2.1-register-a-model) | `POST /llm-models/register`   | Register a new custom model                   |
| [**2.2 Update a Model**](custom-llm-api.md#id-2.2-update-a-model)     | `POST /llm-models/update`     | Update an existing custom model               |
| [**2.3 Deregister a Model**](custom-llm-api.md#id-2.2-update-a-model) | `POST /llm-models/deregister` | Remove a registered model                     |
| [**2.4 List Models**](custom-llm-api.md#id-2.4-list-models)           | `POST /llm-models/list`       | List all custom models linked to your API key |

***

### 2.1 Register a Model

**Endpoint:**

<mark style="color:green;">`POST`</mark> `https://api.convai.com/llm-models/register`

#### Request Body

<table><thead><tr><th width="211.6666259765625">Field</th><th width="93">Type</th><th width="124.3331298828125" align="center" valign="middle">      Required</th><th align="center">Notes</th></tr></thead><tbody><tr><td><strong>model_group_name</strong></td><td>string</td><td align="center" valign="middle">✓</td><td align="center">Unique, immutable identifier</td></tr><tr><td><strong>model_name</strong></td><td>string</td><td align="center" valign="middle">✓</td><td align="center">Model name, e.g., "gpt-4o-mini"</td></tr><tr><td><strong>api_key</strong></td><td>string</td><td align="center" valign="middle">✓</td><td align="center">Secret key for the remote LLM endpoint</td></tr><tr><td><strong>is_uncensored</strong></td><td>boolean</td><td align="center" valign="middle">✓</td><td align="center">True if jailbreak-free</td></tr><tr><td><strong>display_name</strong></td><td>string</td><td align="center" valign="middle">—</td><td align="center">Optional UI label (defaults to group name)</td></tr><tr><td><strong>base_url</strong></td><td>string</td><td align="center" valign="middle">—</td><td align="center">OpenAI-compatible endpoint (default: <code>https://api.openai.com/v1</code>)</td></tr></tbody></table>

#### Example cURL

{% tabs %}
{% tab title="MacOS/Linux" %}
```bash
curl -X POST https://api.convai.com/llm-models/register \
  -H "Content-Type: application/json" \
  -H "CONVAI-API-KEY: YOUR_API_KEY" \
  -d '{
        "model_group_name": "my-turbo",
        "model_name": "gpt-4o-mini",
        "api_key": "sk-proxy-123",
        "is_uncensored": false,
        "display_name": "Turbo (Private)",
        "base_url": "https://api.openai.com/v1"
      }'
```
{% endtab %}

{% tab title="Windows" %}
{% code overflow="wrap" %}
```powershell
curl -X POST "https://api.convai.com/llm-models/register" -H "Content-Type: application/json" -H "CONVAI-API-KEY: YOUR_API_KEY" -d "{\"model_group_name\": \"my-turbo\", \"model_name\": \"gpt-4o-mini\", \"api_key\": \"sk-proxy-123\", \"is_uncensored\": false, \"display_name\": \"Turbo (Private)\", \"base_url\": \"https://api.openai.com/v1\"}"
```
{% endcode %}
{% endtab %}
{% endtabs %}

#### Success Response (200 OK)

```json
{
  "status": "success",
  "model_group_name": "my-turbo",
  "model_name": "gpt-4o-mini",
  "display_name": "Turbo (Private)",
  "message": "Model 'my-turbo' registered successfully",
  "transactionID": "14b0cf96-5230-4b0f-a971-2f4f4f6d5e6a"
}
```

#### Possible Errors

| Code | Message                         | Cause                 |
| ---- | ------------------------------- | --------------------- |
| 400  | Missing required field          | Validation failure    |
| 409  | Model group name already exists | Duplicate identifier  |
| 500  | Database error                  | Internal server error |

***

### 2.2 Update a Model

**Endpoint:**

<mark style="color:green;">`POST`</mark> `https://api.convai.com/llm-models/update`

#### Request Body

| Field                  |        Type | Required |            Notes     |
| ---------------------- | :---------: | :------: | :------------------: |
| **model\_group\_name** |    string   |     ✓    |    Model to update   |
| **display\_name**      |    string   |     —    |   New friendly name  |
| **base\_url**          |    string   |     —    | Updated endpoint URL |
| **api\_key**           |    string   |     —    |    New API secret    |
| **is\_uncensored**     |   boolean   |     —    |   Toggle censorship  |

At least one optional field is required.

#### Example cURL

{% tabs %}
{% tab title="MacOS/Linux" %}
```bash
curl -X POST https://api.convai.com/llm-models/update \
  -H "Content-Type: application/json" \
  -H "CONVAI-API-KEY: YOUR_API_KEY" \
  -d '{
        "model_group_name": "my-turbo",
        "display_name": "Turbo v2",
        "api_key": "sk-proxy-456"
      }'
```
{% endtab %}

{% tab title="Windows" %}
{% code overflow="wrap" %}
```powershell
curl -X POST "https://api.convai.com/llm-models/update" -H "Content-Type: application/json" -H "CONVAI-API-KEY: YOUR_API_KEY" -d "{\"model_group_name\": \"my-turbo\", \"display_name\": \"Turbo v2\", \"api_key\": \"sk-proxy-456\"}"
```
{% endcode %}
{% endtab %}
{% endtabs %}

#### Success Response (200 OK)

```json
{
  "status": "success",
  "message": "Model 'my-turbo' updated successfully",
  "updated_fields": ["display_name", "api_key"],
  "transactionID": "5c0b6c67-97e4-4d78-9d5c-2a3de9d9c8ee"
}
```

#### Possible Errors

| Code | Message                     | Cause                              |
| ---- | --------------------------- | ---------------------------------- |
| 404  | Model not found             | Invalid or unauthorized model name |
| 409  | Display name already exists | Duplicate user label               |
| 400  | No valid fields to update   | Missing updatable fields           |

***

### 2.3 Deregister a Model

**Endpoint:**

<mark style="color:green;">`POST`</mark> `https://api.convai.com/llm-models/deregister`

#### Request Body

| Field                  |         Type |        Required |
| ---------------------- | :----------: | :-------------: |
| **model\_group\_name** |    string    |        ✓        |

#### Example cURL

{% tabs %}
{% tab title="MacOS/Linux" %}
```bash
curl -X POST https://api.convai.com/llm-models/deregister \
  -H "Content-Type: application/json" \
  -H "CONVAI-API-KEY: YOUR_API_KEY" \
  -d '{ "model_group_name": "my-turbo" }'
```
{% endtab %}

{% tab title="Windows" %}
{% code overflow="wrap" %}
```powershell
curl -X POST "https://api.convai.com/llm-models/deregister" -H "Content-Type: application/json" -H "CONVAI-API-KEY: YOUR_API_KEY" -d "{\"model_group_name\": \"my-turbo\"}"
```
{% endcode %}
{% endtab %}
{% endtabs %}

#### Success Response (200 OK)

```json
{
  "status": "success",
  "message": "Model 'my-turbo' deregistered successfully",
  "transactionID": "b11ac4f7-4cd3-4f43-8a79-3c942a14a8c9"
}
```

#### Possible Errors

| Code | Message         | Cause                                                 |
| ---- | --------------- | ----------------------------------------------------- |
| 404  | Model not found | Model does not exist or is not owned by the requester |

***

### 2.4 List Models

**Endpoint:**

<mark style="color:green;">`POST`</mark> `https://api.convai.com/llm-models/list`

This endpoint requires no request body.

#### Example cURL

{% tabs %}
{% tab title="MacOS/Linux" %}
```bash
curl -X POST https://api.convai.com/llm-models/list \
  -H "Content-Type: application/json" \
  -H "CONVAI-API-KEY: YOUR_API_KEY"
```
{% endtab %}

{% tab title="Windows" %}
{% code overflow="wrap" %}
```powershell
curl -X POST "https://api.convai.com/llm-models/list" -H "Content-Type: application/json" -H "CONVAI-API-KEY: YOUR_API_KEY"
```
{% endcode %}
{% endtab %}
{% endtabs %}

#### Success Response (200 OK)

```json
{
  "status": "success",
  "models": [
    {
      "model_group_name": "my-turbo",
      "model_name": "gpt-4o-mini",
      "display_name": "Turbo (Private)",
      "base_url": "https://api.openai.com/v1",
      "is_uncensored": false,
      "category": "Private",
      "created_at": "2025-07-08T09:41:38.123Z"
    },
    {
      "model_group_name": "raw-mixtral",
      "model_name": "mixtral-8x22b-base",
      "display_name": "Mixtral Raw",
      "base_url": "https://llm.my-org.net/v1",
      "is_uncensored": true,
      "category": "Private",
      "created_at": "2025-05-21T14:02:05.551Z"
    }
  ],
  "count": 2,
  "transactionID": "2caa4b99-eda9-46e2-a9ee-b4f251afcb1f"
}
```

***

## 3. Error Reference (All Endpoints)

| HTTP Code | Typical Reason                       |
| --------- | ------------------------------------ |
| **400**   | Missing or malformed parameters      |
| **401**   | Invalid or missing API key           |
| **404**   | Model not found or not owned by user |
| **409**   | Duplicate group or display name      |
| **429**   | Rate limit exceeded                  |
| **500**   | Internal server error                |

Example Error:

```json
{
  "status": "error",
  "message": "Model 'x' not found or access denied",
  "transactionID": "..."
}
```

***

## 4. Usage Notes & Best Practices

{% hint style="danger" %}
Convai currently supports only **OpenAI-compatible endpoints**.\
Most major providers (OpenAI, Google, Cohere, Hugging Face, vLLM, SGlang) support this format.
{% endhint %}

{% hint style="warning" %}
**model\_group\_name** is **immutable**; choose carefully (e.g., `llama3.1-70b-companyX` instead of generic names).
{% endhint %}

{% hint style="warning" %}
**display\_name** values must be **unique per user**.
{% endhint %}

{% hint style="warning" %}
Before using **deregister** for a model, make sure that all characters using the model have been switched to another model, or they will not work.
{% endhint %}

***

## Conclusion

The **Custom LLM API** provides a streamlined way to integrate, manage, and control custom LLM endpoints within Convai.\
By maintaining unique identifiers, secure API keys, and OpenAI-compatible URLs, you ensure stable and private model deployments for your use-case.
