# Gold-standard page skeleton

Use these examples when reviewing or drafting pages. The annotated failure example shows
the most common mistakes with explanations. The gold-standard skeleton shows the correct
structure for a how-to guide.

---

## Wrong — annotated failure example

```md
---
title: Installation Guide
description: This page covers how to install the SDK.
---

# Installation Guide

## Overview

Welcome to the Convai Unity SDK installation guide! The Convai Unity SDK is a really powerful
and seamless solution for adding AI-powered NPC characters to your Unity project. In this guide
we will walk you through everything you need to know.

## Getting started

Before you begin, you may want to make sure you have the following things ready:

- Unity
- An account of some kind
- Package Manager access

## Installing the SDK

Simply open Package Manager and add the package. It's easy and only takes a few minutes to get
up and running.

## Next steps

Click here for more information.
```

**What is wrong and why:**

| Line / element | Problem | Rule broken |
|---|---|---|
| `title: Installation Guide` | Vague, not keyword-first, not unique | Title must be specific and keyword-first (≤ 60 chars) |
| `description: This page covers...` | Forbidden opener; states no outcome | Description must be outcome-focused, not "This page covers" |
| `# Installation Guide` in body | Duplicate H1 — GitBook title is already the H1 | Never use `#` in Markdown body |
| `## Overview` | Forbidden heading | Use a headingless lead paragraph instead |
| "Welcome to..." opener | Filler, marketing voice | Start with what the reader will do, not a greeting |
| "powerful and seamless" | Marketing language | Forbidden in docs |
| "In this guide we will walk you through everything" | Filler opener | State the outcome directly |
| `- Unity` / `- An account of some kind` | Vague prerequisites, no version, no inline code | Prerequisites must be specific and use `inline code` |
| "Simply", "It's easy", "only takes a few minutes" | Dismissive / setup promise | Forbidden |
| "Click here for more information" | Non-descriptive link text | Use descriptive link text; never "click here" |
| No lead paragraph | Body jumps straight to heading after frontmatter | Lead paragraph is required, headingless |
| No code blocks | Installation step has no copy-pasteable content | Every procedure must include working code or precise UI steps |
| No verification step | Reader cannot confirm the task succeeded | Include verification after every procedure |

---

## Right — gold-standard skeleton

```md
---
title: Install the Unity SDK
description: Install the Convai Unity SDK package, add required project settings, and verify that the SDK loads in Unity.
---

Install the Convai Unity SDK into an existing Unity project and confirm that the runtime components are available in the editor.

## Prerequisites

- Unity <code class="expression">space.vars.unity_min_version</code>
- A Convai account
- A project API key from <code class="expression">space.vars.dashboard_url</code>
- Access to Unity Package Manager

{% hint style="info" %}
Use a clean Unity project when evaluating the SDK for the first time. This makes package conflicts easier to isolate.
{% endhint %}

## Install the package

{% stepper %}
{% step %}
### Open Package Manager

In Unity, select **Window > Package Manager**.
{% endstep %}

{% step %}
### Add the SDK package

Select **Add package from git URL**, then enter the package URL for your SDK version.
{% endstep %}

{% step %}
### Import required assets

When Unity prompts you to import required assets, select **Import**.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
The SDK package should now appear in Package Manager with version <code class="expression">space.vars.unity_sdk_version</code>.
{% endhint %}

## Configure the API key

Add your API key to the `ConvaiSettings` asset.

```csharp
// ConvaiSettings is a ScriptableObject located at Assets/Resources/ConvaiSettings.asset
ConvaiSettings.Instance.APIKey = "YOUR_API_KEY";
```

{% hint style="warning" %}
Do not commit API keys to source control. Use environment-specific configuration for shared projects.
{% endhint %}

## Verify the installation

Confirm that:

- The SDK package appears in Package Manager.
- The `ConvaiSettings` asset is present at `Assets/Resources/ConvaiSettings.asset`.
- The editor console has no package resolution errors.

## Troubleshooting

### Package URL cannot be resolved

**Symptom:** Unity shows `Unable to add package`.

**Cause:** The package URL is incorrect, unavailable, or blocked by the network.

**Fix:** Confirm that the URL matches the SDK version you want to install.

**Verify:** Reopen Package Manager and confirm the SDK appears in the package list.

## Next steps

{% content-ref url="../getting-started/configure-api-key.md" %}
[Configure the API key](../getting-started/configure-api-key.md)
{% endcontent-ref %}

{% content-ref url="../getting-started/import-and-run-sample-scenes.md" %}
[Import and run sample scenes](../getting-started/import-and-run-sample-scenes.md)
{% endcontent-ref %}
```

---

## What makes this skeleton correct

| Element | What it does | Rule it satisfies |
|---|---|---|
| `title: Install the Unity SDK` | Specific, keyword-first, sentence case, ≤ 60 chars | Metadata rule |
| `description:` one outcome sentence | 120–160 chars, no "This page covers" | Description rule |
| No `#` in body | GitBook title is the H1 | No body H1 rule |
| Headingless lead paragraph | 1-2 sentences, outcome-focused | Lead paragraph rule |
| `{% hint style="info" %}` prerequisite note | Placed before the task | Hint placement rule |
| `{% stepper %}` with action titles | Short linear procedure | Stepper rule |
| `{% hint style="success" %}` after install | States observable success condition | Verification rule |
| `csharp` code block with context comment | Compilable, realistic, specifies language | Code block rule |
| `{% hint style="warning" %}` before risky action | States consequence explicitly | Warning placement rule |
| Verification section | Bullet list of observable states | Examples/validation rule |
| Troubleshooting with symptom/cause/fix/verify | Exact console message in inline code | Troubleshooting rule |
| `{% content-ref %}` next steps | 2 links, descriptive titles | Cross-linking rule |
| GitBook variables for version/URL | No hard-coded values | Variables rule |
| All class/asset names in `inline code` | `ConvaiSettings`, `ConvaiSettings.asset` | Inline code rule |
