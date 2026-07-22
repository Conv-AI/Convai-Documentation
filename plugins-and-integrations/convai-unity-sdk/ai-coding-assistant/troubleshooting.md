---
title: Troubleshoot AI coding assistant setup
description: >-
  Diagnose and fix Unity MCP bridge reconnects, tool registry refreshes,
  stale tool rejections, and Unity AI Assistant install failures in the
  Convai Unity SDK.
last_reviewed: "4.4.0"
---

The Convai Unity SDK's AI coding integration depends on three things staying in sync: a compatible Unity AI Assistant package, the packaged `convai-unity-sdk` skill, and an exact 20-tool catalog registered with Unity's MCP server. Open `Convai > AI Coding Setup` to open the AI Coding section of the Convai Editor window and see the health of all three, with per-row `Fix` buttons to repair them.

{% hint style="info" %}
`Convai > AI Coding Setup` never starts a repair or writes managed instruction files automatically. Each `Fix` button click runs one repair step, and a repair never exits Play Mode for you — exit Play Mode yourself before retrying.
{% endhint %}

## Read the AI Coding section status

The **Setup Health** card shows four status rows: `Unity 6000+`, `Unity AI Assistant`, `Packaged Convai Skill`, and `Convai MCP Tools`. Each unready row shows a `Fix` button when a repair path exists for it. The `Convai MCP Tools` row's detail text tells you which case you're in:

- `<count>/20 registered` — the catalog is healthy.
- `<count>/20; install Unity AI Assistant first` — the Assistant package itself is not ready yet; fix that row first.
- `<count>/20; <issue>` — the Assistant is ready, but the registered tool set doesn't match the expected 20 tools; `<issue>` lists exactly what's wrong.

A `Fix` button stays disabled only while a repair it started is already running. Clicking `Fix` while Unity is compiling, updating packages, or in Play Mode does not disable the button beforehand — it posts a status message naming the blocking condition and does not start the repair.

A repair also posts its own summary message beneath the rows once it finishes — for example `AI coding setup ready. 20/20 Convai tools registered.` for a completed tool-registration repair. This summary message is separate from each row's own detail text described above.

## Unity MCP bridge doesn't reconnect after a tool repair

A `Convai MCP Tools` repair finishes by restarting Unity's MCP bridge (`Unity.AI.MCP.Editor.UnityMCPBridge`) so external MCP clients — IDE agents connected over stdio or a socket — see the refreshed catalog without you needing to restart Unity. If the bridge was not running when the repair completed, Convai treats that as nothing to reconnect and reports success without a reconnect message. If the bridge was running, Convai stops and restarts it; if that restart throws, the repair completes the tool registration but reports the bridge failure separately, and an external client keeps seeing the old catalog until you resolve it.

## Convai MCP Tools doesn't register after a registry refresh

A tool-registration repair calls Unity's MCP tool registry to refresh its list, then forces an asset refresh and requests a script recompile, then polls for up to 60 seconds waiting for the expected 20 tools to appear. While polling, Convai retries the registry refresh roughly once per second, so a single manual refresh is rarely needed on top of clicking `Fix`. If the registry type itself can't be found — for example because Unity's MCP Server package isn't installed or hasn't finished compiling — the refresh reports that the registry isn't loaded, and no amount of retrying resolves it until the package is present.

## The tool catalog is rejected even though the count matches

Convai validates the registered tool set by exact name, not by count. The expected set is the 20 `Convai_`-prefixed names mirrored from the SDK's tool catalog. If the registered set has the right number of tools but the wrong names — for example stale names left behind by a partially completed SDK update, or an older SDK version's tools that never got replaced — the `Convai MCP Tools` row still reports unready and lists which names are missing and which are unexpected. Re-running `Fix` forces another registry refresh and recompile; if the mismatch persists after that, reimport or update the Convai SDK package so the registered names match the current release's catalog.

## Unity AI Assistant package fails to install

Fixing the `Unity AI Assistant` row installs a specific pinned package version through Unity Package Manager. That install can fail in three distinct ways:

- The install request itself can't start (for example a Package Manager operation is already in progress or the manifest is in a bad state) — the section reports the exception message directly.
- Unity Package Manager rejects or fails the install (network failure, registry unreachable, version conflict) — the section reports Package Manager's own error message, or a generic fallback if Package Manager didn't provide one.
- Package Manager reports success, but the resulting installed version still falls outside Convai's accepted range — after the 60-second repair window elapses, the section reports that the Assistant is still unavailable and asks you to check Package Manager and the Editor log.

