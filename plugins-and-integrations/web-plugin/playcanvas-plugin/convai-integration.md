# Convai Integration

After the addition of Convai web-sdk-cdn to url section, ConvaiClient class will be available to the browser directly.

{% hint style="info" %}
Add all the scripts bellow to your Character entity.
{% endhint %}

### Convai Initialization Script

{% hint style="success" %}
Replace the empty "" with you API key and Character ID.
{% endhint %}

The `ConvaiNpc` script is responsible for handling the interaction between the user and a virtual character powered by the Convai AI.

The script initializes the Convai client by providing an API key and character ID. It sets up necessary callbacks to handle various events, such as errors, user queries, and audio responses from the Convai service.

The `initializeConvaiClient` function is the entry point for setting up the Convai client. It creates a new instance of the `ConvaiClient` and configures it with the provided API key, character ID, and other settings like enabling audio and facial data.

The script handles user input through two methods: text input via a form and voice input using the "T" key. For voice input, the `handleKeyDown` and `handleKeyUp` functions are used to detect when the "T" key is pressed and released, respectively. When the "T" key is pressed, the script starts recording audio and sends it to the Convai service for processing.

The `ConvaiNpc.prototype.initialize` function is called once per entity and sets up the Convai client. It also registers callbacks for handling audio playback events, updating the `isTalking` and `conversationActive` flags accordingly.

The `ConvaiNpc.prototype.handleAnimation` function updates the character's animation based on the `isTalking` state, allowing for synchronized lip movements and facial expressions.

<pre class="language-javascript"><code class="lang-javascript"><strong>var ConvaiNpc = pc.createScript('convaiNpc');
</strong>
/** Loading convai-sdk cdn */
var convaiClient = null;
var userTextStream = ""; // Stores the user's text input
var npcTextStream = ""; // Stores the NPC's text response
var keyPressed = false; // Keeps track of whether the "T" key is pressed
var isTalking = false; // Indicates if the NPC is currently talking
var conversationActive = false; // Indicates if a conversation is currently active
var visemeData = []; // Stores viseme data for lip sync animation
var visemeDataActive = false; // Indicates if viseme data is available
var formLoaded = false; // Indicates if the form has been loaded
let timeoutId;
/**
 * Initializes the ConvaiClient with an API key, a character ID, and flags for enabling the audio recorder and player. Call this first from Start()
 * Sets up several callbacks for handling different types of responses from the Convai Client.
 * @param {string} apiKey - The API key for the Convai service.
 * @param {string} characterId - The ID of the character to use in the Convai service.
 * @param {boolean} enableAudioRecorder - Flag to enable the audio recorder.
 * @param {boolean} enableAudioPlayer - Flag to enable the audio player.
 * @param {number} faceModal - The face modal to use for the character.
 * @param {boolean} enableFacialData - Flag to enable facial data.
*/
function initializeConvaiClient () {
    console.log("Convai client initiated.");
    convaiClient = new ConvaiClient({
        apiKey: "", // Replace with your API key
        characterId: "", // Replace with your character ID
        enableAudio: true,
        faceModal: 3,
        enableFacialData: true,
    });

    // Error callback
    convaiClient.setErrorCallback(function(type, statusMessage) {
        console.log("Error Callback", type, statusMessage);
    });

    // Response callback
    convaiClient.setResponseCallback(function(response) {
        // Handle user query
        if (response.hasUserQuery) {
            var transcript = response.getUserQuery();
            if (transcript) {
                var isFinal = transcript?.getIsFinal();
                var transcriptText = transcript.getTextData();
                if (isFinal) {
                    userTextStream += " " + transcriptText;
                }
                userTextStream = transcriptText;
            }
        }

        // Handle audio response
        if (response.hasAudioResponse()) {
            var audioResponse = response.getAudioResponse();
            npcTextStream += " " + audioResponse.getTextData();

            // Handle viseme data for lip sync animation
            if (audioResponse.hasVisemesData()) {
                let lipsyncData = audioResponse.getVisemesData().array[0];
                if (lipsyncData[0] !== -2) {
                    visemeData.push(lipsyncData);
                    visemeDataActive = true;
                }
            } else {
                visemeDataActive = false;
            }
        }
    });
}

// Handle key down event for starting audio input
function handleKeyDown(e) {
    const convaiFormEl = document.getElementById("convai-input");
    if (convaiClient &#x26;&#x26; e.keyCode === 84 &#x26;&#x26; !keyPressed &#x26;&#x26; !(document.activeElement === convaiFormEl)) {
        e.stopPropagation();
        e.preventDefault();
        keyPressed = true;
        userTextStream = "";
        npcTextStream = "";
        convaiClient.startAudioChunk();
        conversationActive = true;
    }
}

// Handle key up event for stopping audio input
function handleKeyUp(e) {
    const convaiFormEl = document.getElementById("convai-input");
    if (convaiClient &#x26;&#x26; e.keyCode === 84 &#x26;&#x26; keyPressed &#x26;&#x26; !(document.activeElement === convaiFormEl)) {
        e.preventDefault();
        keyPressed = false;
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
        convaiClient.endAudioChunk();
        }, 500);
    }
}

