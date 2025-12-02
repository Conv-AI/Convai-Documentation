---
description: >-
  You can create real-time visualizations from the bot’s audio using Web Audio +
  the WebRTC room.
---

# Audio Visualizer (Optional)

> This is an example and can be adapted to your UI.

```tsx
import { useConvaiClient } from "@convai/web-sdk/react";
import { useEffect, useRef, useState } from "react";

export function AudioVisualizer() {
  const convaiClient = useConvaiClient({
    apiKey: "your-api-key",
    characterId: "your-character-id",
  });

  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [audioLevel, setAudioLevel] = useState(0);

  useEffect(() => {
    if (!convaiClient.room || !convaiClient.state.isConnected) return;

    let animationId: number;
    const audioContext = new AudioContext();
    let analyzer: AnalyserNode | null = null;
    let dataArray: Uint8Array | null = null;

    const setup = async () => {
      const remoteParticipants = Array.from(
        convaiClient.room.remoteParticipants.values()
      );
      if (!remoteParticipants.length) return;

      const participant = remoteParticipants[0];
      const publications = Array.from(
        participant.audioTrackPublications.values()
      );
      if (!publications.length || !publications[0].track) return;

      const track = publications[0].track!;
      const mediaStream = new MediaStream([track.mediaStreamTrack]);

      const source = audioContext.createMediaStreamSource(mediaStream);
      analyzer = audioContext.createAnalyser();
      analyzer.fftSize = 256;

      source.connect(analyzer);
      dataArray = new Uint8Array(analyzer.frequencyBinCount);

      const render = () => {
        if (!analyzer || !dataArray) return;

        analyzer.getByteFrequencyData(dataArray);
        const sum = dataArray.reduce((a, b) => a + b, 0);
        const avg = sum / dataArray.length;
        setAudioLevel(avg / 255);

        const canvas = canvasRef.current;
        if (canvas) {
          const ctx = canvas.getContext("2d");
          if (ctx) {
            const { width, height } = canvas;
            ctx.clearRect(0, 0, width, height);

            const barWidth = (width / dataArray.length) * 2.5;
            let x = 0;
            for (let i = 0; i < dataArray.length; i++) {
              const barHeight = (dataArray[i] / 255) * height;
              ctx.fillRect(x, height - barHeight, barWidth, barHeight);
              x += barWidth + 1;
            }
          }
        }

        animationId = requestAnimationFrame(render);
      };

      render();
    };

    setup();

    return () => {
      if (animationId) cancelAnimationFrame(animationId);
      audioContext.close().catch(() => {});
    };
  }, [convaiClient.room, convaiClient.state.isConnected]);

  return (
    <div>
      <canvas
        ref={canvasRef}
        width={800}
        height={200}
        style={{ border: "1px solid #ccc" }}
      />
      <div>Audio Level: {(audioLevel * 100).toFixed(0)}%</div>
    </div>
  );
}
```
