---
description: Utility Functions - Blueprint Reference for Convai Unreal Engine integration.
---

# Utility Functions

### Create Character

* **Description:** Create a new character and get the character ID for it.

<figure><img src="../../../.gitbook/assets/image (145).png" alt=""><figcaption></figcaption></figure>

**Inputs:**

* **Char Name:** Name of the character.
* **Voice:** Voice name \[MALE/FEMALE].
* **Backstory:** Backstory for the new character.

**Outputs:**

#### ✅ \[On Success]

* **Char ID:** character id for the new character.

#### ⛔ \[On Failure]&#x20;

_Nothing is returned, check logs for details on why it failed._



### Get All Character IDs

* **Description:** Get a list of character IDs belonging to the user.

<figure><img src="../../../.gitbook/assets/image (138).png" alt=""><figcaption></figcaption></figure>

**Outputs:**

#### ✅ \[On Success]

* C**har IDs**: list of characters.

#### ⛔ \[On Failure]&#x20;

_Nothing is returned, check logs for details on why it failed._

### Get Character Details

* **Description:** Fetch all details of a character including backstory, voice, etc.

<figure><img src="../../../.gitbook/assets/image (124).png" alt=""><figcaption></figcaption></figure>

**Inputs:**

* **Char ID:** Character ID for which to fetch all the details.

**Outputs:**

#### ✅ \[On Success]

* **Character Name:** Name of your character.&#x20;
* **Voice Type:** Voice name.&#x20;
* **Backstory:** Character backstory.
* **Has Ready Player Me Link:** True if the avatar is configured on the website.
* **Ready Player Me Link:** The avatar link to be used to download.

#### ⛔ \[On Failure]&#x20;

_Nothing is returned, check logs for details on why it failed._

### Update Character&#x20;

* **Description:** Update a particular character.

<figure><img src="../../../.gitbook/assets/image (116).png" alt=""><figcaption></figcaption></figure>

**Inputs:**

* **Char ID:** Character ID to be updated.
* **New Voice:** Voice name or \[MALE/FEMALE].
* **New Backstory:** Updated backstory.
* **New Char Name:** Name of the character.

{% hint style="info" %}
For the list of supported voices, please refer to the [Voice List API](../../../reference/core-api-reference/voice-list-api.md).
{% endhint %}

{% hint style="info" %}
To update a subset of properties, such as Voice and Name only, leave the other fields empty and the update will only affect the specified fields with values.
{% endhint %}

**Outputs:**

#### ✅ \[On Success]

_Nothing is returned._

⛔ \[On Failure]&#x20;

_Nothing is returned, check logs for details on why it failed._
