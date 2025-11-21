---
description: >-
  API to evaluate a conversation transcript based on user defined attributes
  (e.g. clarity of responses, courtesy, listening skills, and more).
---

# Evaluation API

{% hint style="danger" %}
This API is available only on the Professional Plan and above.
{% endhint %}

## Convai's Evaluation API endpoint

<mark style="color:green;">POST</mark> `https://api.convai.com/character/evaluate_conversation`

This API allows you to evaluate a conversation transcript based on user defined attributes e.g. clarity of responses, courtesy, listening skills, and more. The evaluation will be returned in a structured JSON format.

### Headers

| Name                                             | Type   | Description                                    |
| ------------------------------------------------ | ------ | ---------------------------------------------- |
| CONVAI-API-KEY<mark style="color:red;">\*</mark> | String | The unique api-key provided for every account. |

### Request Body

| Name          | Type                   | Description                                                                                                                                                |
| ------------- | ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| session\_id   | String (required)      | The ID of the session you want to evaluate.                                                                                                                |
| character\_id | String (required)      | The ID of the character performing the evaluation.                                                                                                         |
| prompt        | String (required)      | A predefined or custom prompt containing the transcript and specific instructions for evaluation.                                                          |
| variables     | JSON Object (optional) | A set of key-value pairs providing additional data required for evaluation (e.g., customer name, item details). This depends on the `prompt` being passed. |

### Example Payload

```json
{
  "session_id": "<SESSION ID>",
  "character_id": "<CHARACTER ID>",
  "prompt": "<EVALUATION PROMPT>",
  "variables": {
    "customer_name": "Suzie Denver",
    "customer_age": "54 years",
    "item_details": [
      {
        "item": "Burger",
        "price": "$4",
        "quantity": 3
      },
      {
        "item": "Fries",
        "price": "$2",
        "quantity": 2
      }
    ]
  }
}
```

#### Example prompt

{% code overflow="wrap" %}
```json
You are an human analyst designated to evaluate employee-customer interactions in a given scenario. Based on the conversation transcript provided below, analyze the interaction and provide an evaluation according to the specified attributes. Each attribute should be rated on a scale of Excellent, Good, Fair, or Needs Improvement. Provide specific examples from the transcript to support your rating. Return the evaluation results in a structured JSON format for easy parsing.
Transcript:
[[conversation_history]]


Here are some data that might be needed to evaluate the conversations:
Actual Order: [[item_details]]
Customer Name: [[customer_name]]
Customer Age: [[customer_age]]


Please evaluate the above conversation based on the attributes listed and provide a Rating and Feedback for each of them. If an attribute is not applicable or cannot be assessed, return null in the json output. Return the result in the following format:


{
  "evaluation": {
    "correctness_of_responses": {
      "rating": "",
      "feedback": "[Did the employee place the actual order correctly based on the customer's request?]"
    },
    "clarity_of_responses": {
      "rating": "]",
      "feedback": "[Did the employee's responses appear clear and easy to understand based on the text provided?]"
    },
    "conciseness_and_relevance": {
      "rating": "",
      "feedback": "[Were the employee’s responses concise and focused on the relevant details, without unnecessary information?]"
    },
    "courtesy_and_respect": {
      "rating": "",
      "feedback": "[Did the employee demonstrate politeness and respect toward the customer in their language and responses?]"
    },
    "listening_skills": {
      "rating": "",
      "feedback": "[Did the employee respond appropriately, indicating they were actively listening and addressing customer concerns?]"
    },
    "product_knowledge": {
      "rating": "",
      "feedback": "[Did the employee demonstrate accurate knowledge of the menu, promotions, or policies?]"
    },
    "problem_solving_and_issue_resolution": {
      "rating": "",
      "feedback": "[Evaluate how well the employee addressed and resolved issues]"
    },
    "response_time": {
      "rating": "",
      "feedback": "[Analyze the flow of the conversation and whether there were any delays in response]"
    },
    "order_accuracy": {
      "rating": "",
      "feedback": "[Evaluate the accuracy of order confirmation, if applicable]"
    },
    "follow_up_and_conversation_closure": {
      "rating": "",
      "feedback": "[Review how the conversation was closed and whether appropriate follow-up occurred]"
    },
    "overall_summary": {
      "overall_rating": "",
      "overall_feedback": "[Provide a brief summary of the employee's performance across all attributes]"
    }
  }
}
```
{% endcode %}

