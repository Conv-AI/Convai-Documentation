---
title: Add an audio visualizer in React
description: Draw a live level meter and frequency bars from the character's voice in a React app, using the Web Audio API on the audio track of the session.
last_reviewed: "2.0.1"
---

Draw the character's voice as frequency bars and a level meter in a React component. Use this page when you build a custom UI and want visual feedback while the character speaks. The example is a starting point to adapt to your design.

## Prerequisites

- A React app connected with `useConvaiClient`, on the default LiveKit transport. The example reads the character's audio track from `room.remoteParticipants`, which the WebSocket transport does not populate.
- The character's audio playing through `AudioRenderer` or `ConvaiWidget`. The visualizer reads the track; it does not play it. See [Build a custom UI in React](custom-ui-and-advanced-usage.md).

## Add the visualizer component

The component waits for the session to connect, takes the first remote audio track, and feeds it into a Web Audio `AnalyserNode`. Each animation frame it draws the frequency data on a canvas and stores the average level.

The `AudioContext` used here is the browser's Web Audio class. Do not import `AudioContext` from `@convai/web-widget/react` in the same file; that export is the LiveKit room context.

{% code title="src/AudioVisualizer.tsx" %}
```tsx
import { useEffect, useRef, useState } from 'react';
import type { useConvaiClient } from '@convai/web-sdk/react';

type Client = ReturnType<typeof useConvaiClient>;

export function AudioVisualizer({ convaiClient }: { convaiClient: Client }) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [audioLevel, setAudioLevel] = useState(0);

  useEffect(() => {
    if (!convaiClient.room || !convaiClient.state.isConnected) return;

    let animationId = 0;
    const audioContext = new AudioContext();

    const participant = Array.from(convaiClient.room.remoteParticipants.values())[0];
    const publication = participant
      ? Array.from(participant.audioTrackPublications.values())[0]
      : undefined;
    const track = publication?.track;

    if (track) {
      const source = audioContext.createMediaStreamSource(
        new MediaStream([track.mediaStreamTrack]),
      );
      const analyser = audioContext.createAnalyser();
      analyser.fftSize = 256;
      source.connect(analyser);
      const data = new Uint8Array(analyser.frequencyBinCount);

      const render = () => {
        analyser.getByteFrequencyData(data);
        const average = data.reduce((sum, v) => sum + v, 0) / data.length;
        setAudioLevel(average / 255);

        const ctx = canvasRef.current?.getContext('2d');
        if (ctx && canvasRef.current) {
          const { width, height } = canvasRef.current;
          ctx.clearRect(0, 0, width, height);
          const barWidth = (width / data.length) * 2.5;
          let x = 0;
          for (let i = 0; i < data.length; i++) {
            const barHeight = (data[i] / 255) * height;
            ctx.fillRect(x, height - barHeight, barWidth, barHeight);
            x += barWidth + 1;
          }
        }

        animationId = requestAnimationFrame(render);
      };

      render();
    }

    return () => {
      cancelAnimationFrame(animationId);
      audioContext.close().catch(() => {});
    };
  }, [convaiClient.room, convaiClient.state.isConnected]);

  return (
    <div>
      <canvas ref={canvasRef} width={800} height={200} />
      <div>Audio level: {(audioLevel * 100).toFixed(0)}%</div>
    </div>
  );
}
```
{% endcode %}

The effect runs again when `state.isConnected` changes. If the character's track is not yet published when the session connects, the component draws nothing for that session; re-run the setup when a track arrives if your app needs it.

A component that calls `setAudioLevel` every animation frame re-renders at the display rate. For a heavy page, write the level to a ref or straight to the DOM instead.

## Measure your own microphone

`audioControls` has an `audioLevel` field and `startAudioLevelMonitoring()` and `stopAudioLevelMonitoring()` methods. In this release `startAudioLevelMonitoring()` does not update `audioLevel`, which stays `0`. To show your own microphone level, apply the same analyser approach to the local microphone track from `room.localParticipant.audioTrackPublications`.

## Verify the visualizer

Render `<AudioVisualizer convaiClient={convaiClient} />`, connect, and send a message.

{% hint style="success" %}
The bars move and the level rises above 0% while the character speaks, then fall back when it stops.
{% endhint %}

## Next steps

{% content-ref url="custom-ui-and-advanced-usage.md" %}
[Build a custom UI in React](custom-ui-and-advanced-usage.md)
{% endcontent-ref %}

{% content-ref url="useconvaiclient-hook.md" %}
[useConvaiClient hook reference](useconvaiclient-hook.md)
{% endcontent-ref %}

{% content-ref url="../websocket-transport-layer.md" %}
[Use the WebSocket transport](../websocket-transport-layer.md)
{% endcontent-ref %}
