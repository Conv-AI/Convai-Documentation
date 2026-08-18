---
title: Prerequisites
description: >-
  Confirm the Unity version, package dependencies, and Convai account the
  Convai Unity SDK requires before you begin installation.
last_reviewed: "4.5.0"
---

Before installing the Convai Unity SDK, confirm that your environment meets the requirements below. Missing any of these causes installation errors or runtime failures that are harder to diagnose after the fact.

## System requirements

| Requirement         | Minimum                             |
| ------------------- | ----------------------------------- |
| Unity version       | **<code class="expression">space.vars.unity_min_version</code>** |
| Scripting backend   | Mono or IL2CPP                      |
| Internet connection | Required at editor time and runtime |

{% hint style="warning" %}
Unity <code class="expression">space.vars.unity_min_version</code> is a hard floor — there is no supported configuration on an earlier release, including older LTS versions such as Unity 2022 or Unity 2023. If your project targets an older release, upgrade the project to Unity 6 before installing the SDK. There is no workaround.
{% endhint %}

## Required Unity packages

The SDK depends on six Unity packages. Both installation methods (Package Manager and Asset Store) install these automatically — you do not need to add them manually unless you encounter a version conflict.

| Package                           | Minimum version |
| --------------------------------- | ---------------- |
| `com.unity.nuget.newtonsoft-json` | <code class="expression">space.vars.dep_newtonsoft_json_version</code> |
| `com.unity.ugui`                  | <code class="expression">space.vars.dep_ugui_version</code> |
| `com.unity.inputsystem`           | <code class="expression">space.vars.dep_inputsystem_version</code> |
| `com.unity.ai.navigation`         | <code class="expression">space.vars.dep_ai_navigation_version</code> |
| `com.unity.collections`           | <code class="expression">space.vars.dep_collections_version</code> |
| `com.unity.modules.xr`            | <code class="expression">space.vars.dep_modules_xr_version</code> |

If your project already pins any of these packages to an older version in `Packages/manifest.json`, the automatic install fails silently or produces a version conflict. Remove or update the existing version pins before installing the SDK.

## Supported render pipelines

| Render Pipeline                        | Supported |
| -------------------------------------- | --------- |
| Built-in Render Pipeline               | ✓         |
| Universal Render Pipeline (URP)        | ✓         |
| High Definition Render Pipeline (HDRP) | ✓         |

For detailed platform and render pipeline compatibility, see [Compatibility & Requirements](../compatibility-and-requirements/README.md).

## Account requirements

You need an active Convai account and an API key to connect your project to Convai during local development.

1. Create an account at [convai.com](https://convai.com) if you do not have one.
2. Retrieve your API key from the **API Keys** section of the Convai dashboard.
3. Create at least one character in the Convai dashboard and note its **Character ID** — you need it during scene setup.

Your API key is stored in `Assets/Resources/ConvaiSettings.asset`. This is the **API Key** authentication mode, intended for local development in the Unity Editor rather than for a build you distribute. See [Configure the API key](configure-api-key.md) for full setup steps.

If your project ships to testers or players, the SDK also supports **Auth Token** mode, which resolves a short-lived credential per connection instead of shipping your account API key in the build. Review the two modes and decide which one your project needs before you reach scene setup.

{% content-ref url="../authentication/README.md" %}
[Authentication](../authentication/README.md)
{% endcontent-ref %}

## Next steps

Once your environment meets all requirements above, install the SDK.

{% content-ref url="installation.md" %}
[Installation](installation.md)
{% endcontent-ref %}
