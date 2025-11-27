---
description: >-
  This section provides comprehensive information on integrating and handling
  facial expressions and lipsync within your web applications using the
  convai-web-sdk.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/EtUJA212Zc1S9ACc8T4l/plugins-and-integrations/web-plugins/convai-web-sdk/facial-expressions
---

# Facial Expressions

### Initialization

To kickstart facial expression functionality, initialize the `ConvaiClient` with the necessary parameters. The `enableFacialData` flag must be set to `true` to enable facial expression data.

```javascript
convaiClient.current = new ConvaiClient({
  apiKey: '<apiKey>',
  characterId: '<characterId>',
  enableAudio: true,
  enableFacialData: true,
  faceModel: 3, // OVR lipsync
});
```

{% hint style="info" %}
faceModel : 3 is standard and actively maintained.
{% endhint %}

### Receiving Viseme Data

Retrieve viseme data by incorporating the provided callback. The example code demonstrates how to handle and update facial data.

```javascript
const [facialData, setFacialData] = useState([]);
const facialRef = useRef([]);

convaiClient.current.setResponseCallback((response) => {
if (response.hasAudioResponse()) {
    let audioResponse = response?.getAudioResponse();
      if (audioResponse?.getVisemesData()?.array[0]) {
      //Viseme data
        let faceData = audioResponse?.getVisemesData().array[0];
        //faceData[0] implies sil value. Which is -2 if new chunk of audio is recieve.
          if (faceData[0] !== -2) {
            facialRef.current.push(faceData);
            setFacialData(facialRef.current);
          }
      }
}
```

### Modulating Morph Targets

Utilize the `useFrame` hook from `react-three-fiber` to modulate morph targets based on the received facial data.

<pre class="language-javascript"><code class="lang-javascript"><strong>import {OvrToMorph} from 'convai-web-sdk'
</strong><strong>const blendShapeRef = useRef([]);
</strong>const currentBlendFrame = useRef(0);

useFrame((state, _delta) => {
 // Initiate blendshapes
    if(client?.facialData.length > 0){
// OvrToMorph is required for mapping reallusion morphs
    OvrToMorph(client?.facialData[currentBlendFrame.current],blendShapeRef);
    }
  if (currentBlendFrame.current &#x3C;= blendShapeRef?.current?.length) {
    // Logic to adjust morph targets based on facial data
    currentBlendFrame.current += 1;
  }
});
</code></pre>

In addition to facial expressions, the `convai-web-sdk` allows developers to modulate bone adjustments for specific facial features. Receive bone adjustments for "Open\_Jaw," "Tongue," and "V\_Tongue\_Out" and apply them to your character as demonstrated below:

```javascript

// If current viseme value is Open_Jaw
characterRef.current.getObjectByName("CC_Base_JawRoot").setRotationFromEuler(jawRotation);
// The jaw rotation value can be modulated using THREE.lerp().
// example
const jawRotation = new THREE.Euler(0,0,1.57);
// Here 1.57 is the base value for closed Jaw.
jawRotation.z = THREE.MathUtils.lerp(jawRotation.z,1.57 + blendShapeRef.current[currentBlendFrame.current-1][blend]*0.2,0.8);

```

{% hint style="info" %}
These code examples are specific to reallusion characters.
{% endhint %}

### Handling 100fps Animation

Implement [throttling ](https://www.geeksforgeeks.org/lodash-_-throttle-method/)using lodash to ensure smooth animations at 100fps. The provided example demonstrates how to maintain a consistent animation frame rate.

```javascript
const throttledUpdate = _.throttle(updateAnimation, 10);
const [tick, setTick] = useState(true);

const updateAnimation = () => {
  setTick((tick) => {
    if (tick) {
      return tick;
    }
    return true;
  });
  requestAnimationFrame(throttledUpdate);
};

// Start the animation loop when the component mounts
useEffect(() => {
  requestAnimationFrame(throttledUpdate);
  // Clean up the animation loop when the component unmounts
  return () => {
    cancelAnimationFrame(throttledUpdate);
  };
}, []);

// Use the frame hook to update animations
useFrame((state, _delta) => {
  if (tick) {
    // Logic to get viseme data and alter morph targets accordingly
    setTick(false);
  }
});
```

{% hint style="info" %}
Note: Throttle function is not 100% accurate
{% endhint %}

### Handling 100fps Edge Cases

Throttle accuracy may lead to edge cases. Implement the clock setup and handle both above and below 100fps scenarios using the elapsed time.

```javascript
const [startClock, setStartClock] = useState(false);

useFrame((state, _delta) => {
  if (!startClock || !client?.isTalking) {
    state.clock.elapsedTime = 0;
    if (startClock) setStartClock(false);
  }
  if (client?.isTalking) {
    setStartClock(true);
  }
});

// Handle both above and below 100fps scenarios
if (startClock) {
  if (Math.abs(Math.floor(state.clock.elapsedTime * 100) - currentBlendFrame.current) > 15) {
    if (Math.floor(state.clock.elapsedTime * 100) - currentBlendFrame.current > 0) {
      // Below 100fps
           for(let i=0;i<15;i++){
              blendShapeRef.current.push(0)
            }
            currentBlendFrame.current += 15;
    } else {
      // Above 100fps
       if(blendShapeRef.current.length > 15){
            blendShapeRef.current.splice(-15);
            currentBlendFrame.current -= 15;
       }
    }
  }
}


```

