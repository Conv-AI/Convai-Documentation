# windows macos and linux

Desktop builds have no platform-specific configuration requirements. All SDK features work without additional setup — no permission declarations, no manifest changes, no gesture handling. Microphone access, audio playback, spatial audio, Vision, and screen share all function immediately after the standard SDK setup.

***

## What Works on Desktop

| Feature                      | Windows | macOS  | Linux  |
| ---------------------------- | ------- | ------ | ------ |
| Voice conversation           | ✅ Full  | ✅ Full | ✅ Full |
| Lip sync                     | ✅ Full  | ✅ Full | ✅ Full |
| Actions                      | ✅ Full  | ✅ Full | ✅ Full |
| Emotion                      | ✅ Full  | ✅ Full | ✅ Full |
| Long-Term Memory             | ✅ Full  | ✅ Full | ✅ Full |
| Narrative Design             | ✅ Full  | ✅ Full | ✅ Full |
| Vision                       | ✅ Full  | ✅ Full | ✅ Full |
| Spatial audio                | ✅ Full  | ✅ Full | ✅ Full |
| Unity `AudioSource` playback | ✅ Full  | ✅ Full | ✅ Full |
| Microphone device selection  | ✅ Full  | ✅ Full | ✅ Full |
| Screen share                 | ✅ Full  | ✅ Full | ✅ Full |

Screen share is a desktop-exclusive capability — it is not available on WebGL, iOS, Android, or Android-based XR headsets.

***

## Platform and Architecture Support

The SDK ships pre-built native libraries for the following desktop configurations:

| Platform | Supported Architectures                           |
| -------- | ------------------------------------------------- |
| Windows  | x86\_64, arm64                                    |
| macOS    | arm64 (Apple Silicon), x86\_64 (Intel), Universal |
| Linux    | x86\_64                                           |

{% hint style="warning" %}
**Linux arm64 is not supported.** If your deployment target includes Linux arm64 machines, the native transport library will fail to load and voice conversation will not work. Only x86\_64 is available on Linux.
{% endhint %}

***

## Microphone and Audio

No permission declarations are required on desktop platforms. The operating system grants microphone access at the application level:

* **Windows:** Access is managed through Windows Privacy Settings. Unity builds are recognized as desktop applications and receive microphone access without any manifest changes.
* **macOS:** The OS presents a one-time system permission dialog when the application first accesses the microphone. Unity adds `NSMicrophoneUsageDescription` to the app's `Info.plist` automatically for macOS builds. No manual configuration is needed.
* **Linux:** Microphone access is handled by the system audio stack (PulseAudio, PipeWire, ALSA). No application-level permission handling is required.

***

## Vision on Desktop

`CameraVisionFrameSource` works on all desktop platforms without additional configuration — add the component to a `Camera` GameObject, assign a `ConvaiVisionPublisher`, and Vision is active.

{% hint style="info" %}
On macOS, camera capture applies a vertical pixel flip internally to correct for the macOS coordinate system difference. This is handled automatically — no configuration is required.
{% endhint %}

***

## Usage Examples

### Military Simulation Training on Windows

A defense contractor runs mission rehearsal software on Windows workstations. Convai characters play opposing forces, local commanders, and civilian actors in a branching scenario. Trainees speak with characters using standard desktop microphones.

**Setup:** Standard SDK configuration — no platform-specific steps. Spatial audio places character voices in 3D space relative to the player's position. Screen share is not used in this scenario.

**Outcome:** Trainees interact verbally with multiple characters across a mission simulation. The session records responses and branching decisions for after-action review.

***

### Medical Consultation Training on macOS

A medical school deploys a patient consultation trainer on faculty MacBook Pros. Residents practice taking patient histories with a Convai character that responds with realistic symptoms and adapts based on the resident's questions.

**Setup:** Standard SDK configuration. The character uses Vision via `CameraVisionFrameSource` pointed at a physical model the resident is examining. macOS prompts for microphone access on first launch — no additional setup needed.

**Outcome:** Resident speaks with the character naturally. The macOS microphone permission dialog appears on first launch and is not shown again. Vision enables the character to acknowledge what the resident is holding.

***

## Next Steps

{% content-ref url="/broken/pages/665d1a02c31405b646ea5620c1cde76157d769ae" %}
[Broken link](/broken/pages/665d1a02c31405b646ea5620c1cde76157d769ae)
{% endcontent-ref %}

{% content-ref url="/broken/pages/ff400377bdbe8a12298f59c05337311a5c570cc2" %}
[Broken link](/broken/pages/ff400377bdbe8a12298f59c05337311a5c570cc2)
{% endcontent-ref %}

{% content-ref url="/broken/pages/f796a49a82f4b79cf42397dc35d3add7a3f73bdd" %}
[Broken link](/broken/pages/f796a49a82f4b79cf42397dc35d3add7a3f73bdd)
{% endcontent-ref %}
