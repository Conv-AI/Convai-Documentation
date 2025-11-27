---
description: >-
  Learn how to integrate and configure the External API feature to enable your
  characters to access real-time information, create tasks, and interact with
  third-party platforms.
hidden: true
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/convai-playground/character-customization/external-api
---

# External API

## Introduction

The **External API** feature empowers your characters to interact intelligently with real-time data sources and third-party services. Whether it’s retrieving live weather updates, tracking sports scores, or creating tickets in platforms like Jira and Trello, this feature allows seamless API-based integration. With just a few configuration steps, your characters can fetch data, trigger workflows, and execute automated actions, making them significantly more capable.

{% embed url="https://www.youtube.com/watch?v=Ep1yUeu91FE" %}

***

## Configuration and Usage

### 1. Accessing the External API Page

Navigate to the **External API** section in your dashboard. Here you can view existing API methods, activate or deactivate them, and create new methods. To add a new API method, click **Add API Method**.

<figure><img src="../../.gitbook/assets/Screenshot 2025-08-09 222338.png" alt=""><figcaption></figcaption></figure>

***

### 2. Creating an API Method

**Method Fields Overview**

* **Method Name** – Select an existing template or enter a unique name for your method.
* **Method Description** – Provide a concise explanation of the method’s functionality.
* **Input Description (JSON Format)** – Define required input parameters and their descriptions.
* **Implementation Code** – Write the Python implementation for your API logic.
* **Inputs** – Enter test parameters for validating your method.
* **Output** – Displays the result when you click **Test API**.

<figure><img src="../../.gitbook/assets/Screenshot 2025-08-09 222520.png" alt=""><figcaption></figcaption></figure>

***

## Example 1 – Get Weather Data

**Method Name**\
`Get Weather`

**Method Description**\
`Fetches current weather data for a given city`

**Input Description**

```json
{
    "parameters": {
        "city": {
            "type": "string",
            "description": "Name of the city to get weather information for (e.g., 'London', 'New York', 'Tokyo')"
        }
    },
    "required": [
        "city"
    ]
}
```

**Implementation Code**

```python
import requests

API_KEY = "<your-api-key>"

def handle_event(data):
    city = data.get("city")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(url)
    weather_data = response.json()
    return {"weather": weather_data["weather"][0]["description"]}
```

**Setup Notes**

