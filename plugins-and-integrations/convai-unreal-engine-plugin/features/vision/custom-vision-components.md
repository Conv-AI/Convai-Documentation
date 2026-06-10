---
title: Custom vision components
description: Implement a C++ frame source component for custom Unreal image pipelines that need to provide scene frames to a Convai chatbot.
last_reviewed: "4.0.0-beta.21"
---

This page is for advanced C++ projects. Most teams should use the built-in **Environment Webcam** component from [Vision quick start](vision-quick-start.md).

When your project needs a different image source, create a custom component that implements `IConvaiVisionInterface` so `UConvaiChatbotComponent` can discover or register it. When deriving from `UConvaiWebcamBase`, subclass `USceneComponent`.

## Prerequisites

- A C++ Unreal project with the Convai plugin enabled.
- `ConvaiVisionBase` added to your module's `PublicDependencyModuleNames` in `Build.cs`.
- A working chatbot setup from [Add your first Convai character](../../getting-started/add-your-first-convai-character.md).

## When to implement a custom component

**Environment Webcam** renders from a `USceneCaptureComponent2D` into a `UTextureRenderTarget2D`. Use it for standard in-engine scene capture.

A custom component is appropriate when:

- Your source is an external SDK that produces raw pixel data outside Unreal's texture pipeline.
- Your pipeline already produces image bytes and you need full control over RGBA conversion.
- You need to inject a procedural or generated image feed into the conversation.
- You are wrapping a non-component backend and need a component facade for the chatbot.

## Choose your base class

| Option | When to use |
|---|---|
| Derive from `UConvaiWebcamBase` | You want Blueprint-accessible **Start**, **Stop**, **Get State**, **Set Max FPS**, error getters, and **On Frame Ready**. |
| Implement `IConvaiVisionInterface` directly on `UActorComponent` | You need a component that does not inherit `UConvaiWebcamBase`, but still registers through **Set Vision Component** or actor discovery. |

For most custom sources, derive from `UConvaiWebcamBase`. Override the capture methods your source needs and let the base class handle state, FPS storage, and error reporting.

`bAutoStartVision` exists only on `UEnvironmentWebcam`. Custom subclasses must call **Start** from `BeginPlay` or expose their own auto-start property.

## Interface contract

The table below lists the pure-virtual methods on `IConvaiVisionInterface` in `VisionInterface.h`. When deriving from `UConvaiWebcamBase`, override `CanStart`, `CaptureRaw`, and optionally `GetImageTexture` or `CaptureCompressed`.

| Method | Purpose | Notes |
|---|---|---|
| `void Start()` | Begin capturing. | Shipped base class sets state to `Capturing`. |
| `void Stop()` | End capturing. | Shipped base class sets state to `Stopped`. |
| `EVisionState GetState() const` | Return current lifecycle state. | Called by the chatbot each tick to gate upload. |
| `void SetMaxFPS(int MaxFPS)` | Set maximum capture FPS. | `UConvaiWebcamBase` rejects values `<= 0`. Default is `15`. |
| `int GetMaxFPS() const` | Return current max FPS. | Chatbot upload clamps effective send rate to `1`–`60`. |
| `bool IsCompressedDataAvailable() const` | Return `true` if a pre-compressed frame is ready. | Part of the interface contract. Shipped chatbot path uses `CaptureRaw()`. |
| `bool GetCompressedData(...)` | Retrieve a pre-compressed frame. | Optional for custom integrations. |
| `bool CaptureCompressed(...)` | Capture and compress on demand. | Optional. Shipped chatbot path uses `CaptureRaw()`. |
| `bool CaptureRaw(...)` | Capture a raw RGBA frame. | Required for chatbot upload. Fill row-major RGBA bytes and return `true` on success. |
| `UTexture* GetImageTexture(...)` | Return the current frame texture. | Set `TextureSourceType` to match your texture type. |
| `FString GetLastErrorMessage() const` | Return the last human-readable error. | Return an empty string if no error occurred. |
| `int GetLastErrorCode() const` | Return the last numeric error code. | `UConvaiWebcamBase` initializes this value to `-1`. |

## Implement from UConvaiWebcamBase

`UConvaiWebcamBase` is declared in `ConvaiWebcamBase.h` in the `ConvaiVisionBase` module.

{% stepper %}
{% step %}
### Declare the class

Create a `USceneComponent` subclass that derives from `UConvaiWebcamBase`. Mark it `BlueprintSpawnableComponent` if you want it in the component picker.

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
    TSharedPtr<FMyImageSource> MyImageSource;
};
```
{% endstep %}

{% step %}
### Override CanStart

`CanStart` runs before the base class transitions to `Capturing`. Return `true` only when your source is initialized. Call `SetErrorCodeAndMessage` when the source is not ready so **Get Last Error Message** and **Get Last Error Code** return useful values in Blueprint.

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
{% endstep %}

{% step %}
### Override CaptureRaw

`CaptureRaw` is called by the chatbot upload path. Fill `Width`, `Height`, and `Data` with row-major RGBA bytes. Return `true` on success.

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
{% endstepper %}

## Register the component with the chatbot

Add the component to the same `Actor` as `UConvaiChatbotComponent`.

- When only one vision component exists on the `Actor`, discovery during `BeginPlay` is enough.
- When multiple vision components exist, call **Set Vision Component** in `BeginPlay` and pass the component you want to use.
- Call **Start** from `BeginPlay`, or add your own auto-start property on the custom class.

## Next steps

{% content-ref url="vision-blueprint-reference.md" %}
[Vision Blueprint reference](vision-blueprint-reference.md)
{% endcontent-ref %}

{% content-ref url="vision-frame-sources.md" %}
[Vision frame sources](vision-frame-sources.md)
{% endcontent-ref %}

{% content-ref url="how-vision-works.md" %}
[How vision works](how-vision-works.md)
{% endcontent-ref %}
