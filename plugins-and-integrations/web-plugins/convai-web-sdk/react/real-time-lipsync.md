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
import { useGLTF } from '@react-three/drei';

function CharacterController() {
  const convaiClient = useConvaiClient({<ConvaiConfig>});
  const characterRef = useRef<THREE.SkinnedMesh | null>(null);
  const startTimeRef = useRef<number>(0);
  const { scene } = useGLTF('/character.glb');
  
  useEffect(() => {
    // Find the facial SkinnedMesh in your loaded model
    scene.traverse((child) => {
      if (child instanceof THREE.SkinnedMesh && child.morphTargetInfluences) {
        if (child.name.toLowerCase().includes('head') || 
            child.name.toLowerCase().includes('face') ||
            child.morphTargetInfluences.length > 50) {
          characterRef.current = child;
        }
      }
    });
  }, [scene]);
  
  // Track when bot starts speaking
  useEffect(() => {
    const unsubscribe = convaiClient.on('speakingChange', (isSpeaking: boolean) => {
      if (isSpeaking) {
        startTimeRef.current = performance.now();
      }
    });
    
    return unsubscribe;
  }, [convaiClient]);
  
  useEffect(() => {
    if (!convaiClient.state.isConnected) return;
    
    let animationId: number;
    
    const animate = () => {
      const queue = convaiClient.blendshapeQueue;
      
      if (queue.hasFrames() && queue.isConversationActive()) {
        // Calculate elapsed time since bot started speaking
        const elapsedTime = (performance.now() - startTimeRef.current) / 1000;
        
        // Get frame based on elapsed time (synced with audio)
        const result = queue.getFrameAtTime(elapsedTime);
        
        if (result && characterRef.current?.morphTargetInfluences) {
          applyBlendshapesToCharacter(result.frame, characterRef.current.morphTargetInfluences);
        }
      }
      
      animationId = requestAnimationFrame(animate);
    };
    
    animate();
    
    return () => cancelAnimationFrame(animationId);
  }, [convaiClient.state.isConnected]);
  
  return <primitive object={scene} />;
}

// Helper function: Apply blendshapes to character
function applyBlendshapesToCharacter(frame: Float32Array, influences: number[]) {
  const maxIndex = Math.min(frame.length, influences.length);
  for (let i = 0; i < maxIndex; i++) {
    influences[i] = frame[i];
  }
}
```