// Add event listeners for key down and key up
window.addEventListener("keydown", handleKeyDown);
window.addEventListener("keyup", handleKeyUp);

// Initialize code called once per entity
ConvaiNpc.prototype.initialize = function() {
    initializeConvaiClient();

    // Set callbacks for audio playback
    convaiClient.onAudioPlay(() => {
        isTalking = true;
    });
    convaiClient.onAudioStop(() => {
        isTalking = false;
        conversationActive = false;
    });
};

// Handle animation based on the talking state
ConvaiNpc.prototype.handleAnimation = function() {
    this.entity.anim.setBoolean("Talking", isTalking);
};

// Update code called every frame
ConvaiNpc.prototype.update = function(dt) {
    this.handleAnimation();

    // Check if the form is loaded and add event listener
    if (!formLoaded &#x26;&#x26; document.getElementById("convai-form")) {
        this.formListener();
        formLoaded = true;
    }
};

// Add event listener for form submission
ConvaiNpc.prototype.formListener = function() {
    document.getElementById("convai-form").addEventListener("submit", (e) => {
        e.preventDefault();
        var inputValue = document.getElementById("convai-input").value;
        window.convaiClient.sendTextChunk(inputValue);
        userTextStream = inputValue;
        document.getElementById("convai-form").reset();
        conversationActive = true;
        npcTextStream = "";
    });
}
</code></pre>

### PlayerAnimationHandler Script

The `PlayerAnimationHandler` script is responsible for controlling the animations of a player character based on certain conditions, such as velocity or other factors.

The script defines three attributes:

1. `blendTime`: This attribute controls the blend time between animations, which determines how smoothly the transition between animations occurs. The default value is set to 0.2.
2. `velMin`: This attribute represents the minimum velocity required to trigger a specific animation. The default value is set to 10.
3. `velMax`: This attribute represents the maximum velocity required to trigger a specific animation. The default value is set to 50.

```javascript
// Create a new script called 'playerAnimationHandler'
var PlayerAnimationHandler = pc.createScript('playerAnimationHandler');

// Add an attribute called 'blendTime' with a default value of 0.2
// This attribute controls the blend time between animations
PlayerAnimationHandler.attributes.add('blendTime', { type: 'number', default: 0.2 });

// Add an attribute called 'velMin' with a default value of 10
// This attribute represents the minimum velocity for a specific animation
PlayerAnimationHandler.attributes.add('velMin', { type: 'number', default: 10 });

// Add an attribute called 'velMax' with a default value of 50
// This attribute represents the maximum velocity for a specific animation
PlayerAnimationHandler.attributes.add('velMax', { type: 'number', default: 50 });

// This function is called when the script is initialized
PlayerAnimationHandler.prototype.initialize = function() {
    // Play the 'Idle' animation with the specified blend time
    this.entity.animation.play('Idle', this.blendTime);
};
```

These attributes can be adjusted in the editor or through code to fine-tune the animation behavior for the player character.

The `initialize` function is called when the script is initialized. In this implementation, it plays the 'Idle' animation with the specified blend time (`this.blendTime`). This animation will be played when the player character is not moving or when the velocity is outside the range defined by `velMin` and `velMax`.

The script is designed to be extended further to handle different animation states based on the player character's velocity or other conditions. For example, you could add additional functions or logic to check the player's velocity and play different animations (e.g., 'Walk', 'Run') based on the velocity range defined by `velMin` and `velMax`.

By utilizing this script, you can easily manage and transition between different animations for the player character, providing a more immersive and realistic experience in your game or application.

### Lipsync Script

The `Lipsync` script is responsible for animating the character's mouth and facial expressions based on the received viseme data. Visemes are the key mouth shapes and facial positions used to represent speech sounds. The script applies morph target animations to the character's head and teeth components to achieve realistic lip-syncing effects.

The script works by accessing the `visemeData` array, which contains the viseme weights for each frame of the animation. It then applies these weights to the corresponding morph targets on the head and teeth components. The `runVisemeData` function handles this process by looping through the viseme weights and setting the morph target weights accordingly.

The script keeps track of the current viseme frame using the `currentVisemeFrame` variable and a timer variable. This ensures that the viseme animations are synchronized with the audio playback. When the viseme data has finished playing, the `zeroMorphs` function is called to reset all morph target weights to zero, effectively resetting the character's facial expression.

