---
title: Browse samples and content
description: Browse, search, and open sample content from the Samples section of the Convai editor window so you can explore bundled examples in Unreal Editor.
last_reviewed: "4.0.0-beta.21"
---

The Samples section of the Convai editor window lists sample items bundled with the plugin. Each item has a name, description, tags, and a featured flag. You can filter the list by search text and open items directly from the window.

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
### Select Samples in the sidebar

Click **Samples** in the navigation sidebar. The samples list loads from the plugin content.
{% endstep %}
{% endstepper %}

## Browse and filter samples

The Samples section displays two groups of items:

- **Featured** — items marked as featured appear in a separate, highlighted group at the top of the list.
- **All samples** — the full list of available sample items.

Each item card shows the item name, a short description, and any associated tags.

To narrow the list, type in the **Search** field at the top of the section. The list filters in real time to show only items whose name, description, or tags match the search text.

## Open a sample

Click an item card to open it. The sample loads in the editor according to its type (for example, a level opens in the viewport, a Blueprint asset opens in the Blueprint editor).

{% hint style="info" %}
Samples are read from plugin content. They are not downloaded at runtime — all content is present once the plugin is installed.
{% endhint %}

## Next steps

{% content-ref url="export-diagnostic-logs.md" %}
[Export diagnostic logs](export-diagnostic-logs.md)
{% endcontent-ref %}
