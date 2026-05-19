---
description: >-
  System requirements, Unity version, required packages, and account
  prerequisites for the Convai Unity SDK.
---

# Prerequisites

## What You Need Before Installing

Before installing the Convai Unity SDK, confirm that your environment meets the requirements below. Missing any of these will cause installation errors or runtime failures that are harder to diagnose after the fact.

## System Requirements

| Requirement         | Minimum                             |
| ------------------- | ----------------------------------- |
| Unity version       | **2023.1** or later                 |
| Scripting backend   | Mono or IL2CPP                      |
| Internet connection | Required at editor time and runtime |

{% hint style="warning" %}
The Convai Unity SDK does not support Unity versions earlier than 2023.1. If your project is on an older LTS release, upgrade to Unity 2023.1 before proceeding.
{% endhint %}

## Required Unity Packages

The SDK depends on three Unity packages. Both installation methods (Package Manager and Asset Store) install these automatically — you do not need to add them manually unless you encounter a version conflict.

| Package                           | Minimum Version |
| --------------------------------- | --------------- |
| `com.unity.nuget.newtonsoft-json` | 3.2.2           |
| `com.unity.ugui`                  | 2.0.0           |
| `com.unity.inputsystem`           | 1.18.0          |

{% hint style="warning" %}
If your project already pins `com.unity.inputsystem` or `com.unity.ugui` to an older version in `Packages/manifest.json`, the automatic install will fail silently or produce a version conflict. Remove or update the existing version pins before installing the SDK.
{% endhint %}

## Supported Render Pipelines

| Render Pipeline                        | Supported |
| -------------------------------------- | --------- |
| Built-in Render Pipeline               | ✓         |
| Universal Render Pipeline (URP)        | ✓         |
| High Definition Render Pipeline (HDRP) | ✓         |

For detailed platform and render pipeline compatibility, see [Compatibility & Requirements](/broken/pages/2c6f9c222f765c27a8cd5ef5374da7c806e47b0e).

## Account Requirements

You need an active Convai account and an API key to connect your project to Convai.

1. Create an account at [convai.com](https://convai.com/) if you do not have one.
2. Retrieve your API key from the **API Keys** section of the Convai dashboard.
3. Create at least one character in the Convai dashboard and note its **Character ID** — you will need it during scene setup.

{% hint style="info" %}
Your API key is a project-level credential stored in `Assets/Resources/ConvaiSettings.asset`. Do not commit this file to a public repository.
{% endhint %}

## Next Steps

Once your environment meets all requirements above, install the SDK.

{% content-ref url="/broken/pages/264e25aab5391b818c55f5f1a3eb5ddf8ee7cbb9" %}
[Broken link](/broken/pages/264e25aab5391b818c55f5f1a3eb5ddf8ee7cbb9)
{% endcontent-ref %}
