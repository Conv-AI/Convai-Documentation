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
  private lastFrameIndex: number = -1;
  
  constructor(
    client: ConvaiClient, 
    private onFrame: (frame: Float32Array) => void
  ) {
    this.client = client;
  }

  start(): void {
    if (this.isPlaying) return;
    
    this.isPlaying = true;
    this.lastFrameIndex = -1;
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

    // Get the blendshape queue from the client
    const queue = this.client.blendshapeQueue;
    
    // Check if we have frames to play and conversation is active
    // hasFrames() - Returns true if there are blendshape frames in the queue
    // isConversationActive() - Returns true when bot is speaking
    if (queue.hasFrames() && queue.isConversationActive()) {
      // Get the next frame from the queue (index 0 = first frame)
      // This READS the frame but doesn't remove it yet
      const frame = queue.getFrame(0);
      
      // frame is a Float32Array with blendshape values (0.0 to 1.0)
      // Length depends on format: ARKit=52+, MetaHuman=251
      if (frame) {
        this.onFrame(frame);
        
        // Remove the frame from the queue after applying it
        // consumeFrames(1) removes 1 frame from the front of the queue
        // This is important! Without this, the same frame plays forever
        queue.consumeFrames(1);
      }
    } else if (queue.isConversationEnded()) {
      this.lastFrameIndex = -1;
    }

    // Continue the animation loop at ~60fps (or your monitor's refresh rate)
    this.animationFrameId = requestAnimationFrame(this.animate);
  };
}

// Usage
const lipsyncPlayer = new LipsyncPlayer(client, (blendshapes) => {
  // IMPORTANT: Your character likely has MORE morph targets than the blendshape format!
  // Example: Your character might have 300+ morphs (body, face, expressions)
  // But ARKit only provides 52 facial blendshapes
  // 
  // RECOMMENDED: Create a mapping function that specifies which blendshape index
  // should affect which morph target index on your character
  applyBlendshapesToCharacter(blendshapes, character.morphTargetInfluences);
});

lipsyncPlayer.start();

// Helper function: Map blendshape indices to your character's morph target indices
function applyBlendshapesToCharacter(frame: Float32Array, influences: number[]) {
  // Map each blendshape to the correct morph target on your character
  // Example mappings (customize based on your character's morph target order):
  influences[10] = frame[0];  // ARKit jawOpen -> your character's jaw morph at index 10
  influences[15] = frame[1];  // ARKit mouthClose -> your character's mouth morph at index 15
  influences[42] = frame[17]; // ARKit eyeBlinkLeft -> your character's left eye at index 42
  // ... add mappings for all blendshapes you need
  
  // Tip: Check your character's morphTargetDictionary to find the correct indices:
  // console.log(character.morphTargetDictionary);
}
```