1. Sign up at [OpenWeatherMap](https://openweathermap.org/) and get your API key.
2. Replace `<your-api-key>` in the code with your key.

**Test Input**

```json
{
  "city": "New York"
}
```

Click **Test API**.&#x20;

**A successful Output Example:**

```json
{
  "weather": "clear sky"
}
```

<figure><img src="../../.gitbook/assets/Screenshot 2025-08-09 222520.png" alt=""><figcaption></figcaption></figure>

#### **Activate the method**

If the test passes, click **Save Changes**, return to the main API list, and enable the method by toggling **Connect** to green.

<figure><img src="../../.gitbook/assets/Screenshot 2025-08-09 222055.png" alt=""><figcaption></figcaption></figure>

#### **Test with a character**

Once activated, test the method in a conversation with your character.\
As seen in the screenshot below, the character correctly returned the current weather for Roma and Wrangell.

<figure><img src="../../.gitbook/assets/Screenshot 2025-08-09 155243.png" alt=""><figcaption></figcaption></figure>

***

## Example 2 – Create Jira Support Ticket

**Method Name**\
`Creating Support Tickets`

**Method Description**\
`Creates a support ticket on Jira`

**Input Description**

```json
{
    "parameters": {
        "summary": {
            "type": "string",
            "description": "Short title for the Jira ticket"
        },
        "description": {
            "type": "string",
            "description": "Detailed description of the Jira issue"
        }
    },
    "required": [
        "summary",
        "description"
    ]
}
```

**Implementation Code**

```python
import requests
from requests.auth import HTTPBasicAuth
import json

# Jira configuration
JIRA_DOMAIN = "mycompany.atlassian.net"  # Replace with your Jira domain
EMAIL = "user@example.com"               # Replace with your Atlassian account email
API_TOKEN = "abc123xyz456..."            # Replace with your Jira API token
JIRA_PROJECT_KEY = "EX"                  # Replace with your Jira project key
ISSUE_TYPE = "Story"                     # Issue type: Story, Task, or Bug

API_ENDPOINT = f"https://{JIRA_DOMAIN}/rest/api/3/issue"

# Standard headers required by JIRA.
headers = {"Accept": "application/json", "Content-Type": "application/json"}

def create_jira_ticket(ticket_data):
    """
    Create a JIRA ticket using provided ticket_data dictionary.

    Expected ticket_data keys:
      - summary: (str) Brief summary of the issue.
      - description: (str) Detailed description of the issue.

    Returns:
      - JSON response if the ticket is created successfully.
      - Error message if there was an error.
    """
    # Convert plain text description to Atlassian Document Format
    description_adf = {
        "version": 1,
        "type": "doc",
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": ticket_data.get("description", "")}
                ],
            }
        ],
    }

    # Construct the payload for the JIRA issue
    payload = {
        "fields": {
            "project": {"key": JIRA_PROJECT_KEY},
            "summary": ticket_data.get("summary"),
            "description": description_adf,
            "issuetype": {"name": ISSUE_TYPE},
        }
    }

    # Convert the payload to a JSON string
    payload_json = json.dumps(payload)

    # Send a POST request to the JIRA API endpoint
    response = requests.post(
        API_ENDPOINT,
        data=payload_json,
        headers=headers,
        auth=HTTPBasicAuth(EMAIL, API_TOKEN),
    )

    # Check for a successful creation (HTTP 201 Created)
    if response.status_code == 201:
        return response.json()
    else:
        return {"error": f"Failed to create ticket: {response.status_code}"}


def handle_event(data):
    return create_jira_ticket(data)
```

**Where to Find Required Values**

* **JIRA\_DOMAIN** – Found in your Jira account URL. Example:\
  `https://mycompany.atlassian.net` → `JIRA_DOMAIN = "mycompany.atlassian.net"`
* **EMAIL** – Your Atlassian login email.
* **API\_TOKEN** – Create from [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens).
* **JIRA\_PROJECT\_KEY** – Found in your project URL or next to the project name.
* **ISSUE\_TYPE** – Must be valid in your Jira project (Story, Task, Bug).

**Test Input**

```json
{
  "summary": "This is to test ticket creation",
  "description": "Created using External API"
}
```

Click **Test API**.&#x20;

**A successful Output Example:**

```json
{
  "id": "10004",
  "key": "EX-5",
  "self": "https://mycompany.atlassian.net/rest/api/3/issue/10004"
}
```

<figure><img src="../../.gitbook/assets/image (39).png" alt=""><figcaption></figcaption></figure>

**Activate the method**\
If the test passes, click **Save Changes**, return to the main API list, and enable the method by toggling **Connect** to green.

<figure><img src="../../.gitbook/assets/Screenshot 2025-08-09 164455.png" alt=""><figcaption></figcaption></figure>

**Test with a character**\
Once activated, test the method in a conversation with your character.\
As seen in the screenshot below, the character successfully created a Jira ticket and returned the ticket key.

<figure><img src="../../.gitbook/assets/Screenshot 2025-08-09 164924 (1).png" alt=""><figcaption></figcaption></figure>

***

## Limitations and Supported Environment

{% hint style="warning" %}
**Supported LLM Models**: GPT-4o, GPT-4o-mini, Claude-3.5, Claude 4.0
{% endhint %}

{% hint style="warning" %}
**Max Execution Time**: 5 seconds
{% endhint %}

{% hint style="warning" %}
**Python Version**: 3.12
{% endhint %}

{% hint style="warning" %}
**Libraries Available**: Standard library + requests
{% endhint %}

***

## Conclusion

By configuring the External API feature, you can transform your characters into powerful, data-driven assistants. From retrieving real-time weather information to creating Jira tickets directly from a conversation, the possibilities are vast. This integration capability enables highly interactive, automated, and intelligent workflows.
