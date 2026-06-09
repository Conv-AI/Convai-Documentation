---
title: Custom vision components
description: Implement a C++ frame source component for custom Unreal image pipelines that need to provide scene frames to a Convai chatbot.
last_reviewed: "4.0.0-beta.21"
---

The built-in `UEnvironmentWebcam` covers scene capture from a `USceneCaptureComponent2D`. When your project needs a different image source, create a custom `UActorComponent` that implements `IConvaiVisionInterface` so `UConvaiChatbotComponent` can discover or register it.

## When to implement a custom component

`UEnvironmentWebcam` renders from a `USceneCaptureComponent2D` into a `UTextureRenderTarget2D`. This covers the vast majority of in-engine capture scenarios. A custom component is the right choice when:

- Your source is an external SDK (for example, a vendor's native webcam or depth-camera library) that produces raw pixel data outside of UE's texture pipeline.
- Your pipeline already produces image bytes and you need full control over how those bytes are converted to the raw RGBA data sent by the chatbot.
- You need to inject a procedural or AI-generated image feed into the conversation.
- You are integrating a non-`UActorComponent` backend and need a component wrapper that exposes it to the chatbot.

For any use case that involves a standard UE camera rendering to a render target, use `UEnvironmentWebcam` instead and adjust its `CaptureComponent` properties.

## Choose your base class

| Option | When to use |
|---|---|
| Derive from `UConvaiWebcamBase` | You want a `UActorComponent` with Blueprint-accessible `OnFrameReady`, Inspector-visible `m_MaxFPS` and `bAutoStartVision`, and the `SetErrorCodeAndMessage` error-reporting helper. Covers the majority of custom-source needs. |
| Implement `IConvaiVisionInterface` directly on a component | You need a component that does not inherit `UConvaiWebcamBase`, but still needs to register through `SetVisionComponent(UActorComponent*)` or Actor component discovery. |

For most custom sources, derive from `UConvaiWebcamBase`. It handles the `Start`/`Stop` state machine, `m_MaxFPS` storage, error tracking, and the `OnFrameReady` Blueprint event, so you only override the methods specific to your image source.

## Interface contract

The table below lists all pure-virtual methods on `IConvaiVisionInterface`, declared in `VisionInterface.h`. When deriving from `UConvaiWebcamBase`, override `CanStart`, `CaptureRaw`, and optionally `GetImageTexture` or `CaptureCompressed` if your source needs them.

| Method | Purpose | Notes |
|---|---|---|
| `void Start()` | Begin capturing. | Transitions state from `Stopped` or `Paused` to `Capturing`. |
| `void Stop()` | End capturing. | Transitions state from `Capturing` or `Paused` to `Stopped`. |
| `EVisionState GetState() const` | Return current lifecycle state. | Called by the chatbot each tick to gate `SendImage`. |
| `void SetMaxFPS(int MaxFPS)` | Set maximum capture FPS. | `UConvaiWebcamBase` rejects values `<= 0`; default is `15`. |
| `int GetMaxFPS() const` | Return current max FPS. | — |
| `bool IsCompressedDataAvailable() const` | Return `true` if a pre-compressed frame is ready. | Part of the interface contract. The verified chatbot send path uses `CaptureRaw()`. |
| `bool GetCompressedData(int& Width, int& Height, TArray<uint8>& Data)` | Retrieve a pre-compressed frame. | Part of the interface contract for integrations that use pre-compressed data. |
| `bool CaptureCompressed(int& Width, int& Height, TArray<uint8>& Data, float ForceCompressionRatio)` | Capture and compress a frame on demand. | `UConvaiWebcamBase` returns `false` by default; override it only if your integration calls the compressed path. |
| `bool CaptureRaw(int& Width, int& Height, TArray<uint8>& Data)` | Capture a raw RGBA frame. | This is the method used by `UConvaiChatbotComponent::SendImage()` in the verified source path. Fill `Data` with row-major RGBA bytes and return `true` on success. |
| `UTexture* GetImageTexture(ETextureSourceType& TextureSourceType)` | Return the current frame texture. | Set `TextureSourceType` to `RenderTarget2D` or `Texture2D` to match your texture type. |
| `FString GetLastErrorMessage() const` | Return the last human-readable error. | Return an empty string if no error has occurred. |
| `int GetLastErrorCode() const` | Return the last numeric error code. | `UConvaiWebcamBase` initializes this value to `-1`. |

## Implement from UConvaiWebcamBase

`UConvaiWebcamBase` is declared in `ConvaiWebcamBase.h` (module `ConvaiVisionBase`). Add `ConvaiVisionBase` to your module's `PublicDependencyModuleNames` in `Build.cs` before including it.

{% stepper %}
{% step %}
### Declare the class

Create a `UActorComponent` subclass that derives from `UConvaiWebcamBase`. Mark it `BlueprintSpawnableComponent` so it appears in the Blueprint component picker.

```cpp
// MyCustomVisionComponent.h
// Pseudocode: replace FMyImageSource with your own image source type.
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
### Override CanStart

`CanStart` is called by the base class `Start()` before it transitions state. Return `true` only when your source is initialized and ready to produce frames. Call `SetErrorCodeAndMessage` to record a diagnostic message if the source is not ready — this powers `GetLastErrorMessage()` and `GetLastErrorCode()` in Blueprint.

```cpp
// MyCustomVisionComponent.cpp
// Pseudocode
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
### Override CaptureRaw

`CaptureRaw` is called by the chatbot each time it needs a frame. Fill `Width`, `Height`, and `Data` with the raw RGBA pixel data from your source (row-major, 4 bytes per pixel). Return `true` on success and `false` if the frame could not be captured.

```cpp
// Pseudocode
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
### Override CaptureCompressed when needed

Override `CaptureCompressed` only if another part of your integration calls the compressed capture path. The current chatbot send path uses `CaptureRaw()`, so most custom chatbot vision sources do not need this method.

```cpp
// Pseudocode
bool UMyCustomVisionComponent::CaptureCompressed(
    int& Width, int& Height, TArray<uint8>& Data, float ForceCompressionRatio)
{
    if (!MyImageSource.IsValid())
        return false;

    // Return pre-compressed JPEG directly from the source.
    return MyImageSource->GetJPEGFrame(Width, Height, Data);
}
```

If you do not override `CaptureCompressed`, `UConvaiWebcamBase::CaptureCompressed()` returns `false`.
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
