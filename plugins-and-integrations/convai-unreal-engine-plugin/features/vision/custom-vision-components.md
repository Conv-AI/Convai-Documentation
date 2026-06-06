---
title: Custom vision components
description: Implement the vision interface in C++ to create a custom frame source that any Convai chatbot component can use as a vision input.
last_reviewed: "4.0.0-beta.21"
---

The built-in `UEnvironmentWebcam` covers scene-camera capture for most Unreal Engine use cases. When you need a different image source — a physical webcam feed, an external video stream, a GPU-generated texture, or a pre-compressed image pipeline — you can create a custom component by implementing `IConvaiVisionInterface`. Any component that satisfies the interface is automatically discoverable by `UConvaiChatbotComponent` without any changes to the chatbot.

## When to implement a custom component

`UEnvironmentWebcam` renders from a `USceneCaptureComponent2D` into a `UTextureRenderTarget2D`. This covers the vast majority of in-engine capture scenarios. A custom component is the right choice when:

- Your source is an external SDK (for example, a vendor's native webcam or depth-camera library) that produces raw pixel data outside of UE's texture pipeline.
- Your pipeline already produces compressed frames (JPEG/PNG) and you want to skip the re-compression pass.
- You need to inject a procedural or AI-generated image feed into the conversation.
- You are integrating a non-`UActorComponent` backend (such as a singleton service class) and need full control over the interface implementation.

For any use case that involves a standard UE camera rendering to a render target, use `UEnvironmentWebcam` instead and adjust its `CaptureComponent` properties.

## Choose your base class

| Option | When to use |
|---|---|
| Derive from `UConvaiWebcamBase` | You want a `UActorComponent` with Blueprint-accessible `OnFrameReady`, Inspector-visible `m_MaxFPS` and `bAutoStartVision`, and the `SetErrorCodeAndMessage` error-reporting helper. Covers the majority of custom-source needs. |
| Implement `IConvaiVisionInterface` directly | You need a non-`UActorComponent` integration, or you only need the C++ delegates (`FOnVisionStateChanged`, `FOnFirstFrameCaptured`, `FOnFramesStopped`) and have no Blueprint usage. |

For most custom sources, derive from `UConvaiWebcamBase`. It handles the `Start`/`Stop` state machine, `m_MaxFPS` storage, error tracking, and the `OnFrameReady` Blueprint event, so you only override the methods specific to your image source.

## Interface contract

The table below lists all pure-virtual methods on `IConvaiVisionInterface` (declared in `VisionInterface.h`). When deriving from `UConvaiWebcamBase`, only `CanStart`, `CaptureRaw`, and optionally `CaptureCompressed` and `GetImageTexture` need to be overridden — the base class implements the rest.

| Method | Purpose | Notes |
|---|---|---|
| `void Start()` | Begin capturing. | Transitions state from `Stopped` or `Paused` to `Capturing`. |
| `void Stop()` | End capturing. | Transitions state from `Capturing` or `Paused` to `Stopped`. |
| `EVisionState GetState() const` | Return current lifecycle state. | Called by the chatbot each tick to gate `SendImage`. |
| `void SetMaxFPS(int MaxFPS)` | Set maximum capture FPS. | Cap between 1 and 60; default is 15. |
| `int GetMaxFPS() const` | Return current max FPS. | — |
| `bool IsCompressedDataAvailable() const` | Return `true` if a pre-compressed frame is ready. | When `true`, the chatbot calls `GetCompressedData` instead of `CaptureRaw`. |
| `bool GetCompressedData(int& Width, int& Height, TArray<uint8>& Data)` | Retrieve a pre-compressed frame. | Called only when `IsCompressedDataAvailable()` returns `true`. |
| `bool CaptureCompressed(int& Width, int& Height, TArray<uint8>& Data, float ForceCompressionRatio)` | Capture and compress a frame on demand. | Override if your source already produces compressed bytes; otherwise the base class compresses the output of `CaptureRaw`. |
| `bool CaptureRaw(int& Width, int& Height, TArray<uint8>& Data)` | Capture a raw RGBA frame. | Fill `Data` with row-major RGBA bytes. Return `true` on success. |
| `UTexture* GetImageTexture(ETextureSourceType& TextureSourceType)` | Return the current frame texture. | Set `TextureSourceType` to `RenderTarget2D` or `Texture2D` to match your texture type. |
| `FString GetLastErrorMessage() const` | Return the last human-readable error. | Return an empty string if no error has occurred. |
| `int GetLastErrorCode() const` | Return the last numeric error code. | Return `0` if no error has occurred. |

## Implement from UConvaiWebcamBase

`UConvaiWebcamBase` is declared in `ConvaiWebcamBase.h` (module `ConvaiVisionBase`). Add `ConvaiVisionBase` to your module's `PublicDependencyModuleNames` in `Build.cs` before including it.

{% stepper %}
{% step %}
#### Declare the class

Create a `UActorComponent` subclass that derives from `UConvaiWebcamBase`. Mark it `BlueprintSpawnableComponent` so it appears in the Blueprint component picker.

```cpp
// MyCustomVisionComponent.h
#pragma once

#include "ConvaiWebcamBase.h"
#include "MyCustomVisionComponent.generated.h"

UCLASS(ClassGroup=(Convai), meta=(BlueprintSpawnableComponent))
class MYPROJECT_API UMyCustomVisionComponent : public UConvaiWebcamBase
{
    GENERATED_BODY()

protected:
    virtual bool CanStart() override;
    virtual bool CaptureRaw(int& Width, int& Height, TArray<uint8>& Data) override;

private:
    // Your image source handle — replace with whatever your SDK provides.
    TSharedPtr<FMyImageSource> MyImageSource;
};
```
{% endstep %}

{% step %}
#### Override CanStart

`CanStart` is called by the base class `Start()` before it transitions state. Return `true` only when your source is initialized and ready to produce frames. Call `SetErrorCodeAndMessage` to record a diagnostic message if the source is not ready — this powers `GetLastErrorMessage()` and `GetLastErrorCode()` in Blueprint.

```cpp
// MyCustomVisionComponent.cpp
bool UMyCustomVisionComponent::CanStart()
{
    if (!MyImageSource.IsValid())
    {
        SetErrorCodeAndMessage(1, TEXT("Image source is not initialized."), /*bPrintToLog=*/true);
        return false;
    }
    return true;
}
```

`SetErrorCodeAndMessage(int ErrorCode, const FString& ErrorMessage, bool bPrintToLog)` is a protected helper declared on `UConvaiWebcamBase`. It stores both values so they can be retrieved from Blueprint via **Get Last Error Message** and **Get Last Error Code**.
{% endstep %}

{% step %}
#### Override CaptureRaw

`CaptureRaw` is called by the chatbot each time it needs a frame. Fill `Width`, `Height`, and `Data` with the raw RGBA pixel data from your source (row-major, 4 bytes per pixel). Return `true` on success and `false` if the frame could not be captured.

```cpp
bool UMyCustomVisionComponent::CaptureRaw(int& Width, int& Height, TArray<uint8>& Data)
{
    if (!MyImageSource.IsValid())
        return false;

    MyImageSource->GetRGBAFrame(Width, Height, Data);
    return Data.Num() > 0;
}
```
{% endstep %}

{% step %}
#### (Optional) Override CaptureCompressed

Override `CaptureCompressed` only if your source already produces JPEG or PNG-compressed bytes. This skips the re-compression pass the base class would otherwise apply to the output of `CaptureRaw`, which reduces per-frame CPU cost.

```cpp
bool UMyCustomVisionComponent::CaptureCompressed(
    int& Width, int& Height, TArray<uint8>& Data, float ForceCompressionRatio)
{
    if (!MyImageSource.IsValid())
        return false;

    // Return pre-compressed JPEG directly from the source.
    return MyImageSource->GetJPEGFrame(Width, Height, Data);
}
```

If you do not override `CaptureCompressed`, the base class automatically calls `CaptureRaw` and compresses the result using the `ForceCompressionRatio` parameter.
{% endstep %}
{% endstepper %}

## Register the component with the chatbot

Add the component to the same Actor as the `UConvaiChatbotComponent`. The chatbot calls `FindFirstVisionComponent()` at session start and auto-discovers any component on its Actor that implements `IConvaiVisionInterface`.

- If only one vision component is present on the Actor, no explicit registration is needed.
- If multiple vision components are present, call **Set Vision Component** on the chatbot in `BeginPlay` and pass the specific component you want to use.

{% hint style="info" %}
`bAutoStartVision` is inherited from `UConvaiWebcamBase` and works on custom components exactly as it does on `UEnvironmentWebcam`. Set it to `true` in the Inspector or call `Start()` from `BeginPlay` to begin capture automatically when the level starts.
{% endhint %}

## Next steps

{% content-ref url="vision-blueprint-reference.md" %}
[Vision Blueprint reference](vision-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="frame-sources.md" %}
[Vision frame sources](frame-sources.md)
{% endcontent-ref %}

{% content-ref url="how-vision-works.md" %}
[How vision works](how-vision-works.md)
{% endcontent-ref %}
