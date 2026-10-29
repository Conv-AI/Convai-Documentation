---
title: Scene Auto Tagger scripting API
description: Tag scene objects from Editor code and apply approved results, or send your own images to Convai Vision from the Editor or a player build.
last_reviewed: "5.0.0-preview"
---

`Convai.Editor.SceneTagging.ConvaiSceneTagger` exposes the window's analysis pipeline for Editor tooling. It supports Windows and macOS Editors in Edit mode. Call from the Unity main thread and await the task; blocking on `.Result` can prevent capture frames from progressing.

To send your own images to Convai Vision from the Editor or a player build, use `ConvaiObjectAutotagClient`. See [Call Convai Vision directly](#call-convai-vision-directly).

{% hint style="warning" %}
`ConvaiSceneTagger` depends on the same preview Core and service as the window. The reviewed Core is `unsigned-internal-prerelease` and has `customerDistributionReady: false`. An SDK/Core release owner must approve distribution and service availability before this workflow is presented as a supported public release.
{% endhint %}

## Analyze without changing the scene

The following are API signatures, not standalone scripts. Put caller code in an Editor assembly or guard it with `UNITY_EDITOR`.

```csharp
public static Task<ConvaiSceneTagResult> TagAsync(
    ConvaiSceneTagRequest request,
    IProgress<ConvaiSceneTagProgress> progress = null,
    CancellationToken cancellationToken = default)

public static Task<ConvaiSceneDescriptionResult> DescribeViewAsync(
    string characterId, Camera camera = null,
    CancellationToken cancellationToken = default)
```

`ConvaiSceneTagger` itself is Editor-only; its request and result types live in `Convai.Runtime.SceneTagging`. `DescribeViewAsync` uses the supplied camera or last active Scene view to draft environment text. Neither method changes scene components.

| Request member | Constraint |
| --- | --- |
| `CharacterId` | Valid character GUID with service access |
| `Targets` | 1–300 `ConvaiSceneTagTarget` entries |
| `SceneDescription` | Up to 800 characters |
| `Focus` | Up to 400 characters |
| `Quality` | `Fast` by default, or `Accurate` |
| `IncludeLowInformation` | Whether captures with little visual detail may be analyzed |

Create a target with `new ConvaiSceneTagTarget(id, anchor, renderers, note)`. IDs and anchors must be unique within a request. Optional renderer sets must be nonempty and cannot share renderers across targets. A target accepts up to 4,096 renderers and a note up to 300 characters. Inactive, unloaded, uncapturable, player, or character objects can be ineligible.

Progress reports `Phase`, `Completed`, and `Total` on the main thread. Phases are `Capturing` and `Analyzing`. Cancellation is also triggered by script reload or entering Play mode; an in-flight Vision call completes before the task finishes cancellation.

## Inspect every result

`ConvaiSceneTagResult` exposes `Succeeded`, `Failure`, `Message`, and `Objects`. A successful run does not imply every object was tagged. Each object's `Status`, `Failure`, `Message`, and `IsTagged` explain its outcome; tagged entries include `Name`, `Description`, and `Confidence`.

| Status | Meaning |
| --- | --- |
| `Tagged` | A name and description were returned |
| `NotAnalyzed` | The run stopped before this target was analyzed |
| `NotEligible` | The target cannot be captured under the API's object rules |
| `CaptureFailed` | No usable capture was produced |
| `LowInformation` | Capture was not submitted because it lacked useful visual detail |
| `AnalysisFailed` | No usable description was returned |

Run-level failures include `InvalidRequest`, `MissingApiKey`, `Unauthorized`, `UsageLimitReached`, `RateLimited`, `ServiceError`, `NetworkError`, `InvalidResponse`, and `NativeCoreUnavailable`. `DescribeViewAsync` can also return `CaptureFailed`. Invalid null arguments, thread/mode misuse, and cancellation are exceptions rather than result failures.

## Apply approved results

```csharp
public static ConvaiSceneTagApplyResult Apply(
    IEnumerable<ConvaiSceneTagObjectResult> results,
    ConvaiSceneTagApplyOptions options = null)
```

Review results first, and use `WithText(name, description)` to make explicit corrections. Apply accepts results produced by this Editor session, with no duplicate tagged object in the same call. It writes a single Undo step and marks scenes dirty without saving.

`ConvaiSceneTagApplyOptions` defaults `IncludeSpatialContext`, `EnableGaze`, and `CreateActionTargets` to true. Inspect each returned `Items` entry's `Id` and `Outcome`; results can preserve authored metadata, edited companions, or an existing logical group instead of applying. Changed geometry, transforms, or materials require a fresh capture. Text is trimmed and fitted to 64/320 UTF-16 authoring limits without splitting surrogate pairs.

The API's per-target Apply does not replace the window's multi-object grouping review. Runtime payload size, targeting, navigation, and conversational behavior still require their own checks after authoring.

## Call Convai Vision directly

`ConvaiObjectAutotagClient` sends your own PNG images and an optional prompt to Convai Vision and returns the objects Convai names in each image. Use it when you capture the images yourself or when the code must run in a player build. It captures nothing, changes nothing in the scene, and needs no native libraries. It runs in the Editor and in player builds, WebGL included.

Use `ConvaiSceneTagger` instead when the Editor should capture scene objects and apply the results as World Object metadata.

| | `ConvaiSceneTagger` | `ConvaiObjectAutotagClient` |
| --- | --- | --- |
| Runs in | Windows and macOS Editors, in Edit mode | The Editor and player builds, WebGL included |
| Images | Captured from scene objects | Your PNG files, one to three per request |
| Prompt | Protected templates; you cannot supply your own | Yours, sent as written, or the service's own when you pass `null` |
| Credential | The API key saved in **Edit > Project Settings > Convai SDK** | The API key or auth token you pass in |
| Result | Per-object results that `Apply` can write with Undo | The objects named in each image; nothing in the scene changes |

### Send images and read the objects

The example sends one numbered contact sheet and returns the objects Convai Vision names in it. Compile it in an assembly definition that references both `Convai.Runtime` and `Convai.Api.Transport`. `Convai.Api.Transport` is not auto-referenced, so the same code in the default `Assembly-CSharp` assembly fails to compile with error CS0012.

```csharp
using System.Collections.Generic;
using System.Threading.Tasks;
using Convai.Runtime.SceneTagging;
using UnityEngine;

public static class PartSheetNamer
{
    public static async Task<IReadOnlyList<ConvaiObjectAutotagObject>> NameAsync(string authToken, string characterId, byte[] sheetPng)
    {
        using var client = new ConvaiObjectAutotagClient(ConvaiObjectAutotagOptions.WithAuthToken(authToken));
        var request = new ConvaiObjectAutotagRequest(
            characterId,
            new[] { new ConvaiObjectAutotagImage("sheet-01.png", sheetPng) },
            "Cell 1 shows the whole machine for context. Name the part in every other numbered cell. " +
            "Copy each cell's printed number and ID exactly.");

        ConvaiObjectAutotagResult result = await client.TagAsync(request);
        if (!result.Succeeded)
        {
            Debug.LogError($"Convai Vision failed ({result.Failure}, HTTP {result.HttpStatus}, reference '{result.ReferenceId}'): {result.Message}");
            return new ConvaiObjectAutotagObject[0];
        }
        return result.Images[0].Objects;
    }
}
```

On success, `result.Images[0].Objects` holds one `ConvaiObjectAutotagObject` for each part Convai named on the sheet. `Index` is the printed cell number, and `EchoId` is the ID the model read next to the object. Compare both with the number and ID you printed in that cell before you trust a match.

All types are in `Convai.Runtime.SceneTagging`.

| Type | Purpose |
| --- | --- |
| `ConvaiObjectAutotagClient` | Sends a request with `TagAsync` and returns a result. Implements `IDisposable`. |
| `ConvaiObjectAutotagOptions` | Credential, host, timeout and retry settings. Create it with `WithApiKey` or `WithAuthToken`. |
| `ConvaiObjectAutotagCredentialKind` | `ApiKey` or `AuthToken`: which credential header the client sends. |
| `ConvaiObjectAutotagRequest` | The character ID, images, prompt and model. |
| `ConvaiObjectAutotagImage` | One PNG with its file name. |
| `ConvaiObjectAutotagResult` | The outcome of one call: success or failure, HTTP status, reference ID and attempt count. |
| `ConvaiObjectAutotagImageResult` | The objects named in one image, with that image's `FileName`. |
| `ConvaiObjectAutotagObject` | One named object: `Index`, `EchoId`, `Name`, `Description` and `Confidence`. |

### Request limits

`TagAsync` checks the request before it sends anything. A request that breaks a rule returns `InvalidRequest` with `HttpStatus` and `Attempts` of `0`.

| Request part | Rule |
| --- | --- |
| `characterId` | A Convai character ID in UUID form. The character's context informs the answers. |
| `images` | One to `ConvaiObjectAutotagRequest.MaxImages` (3) PNG images. The request copies the list but not the `png` byte arrays, so do not change an array while the request runs. |
| Each PNG | At most `MaxImageBytes` (10 MiB) and `MaxImagePixels` (64,000,000 pixels, width times height). The client reads the PNG header and refuses a file that is not a PNG. |
| `FileName` | Unique within the request. ASCII letters, digits, `.`, `-` and `_` only, with no folders, so the service returns the name unchanged. |
| `prompt` | Optional, not blank, and at most `MaxPromptBytes` (500,000 UTF-8 bytes). Sent as written with every image, so describe the image layout in it. `null` uses the service's own prompt. |
| `model` | Optional. A Gemini model name that starts with `gemini-`, such as `gemini-3.5-flash`. `null` uses the service's default. |

The service scales each image down to 2048 pixels on its longest side.

### Configure credentials and options

`ConvaiObjectAutotagOptions.WithApiKey` sends the key as `CONVAI-API-KEY`. `WithAuthToken` sends the token as `API-AUTH-TOKEN`. The credential travels only in that request header, and the SDK never logs it.

{% hint style="danger" %}
A player build that carries an API key exposes the key to anyone who has the build. Ship players with `WithAuthToken` and a token your own server issues, and keep `WithApiKey` for the Editor, tools and trusted desktop builds. See [Mint auth tokens on your backend](../../authentication/mint-tokens-on-your-backend.md).
{% endhint %}

Both factory methods take the same optional settings after the credential.

| Parameter | Default | Rule |
| --- | --- | --- |
| `baseUri` | `ConvaiObjectAutotagOptions.ProductionBaseUri`, which is `https://api.convai.com/` | An absolute URI. The client appends `vision/object-autotag`. The client does not read the project **Environment** setting, so pass `baseUri` to use another host. |
| `timeout` | 120 seconds | How long one attempt may take. Greater than zero and at most 24 days. |
| `maxRetriesOn429` | `3` | How many times a rate-limited request is sent again. Zero or more. |
| `retryDelay` | 20 seconds | The wait before each such retry. From zero to 24 days. |

`WithApiKey` and `WithAuthToken` throw `ArgumentException` for a blank credential or a relative `baseUri`. They throw `ArgumentOutOfRangeException` for a `timeout`, retry count or `retryDelay` outside these ranges.

Create the client with `new ConvaiObjectAutotagClient(options)`. The optional second argument is an `IConvaiApiTransport` from `Convai.Api.Transport`. When you omit it, the client uses `UnityWebRequest` in a WebGL player and `HttpClient` elsewhere. Pass a `UnityWebRequestApiTransport` only in a WebGL player. Elsewhere, the client resumes off the main thread after a retry wait, where `UnityWebRequest` cannot run. Dispose the client when you are done; `Dispose` releases a transport only if the client created it.

### Retries, timeouts, and cost

The service runs one model call per image, and a successful request counts against the plan's usage. For that reason, the client retries only HTTP 429 (rate limited), which the service refuses before any model runs.

- **Rate-limited requests.** The client sends the same request again up to `MaxRetriesOn429` times, so a call makes at most four attempts by default. Each retry waits `RetryDelay`, or the `Retry-After` header's value when that is longer. `Retry-After` can be whole seconds or an HTTP date. In a WebGL player the browser hides `Retry-After`, so the client waits `RetryDelay` before each retry.
- **Long waits.** Outside WebGL, a `Retry-After` longer than `ConvaiObjectAutotagClient.MaxRetryAfter` (five minutes) is not waited out. The call returns `RateLimited` at once.
- **Server errors and timeouts.** The client returns them without a retry, because the model calls may already have run.
- **Timeouts.** Each attempt is abandoned after `Timeout`, in WebGL players too. The result has `Failure` set to `NetworkError` and `TimedOut` set to `true`, and the service may still have processed the request.
- **Cancellation.** The `CancellationToken` you pass to `TagAsync` also cancels the wait before a retry.

The service answers for all images or for none. If one image fails, the whole request fails and `Images` is empty. Send one image per request when each result must survive on its own, and keep successful results instead of asking again.

### Read the result and handle failures

`TagAsync` reports service and network problems as values in the result. It throws `ArgumentNullException` for a null request, `ObjectDisposedException` after `Dispose`, and `OperationCanceledException` when your cancellation token is cancelled.

| `ConvaiObjectAutotagResult` member | Meaning |
| --- | --- |
| `Succeeded` | `true` when the service answered for every image. |
| `Images` | One `ConvaiObjectAutotagImageResult` for each request image, in request order. Empty when the call failed. |
| `Failure` | A `ConvaiSceneTagFailure`. `None` on success. |
| `Message` | What went wrong and what to do next, in plain language. Empty on success. It never contains the service's response body or a credential. |
| `HttpStatus` | The HTTP status of the last attempt. `0` when nothing was sent or no answer arrived. |
| `ReferenceId` | The `Reference ID` that Convai returned with a failed request. Quote it to Convai support. Empty when none came back. |
| `Attempts` | How many requests were sent: `0` when the request was refused before sending, more than `1` after rate-limited retries. |
| `TimedOut` | `true` when the last attempt was abandoned after `Timeout`. |

Each `ConvaiObjectAutotagImageResult` has the image's `FileName` and its `Objects`, which can be empty. Each `ConvaiObjectAutotagObject` has `Index` (1-based), `EchoId`, `Name` (one to three words), `Description` (one or two sentences) and `Confidence` (0 to 1). The SDK creates these result types; you only read them.

`Failure` is the same `ConvaiSceneTagFailure` enum that `ConvaiSceneTagResult` uses. This client returns only the values below, never `MissingApiKey`, `NativeCoreUnavailable` or `CaptureFailed`.

| `Failure` | When it happens |
| --- | --- |
| `InvalidRequest` | The request broke a limit above and was not sent, or the answer was HTTP 400, 404, 413 or 422. |
| `Unauthorized` | HTTP 401: Convai rejected the credential, or the credential has no access to the character or to Convai's core APIs. |
| `UsageLimitReached` | HTTP 403: the plan's usage limit is reached. |
| `RateLimited` | HTTP 429 after the last retry, or, outside WebGL, a `Retry-After` longer than five minutes. |
| `ServiceError` | Any other HTTP status, 5xx included. HTTP 502, 503 and 504 usually mean the request took too long; send fewer images. |
| `NetworkError` | No answer arrived: Convai could not be reached, or the attempt passed `Timeout`. |
| `InvalidResponse` | HTTP 2xx, but the answer did not list every image by its file name, or an object was incomplete or out of range. |

## Next steps

{% content-ref url="scene-auto-tagger-window-reference.md" %}
[Scene Auto Tagger window reference](scene-auto-tagger-window-reference.md)
{% endcontent-ref %}
{% content-ref url="scripting-api-reference.md" %}
[Scene metadata scripting API](scripting-api-reference.md)
{% endcontent-ref %}