{% hint style="info" %}
If you focus on the prompt, there are certain text within `[[ ]]` . These are `expected-variables`. Now, `[[conversation_history]]` is a compulsory expected-variable, that has to be present in the prompt. The rest of them depends on your requirements, to be passed to the prompt as needed.

So the `variables` key, in the body of the request, should be of length `expected-variables - 1`, i.e, there should be values for all the other keys mentioned in the `[[ ]]` brackets, except for `conversation_history` which is fetched from the `session_id` provided. The `variables` list can be empty if you are passing no other `expected-variables`  in the prompt.
{% endhint %}

{% hint style="danger" %}
Not passing the `conversation_history` variable in the prompt will lead to 500 error response from the server.
{% endhint %}

### Response

{% tabs %}
{% tab title="200: OK" %}
On success, the API returns a structured evaluation of the conversation, covering multiple attributes.

```json
{
  "evaluation": {
    "clarity_of_responses": {
      "rating": "Excellent",
      "feedback": "The employee provided clear and concise responses throughout the conversation."
    },
    "conciseness_and_relevance": {
      "rating": "Good",
      "feedback": "Responses were relevant but could be more concise."
    },
    "courtesy_and_respect": {
      "rating": "Excellent",
      "feedback": "The employee was polite and respectful."
    },
    "listening_skills": {
      "rating": "Good",
      "feedback": "The employee responded appropriately, though some concerns were addressed after a delay."
    },
    "product_knowledge": {
      "rating": "Excellent",
      "feedback": "The employee demonstrated accurate knowledge of the menu."
    },
    "problem_solving_and_issue_resolution": {
      "rating": "Needs Improvement",
      "feedback": "Issue resolution took longer than expected."
    },
    "response_time": {
      "rating": "Fair",
      "feedback": "There were noticeable delays between responses."
    },
    "order_accuracy": {
      "rating": "Excellent",
      "feedback": "All items were confirmed accurately."
    },
    "follow_up_and_conversation_closure": {
      "rating": "Good",
      "feedback": "The employee followed up appropriately, though the closure could have been smoother."
    },
    "overall_summary": {
      "overall_rating": "Good",
      "overall_feedback": "The employee's performance was generally good, but there is room for improvement in responsiveness."
    }
  }
}

```

<br>
{% endtab %}

{% tab title="401: Invalid API Key Provided" %}
```json
{
    "ERROR": "Invalid API key provided."
}
```
{% endtab %}

{% tab title="500: Internal Server Error" %}
```json
{
    "ERROR": "Invalid variable list. Please recheck the variables being sent",
    "Reference ID": "<REFERENCE-ID>"
}
```
{% endtab %}
{% endtabs %}

### Code Snippet&#x20;

```python
import requests
import json

EVALUATION_URL = "https://api.convai.com/character/evaluate_conversation"

# Headers
headers = {
  'Content-Type': 'application/json',
  'CONVAI-API-KEY': '<YOUR API KEY>'
}

# Payload
payload = {
    "session_id": "<SESSION ID>",
    "character_id": "<CHARACTER ID>",
    "prompt": "<YOUR CUSTOM PROMPT>",
    "variables": {
        "customer_name": "Suzie Denver",
        "customer_age": "54 years",
        "item_details": json.dumps([
            {"item": "Burger", "price": "$4", "quantity": 3},
            {"item": "Fries", "price": "$2", "quantity": 2}
        ])
    }
}

# Make the request
response = requests.post(EVALUATION_URL, headers=headers, json=payload)

# Handle the response
evaluation_response = response.json()

try:
    evaluation = evaluation_response["evaluation"]
    print("Evaluation: ", evaluation)
except KeyError:
    print("Error: ", evaluation_response)

```
