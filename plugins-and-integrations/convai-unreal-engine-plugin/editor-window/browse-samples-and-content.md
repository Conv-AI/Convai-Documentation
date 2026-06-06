---
title: Browse samples and content
description: Browse, search, and open sample projects from the Samples section of the Convai editor window to explore example content and assets in Unreal Editor.
last_reviewed: "4.0.0-beta.21"
---

The Samples section of the Convai editor window lists sample projects and content items available for the plugin. Each item shows its name, a short description, and associated tags. Featured items are highlighted separately at the top of the list. You can search and filter the list and open items directly from the window.

## Prerequisites

- Convai Unreal Engine plugin installed and enabled.
- Signed in through the Convai editor window (see [Sign in and manage your account](sign-in-and-account.md)).

## Open the Samples section

{% stepper %}
{% step %}
### Open the Convai editor window

Click **Convai Editor** in the Level Editor toolbar, or select **Window > Convai > Open Convai Editor**.
{% endstep %}

{% step %}
### Select Samples in the navigation bar

Click **Samples** in the navigation bar. The samples list loads from the content feed.
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
**Screenshot required before publishing:** Capture the Samples section as it appears after loading. The image must show the Featured group at the top, the All Samples list below, and the Search field.
{% endhint %}

<figure><img src="../../../.gitbook/assets/TODO-convai-editor-samples-section.png" alt="The Samples section of the Convai editor window showing Featured and All Samples groups with a search field at the top"><figcaption><p>TODO: Replace with screenshot of the Samples section showing the Featured group, All Samples list, and Search field.</p></figcaption></figure>

## Browse and filter samples

The Samples section displays two groups of items:

- **Featured** — highlighted items that appear at the top of the list.
- **All samples** — the full list of available sample items.

Each item card shows the item name, a short description, and any associated tags.

To narrow the list, type in the **Search** field at the top of the section. The list filters in real time to show only items whose name, description, or tags match the search text.

## Open a sample

Click an item card to open it. The sample loads in the editor according to its type — for example, a level opens in the viewport and a Blueprint asset opens in the Blueprint editor.

{% hint style="info" %}
Sample items are loaded via the plugin's content feed. An internet connection is required for the list to populate.
{% endhint %}

## Next steps

{% content-ref url="export-diagnostic-logs.md" %}
[Export diagnostic logs](export-diagnostic-logs.md)
{% endcontent-ref %}