```javascript
// Create a new script called 'lipsync'
var Lipsync = pc.createScript('lipsync');

// Array to store the lipsync data
var lipsyncData = [];

// initialize code called once per entity
Lipsync.prototype.initialize = function() {
    // Find the head component of the entity
    this.headComponent = this.entity.findByName("Wolf3D_Head").render;

    // Find the teeth component of the entity
    this.teethComponent = this.entity.findByName("Wolf3D_Teeth").render;

    // Initialize the current viseme frame to 0
    this.currentVisemeFrame = 0;

    // Initialize the timer to 0
    this.timer = 0;
};

// Run morph targets on the viseme data received
Lipsync.prototype.runVisemeData = function(dt) {
    // Sync frames with time
    if (this.currentVisemeFrame <= lipsyncData.length && lipsyncData.length !== 0) {
        if (this.headComponent && this.teethComponent) {
            // Get the morph instance for the head and teeth components
            var headMorphInstance = this.headComponent.meshInstances[0].morphInstance;
            var teethMorphInstance = this.teethComponent.meshInstances[0].morphInstance;

            if (lipsyncData[this.currentVisemeFrame] !== undefined) {
                // Loop through the morph targets and set their weights
                for (let i = 0; i < 15; i++) {
                    if (lipsyncData[this.currentVisemeFrame][i] !== undefined) {
                        headMorphInstance.setWeight(i, lipsyncData[this.currentVisemeFrame][i]);
                        teethMorphInstance.setWeight(i, lipsyncData[this.currentVisemeFrame][i]);
                    }
                }
            }

            // Update the current viseme frame based on the timer
            this.currentVisemeFrame = Math.floor(this.timer * 100);
        }
    }
}

// Reset all morph targets to 0
Lipsync.prototype.zeroMorphs = function(dt) {
    if (this.headComponent && this.teethComponent) {
        // Get the morph instance for the head and teeth components
        var headMorphInstance = this.headComponent.meshInstances[0].morphInstance;
        var teethMorphInstance = this.teethComponent.meshInstances[0].morphInstance;

        // Loop through the morph targets and set their weights to 0
        for (let i = 0; i < 15; i++) {
            headMorphInstance.setWeight(i, 0);
            teethMorphInstance.setWeight(i, 0);
        }
    }
}

// update code called every frame
Lipsync.prototype.update = function(dt) {
    // Check if there is new viseme data and update the lipsyncData array
    if (window.visemeData && window.visemeDataActive) {
        lipsyncData = window.visemeData;
    }

    if (lipsyncData.length > 0) {
        // Update the timer
        this.timer += dt;

        // Run the viseme data
        this.runVisemeData();

        // Check if the viseme data has finished playing
        if (this.timer * 100 >= lipsyncData.length) {
            // Reset all morph targets to 0
            this.zeroMorphs();

            // Clear the lipsyncData array and reset the timer and currentVisemeFrame
            lipsyncData = [];
            this.timer = 0;
            this.currentVisemeFrame = 0;
            window.visemeData = [];
        }
    }
};
```

### HeadTracking Script

The `HeadTracking` script is responsible for controlling the rotation of a character's head and eyes based on the position of the camera (representing the user's viewpoint). The script achieves this by calculating the angle between the forward vector of the head component and the forward vector of the camera. If this angle is within a specified threshold (45 degrees in this case), the head and eyes are rotated to look towards the camera's position.

<pre class="language-javascript"><code class="lang-javascript"><strong>// Create a new script called 'headTracking'
</strong>var HeadTracking = pc.createScript('headTracking');

// Helper function to find a child entity by name recursively
HeadTracking.prototype.findChild = function(children, matchName) {
    for (let child of children) {
        if (child.name.includes(matchName)) {
            return child;
        }

        if (child.children) {
            const foundChild = this.findChild(child.children, matchName);
            if (foundChild) {
                return foundChild;
            }
        }
    }

    return null;
};

// Function to calculate the radian angle between two vectors
HeadTracking.prototype.getRadianAngle = function(vecA, vecB) {
    dot = vecA.normalize().dot(vecB.normalize());
    return Math.acos(dot);
};

// initialize code called once per entity
HeadTracking.prototype.initialize = function() {
    // Find the head, left eye, and right eye components
    this.headComponent = this.entity.findByName("Head");
    this.leftEye = this.entity.findByName("LeftEye");
    this.rightEye = this.entity.findByName("RightEye");
};

// Function called after the update loop
HeadTracking.prototype.postUpdate = function(dt) {
    // Check if the camera position is available
    if (window.fpsCamera?.position !== undefined) {
        const cameraPosition = window.fpsCamera.getPosition().clone();
        const angle = this.getRadianAngle(this.headComponent.forward, window.fpsCamera.forward);
        const degree = angle * pc.math.RAD_TO_DEG;

        // If the angle is within 45 degrees, look at the camera position
        if (degree &#x3C;= 45) {
            this.headComponent.lookAt(-cameraPosition.x, cameraPosition.y, -cameraPosition.z);
            this.leftEye.lookAt(-cameraPosition.x, cameraPosition.y, -cameraPosition.z);
            this.rightEye.lookAt(-cameraPosition.x, cameraPosition.y, -cameraPosition.z);
        }
    }
};
</code></pre>

Add all the above scripts to your playcanvas project and attach convaiNPC, lipsync, Headtracking to the convi (your model) component.

<figure><img src="../../../.gitbook/assets/Screenshot (36).png" alt=""><figcaption><p>Attaching Scripts</p></figcaption></figure>