{% hint style="warning" %}
Convai only accepts a Unity AI Assistant version between `2.13.0` and `3.0.0`. A `2.13.0` pre-release build must be `pre.2` or later to count as compatible; any version strictly between `2.13.0` and `3.0.0` is accepted regardless of pre-release tag; and `3.0.0` itself is accepted only as a pre-release, never the final release.
{% endhint %}

## Troubleshooting table

| Symptom | Likely cause | Fix | Verify |
|---|---|---|---|
| `Convai MCP Tools` row shows `<count>/20; install Unity AI Assistant first` | The Unity AI Assistant package isn't installed, or its version is outside Convai's accepted range | Click `Fix` on the `Unity AI Assistant` row first; the tools repair only becomes available once the Assistant is ready | The `Unity AI Assistant` row shows `Ready`, then the `Convai MCP Tools` repair becomes available |
| `Fix` button stays disabled | A repair started by that button is already running | Wait for the current repair to finish | The button becomes clickable again |
| Clicking `Fix` does nothing and a warning message appears | Unity is compiling, updating packages, or Play Mode is active | Wait for the compile or package update to finish, or exit Play Mode, then click `Fix` again | The warning message clears and the repair proceeds |
| Assistant repair reports `Could not start Unity AI Assistant installation` with an exception message | Unity Package Manager could not begin the install request | Resolve the reported exception (often a Package Manager operation already in progress), then click `Fix` again | The status message changes to the installing message, then to a result |
| Assistant repair reports `Unity AI Assistant installation failed` with a Package Manager error | Unity Package Manager rejected or could not complete the install (network, registry, or version conflict) | Resolve the reported Package Manager error, then click `Fix` again | The `Unity AI Assistant` row shows the installed version and `Ready` |
| Assistant repair reports the Assistant is `still unavailable after the package refresh` | The install completed per Package Manager, but the resulting version is outside `2.13.0`–`3.0.0` | Check the installed version in Package Manager; install a version inside the accepted range | Reopening `Convai > AI Coding Setup` shows the `Unity AI Assistant` row as ready |
| `Convai MCP Tools` row shows `<count>/20; <issue>` where `<count>` equals 20 | The registered tool set has the right count but includes missing or unexpected `Convai_`-prefixed names (stale entries from a prior version) | Click `Fix` to force another registry refresh and recompile; if it persists, reimport or update the Convai SDK package | The row reads `20/20 registered` with no issue text |
| Registry refresh reports the tool registry `is not loaded` | Unity's MCP Server package isn't installed, or its assemblies haven't finished compiling | Install or enable Unity's MCP Server package and let Unity finish compiling, then retry `Fix` | The registry refresh no longer reports this message |
| Registry refresh reports the tool registry `has no compatible RefreshTools method` | The installed Unity MCP Server version doesn't expose the reflection API Convai expects | Update Unity's MCP Server package to a version compatible with this Convai SDK release | Registry refresh completes without this message |
| Repair times out reporting the tool catalog is `unhealthy` after the Assistant loaded | The 60-second repair window elapsed before the registered names matched the expected 20 | Click `Fix` again; a fresh Assistant install sometimes needs one more Unity compile pass | Repair completes with `AI coding setup ready. 20/20 Convai tools registered.` |
| Tools reach `20/20` but the row reports `Unity MCP bridge reconnect failed` | Restarting `Unity.AI.MCP.Editor.UnityMCPBridge` threw, or its `Stop`/`Start`/`IsRunning` lifecycle API is missing | Check the Editor log for the reported bridge error; confirm the Unity MCP Server package exposes a compatible bridge lifecycle | The row reports `AI coding setup ready` with `Unity MCP bridge reconnected` |
| An external MCP client (IDE agent) still shows the old tool list after a repair completes | The bridge wasn't running when the repair finished, so nothing needed reconnecting, or the client cached the catalog before the bridge restarted | Reconnect or restart the external MCP client | The client's tool list matches the current 20-tool catalog |
| `Packaged Convai Skill` row stays unready reporting the skill `is still missing` | `AIAssistantSkills/convai-unity-sdk/SKILL.md` isn't present in the resolved Convai SDK package folder (interrupted install or corrupted package cache) | Reimport or update the Convai SDK package through Package Manager, then click `Fix` | The row shows the `SKILL.md` path and `Ready` |

## Next steps

{% content-ref url="README.md" %}
[AI coding assistant](README.md)
{% endcontent-ref %}

{% content-ref url="quick-start.md" %}
[AI coding assistant quick start](quick-start.md)
{% endcontent-ref %}

{% content-ref url="mcp-tools-reference.md" %}
[MCP tools reference](mcp-tools-reference.md)
{% endcontent-ref %}
