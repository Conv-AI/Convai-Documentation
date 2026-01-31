---
description: Integrate real-time facial animation in your React applications.
---

# Real-time Lipsync

Supported Formats

## ARKit (61 Elements)

Apple's ARKit blendshape format with 52 facial blendshapes + 9 rotation values:

* 52 standard facial blendshapes (eye, brow, jaw, mouth, cheek, nose)
* 3 head rotation values (pitch, yaw, roll)
* 6 eye rotation values (left/right eye gaze)

## MetaHuman (251 Elements)

Unreal Engine's MetaHuman format with 251 CTRL\_expressions\_\* blendshapes:

* Comprehensive facial control (brow, eye, cheek, nose, mouth, jaw)
* Highly detailed mouth shapes for precise lip-sync
* Industry-standard for high-fidelity character animation

## Configuration Options

### ConvaiConfig (useConvaiClient)

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

```tsx
const convaiClient = useConvaiClient({
  apiKey: 'your-api-key',
  characterId: 'your-character-id',
  enableVideo: true,
  enableLipsync: true,
  blendshapeFormat: 'arkit',
  startWithVideoOn: false,
});
```

## Access Blendshape Queue

The blendshape queue is available on the client instance:

```tsx
import { useConvaiClient } from '@convai/web-sdk';
import { useEffect, useRef } from 'react';
import * as THREE from 'three';

function CharacterController() {

  const convaiClient = useConvaiClient({<ConvaiConfig>});
  const characterRef = useRef<THREE.SkinnedMesh | null>(null);
  const { scene } = useGLTF('/character.glb');
  
  useEffect(() => {
    // Find the facial SkinnedMesh in your loaded model
    scene.traverse((child) => {
      if (child instanceof THREE.SkinnedMesh && child.morphTargetInfluences) {
        // Look for the mesh with facial morphs (usually head/face)
        if (child.name.toLowerCase().includes('head') || 
            child.name.toLowerCase().includes('face') ||
            child.morphTargetInfluences.length > 50) {
          characterRef.current = child;
        }
      }
    });
  }, [scene]);
  
  useEffect(() => {
    if (!convaiClient.state.isConnected) return;
    
    const animate = () => {
      // Get the blendshape queue from the client
      const queue = convaiClient.blendshapeQueue;
      
      // Check if we have frames to play and conversation is active
      // hasFrames() - Returns true if there are blendshape frames in the queue
      // isConversationActive() - Returns true when bot is speaking
      if (queue.hasFrames() && queue.isConversationActive()) {
        // Get the next frame from the queue (index 0 = first frame)
        // This READS the frame but doesn't remove it yet
        const frame = queue.getFrame(0);
        
        // frame is a Float32Array with blendshape values (0.0 to 1.0)
        // Length depends on format: ARKit=52+, MetaHuman=251
        if (frame && characterRef.current?.morphTargetInfluences) {
          // IMPORTANT: Your character likely has MORE morph targets than the blendshape format!
          // Example: Your character might have 300+ morphs (body, face, expressions)
          // But ARKit only provides 52 facial blendshapes
          // 
          // RECOMMENDED: Create a mapping function that specifies which blendshape index
          // should affect which morph target index on your character:
          //
          // const applyBlendshapes = (frame: Float32Array, influences: number[]) => {
          //   influences[10] = frame[0];  // ARKit jawOpen -> your character's jaw morph
          //   influences[15] = frame[1];  // ARKit mouthClose -> your character's mouth morph
          //   influences[42] = frame[17]; // ARKit eyeBlinkLeft -> your character's left eye
          //   // ... map all blendshapes you need
          // };
          //
          // For better approach with name-based mapping, see Pattern 4 below
          //
          // This simple example assumes first N morphs match ARKit/MetaHuman order:
          const maxIndex = Math.min(frame.length, characterRef.current.morphTargetInfluences.length);
          applyBlendshapesToCharacter(frame, characterRef.current.morphTargetInfluences);
        }
        
        // Remove the frame from the queue after applying it
        // consumeFrames(1) removes 1 frame from the front of the queue
        // This is important! Without this, the same frame plays forever
        queue.consumeFrames(1);
      }
      
      // Continue the animation loop at ~60fps (or your monitor's refresh rate)
      requestAnimationFrame(animate);
    };
    
    animate();
  }, [convaiClient.state.isConnected]);
  
  return <primitive object={scene} />;
}
```

