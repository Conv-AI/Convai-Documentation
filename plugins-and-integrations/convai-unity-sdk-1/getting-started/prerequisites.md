---
title: Prerequisites
description: >-
  System requirements, Unity version, required packages, and account
  prerequisites for the Convai Unity SDK.
last_reviewed: "4.2.0"
---

Before installing the Convai Unity SDK, confirm that your environment meets the requirements below. Missing any of these will cause installation errors or runtime failures that are harder to diagnose after the fact.

## System requirements

| Requirement         | Minimum                             |
| ------------------- | ----------------------------------- |
| Unity version       | **<code class="expression">space.vars.unity_min_version</code>** |
| Scripting backend   | Mono or IL2CPP                      |
| Internet connection | Required at editor time and runtime |

{% hint style="warning" %}
The Convai Unity SDK requires Unity <code class="expression">space.vars.unity_min_version</code>. If your project is on an older LTS release, upgrade before proceeding.
{% endhint %}

## Required Unity packages

The SDK depends on three Unity packages. Both installation methods (Package Manager and Asset Store) install these automatically — you do not need to add them manually unless you encounter a version conflict.

| Package                           | Minimum Version |
| --------------------------------- | --------------- |
| `com.unity.nuget.newtonsoft-json` | 3.2.2           |
| `com.unity.ugui`                  | 2.0.0           |
| `com.unity.inputsystem`           | 1.18.0          |

If your project already pins `com.unity.inputsystem` or `com.unity.ugui` to an older version in `Packages/manifest.json`, the automatic install will fail silently or produce a version conflict. Remove or update the existing version pins before installing the SDK.

## Supported render pipelines

| Render Pipeline                        | Supported |
| -------------------------------------- | --------- |
| Built-in Render Pipeline               | ✓         |
| Universal Render Pipeline (URP)        | ✓         |
| High Definition Render Pipeline (HDRP) | ✓         |

For detailed platform and render pipeline compatibility, see [Compatibility & Requirements](../compatibility-and-requirements/README.md).

## Account requirements

You need an active Convai account and an API key to connect your project to Convai.

1. Create an account at [convai.com](https://convai.com) if you do not have one.
2. Retrieve your API key from the **API Keys** section of the Convai dashboard.
3. Create at least one character in the Convai dashboard and note its **Character ID** — you will need it during scene setup.

Your API key is stored in `Assets/Resources/ConvaiSettings.asset`. If your project uses source control, decide whether to commit this file based on your team's security policy. See [Configure the API key](configure-api-key.md) for full setup steps and secure-deployment options.

## Next steps

Once your environment meets all requirements above, install the SDK.

{% content-ref url="installation.md" %}
[Installation](installation.md)
{% endcontent-ref %}
