---
description: >-
  Integrate real-time facial animation in vanilla JavaScript/TypeScript
  applications.
---

# Real-time Lipsync

## Enable Lipsync

Create a client with lipsync configuration:

```typescript
import { ConvaiClient } from '@convai/web-sdk/vanilla';

const client = new ConvaiClient({
  apiKey: 'your-api-key',
  characterId: 'your-character-id',
  enableLipsync: true,          // Enable blendshape streaming
  blendshapeFormat: 'mha',      // 'arkit' or 'mha' (default: 'mha')
});

// Connect to start receiving blendshapes
await client.connect();
```

## Configuration Options

### ConvaiConfig

```typescript
interface ConvaiConfig {
  // ... other options
  
  /**
   * Enable lipsync/facial animation blendshapes (default: false).
   * When enabled, streams real-time blendshape data at 60fps.
   */
  enableLipsync?: boolean;
  
  /**
   * Blendshape format to receive from server (default: 'mha').
   * 'arkit' - 61 elements (52 blendshapes + 9 rotation values)
   * 'mha' - 251 elements (MetaHuman format)
   */
  blendshapeFormat?: 'arkit' | 'mha';
}
```

### Example with All Options

```typescript
const client = new ConvaiClient({
  apiKey: 'your-api-key',
  characterId: 'your-character-id',
  enableVideo: true,
  enableLipsync: true,
  blendshapeFormat: 'arkit',
  startWithVideoOn: false,
});
```

## Create Lipsync Player

Implement a player class to handle the animation loop:

```typescript
class LipsyncPlayer {
  private client: ConvaiClient;
  private isPlaying: boolean = false;
  private animationFrameId: number | null = null;
  private startTime: number = 0;
  
  constructor(
    client: ConvaiClient, 
    private onFrame: (frame: Float32Array) => void
  ) {
    this.client = client;
    
    // Track when bot starts speaking to sync timing
    client.on('speakingChange', (isSpeaking) => {
      if (isSpeaking) {
        this.startTime = performance.now();
      }
    });
  }

  start(): void {
    if (this.isPlaying) return;
    this.isPlaying = true;
    this.animate();
  }

  stop(): void {
    if (!this.isPlaying) return;
    this.isPlaying = false;
    if (this.animationFrameId !== null) {
      cancelAnimationFrame(this.animationFrameId);
      this.animationFrameId = null;
    }
  }

  private animate = (): void => {
    if (!this.isPlaying) return;

    const queue = this.client.blendshapeQueue;
    
    if (queue.hasFrames() && queue.isConversationActive()) {
      // Calculate elapsed time since bot started speaking
      const elapsedTime = (performance.now() - this.startTime) / 1000;
      
      // Get frame based on elapsed time (synced with audio)
      const result = queue.getFrameAtTime(elapsedTime);
      
      if (result) {
        this.onFrame(result.frame);
      }
    }

    this.animationFrameId = requestAnimationFrame(this.animate);
  };
}

// Usage
const lipsyncPlayer = new LipsyncPlayer(client, (blendshapes) => {
  applyBlendshapesToCharacter(blendshapes, character.morphTargetInfluences);
});

lipsyncPlayer.start();

// Helper function: Map blendshapes to your character's morph targets
function applyBlendshapesToCharacter(frame: Float32Array, influences: number[]) {
  // Simple direct mapping (first N blendshapes to first N morph targets)
  const maxIndex = Math.min(frame.length, influences.length);
  for (let i = 0; i < maxIndex; i++) {
    influences[i] = frame[i];
  }
  
  // OR custom mapping if your character's morphs are in different order:
  // influences[10] = frame[17]; // Map jawOpen (ARKit index 17) to your jaw morph (index 10)
  // influences[15] = frame[18]; // Map mouthClose (ARKit index 18) to your mouth morph (index 15)
}
```

BlendQueue functions:

```tsx
// TIME-BASED ACCESS (Most important for real usage!)
queue.getFrameAtTime(elapsedSeconds) // Returns { frame, frameIndex }

// STATE CHECKS
queue.isConversationActive() // Is bot speaking?
queue.isConversationEnded()  // Did stats arrive?
queue.isAllFramesConsumed()  // Playback complete?

// STATISTICS
queue.getTurnStats()         // TurnStats object
queue.getTimeLeftMs()        // Remaining time in ms
queue.getFramesConsumed()    // How many frames played
queue.getDebugInfo()         // Complete state snapshot

// INTERRUPTION
queue.interrupt()     // Called automatically on sendInterruptMessage()
```
