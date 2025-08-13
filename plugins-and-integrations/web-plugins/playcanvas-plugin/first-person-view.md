---
description: First Person View - PlayCanvas Plugin Guide for Convai integration.
---

# First Person View

### Adding Physics components to plane

1. Scale up the plane and add physics component to it. Add both collision and rigidbody.&#x20;
2. Import Ammo Js (enables physics). Scale up the Collision component according to the plane size.

<figure><img src="../../../.gitbook/assets/Screenshot (21).png" alt=""><figcaption><p>Physics Component on Plane</p></figcaption></figure>

### Player Body

1. **Create a New Entity**
   * In the PlayCanvas Editor, right-click in the Hierarchy panel and select "Create New Entity".
2. **Add Physics Component**
   * With the new entity selected, click the "Add Component" button in the top-right corner of the Editor.
   * Search for "Physics" and add the "Physics" component to the entity.
3. **Add Collision Capsule Component**
   * With the entity still selected, click "Add Component" again.
   * Search for "Collision" and add the "Collision Capsule" component to the entity.
4. **Adjust Entity Y-Position**
   * Adjust the "Y" value of the Translation to position the entity above the plane.
5. **Add Rigidbody Component**
   * With the entity still selected, click "Add Component" again.
   * Search for "Rigidbody" and add the "Rigidbody" component to the entity.
   * Set the "Type" of the rigidbody to "Dynamic".
6. **Adjust Angular Factors**
   * In the Rigidbody component, locate the "Angular Factor" section.
   * Set the "X", "Y", and "Z" values of the Angular Factor to 0.

<figure><img src="../../../.gitbook/assets/Screenshot (22).png" alt=""><figcaption><p>Physics component for player component</p></figcaption></figure>

### Camera controls for first person view

Create a FirstPersonView.js script and add the bellow code. You can find examples for implementing camera controls on [PlayCanvas documentation](https://api.playcanvas.com/) and examples as well. Attach this script to Player capsule.

```javascript
var FirstPersonMovement = pc.createScript('firstPersonMovement');
var fpsCamera = null
var overChat = false
FirstPersonMovement.attributes.add('power', {
    type: 'number',
    default: 2500,
    description: 'Adjusts the speed of player movement'
});

FirstPersonMovement.attributes.add('lookSpeed', {
    type: 'number',
    default: 0.07,
    description: 'Adjusts the sensitivity of looking'
});
// initialize code called once per entity
FirstPersonMovement.prototype.initialize = function() {
    this.force = new pc.Vec3();
    this.eulers = new pc.Vec3();

    var app = this.app;
    app.mouse.on("mousemove", this._onMouseMove, this);
    app.mouse.on("mousedown", function () { 
        if(!overChat){
            app.mouse.enablePointerLock();
        }   
    },this);
    // Check for required components
    if (!this.entity.collision) {
        console.error("First Person Movement script needs to have a 'collision' component");
    }

    if (!this.entity.rigidbody || this.entity.rigidbody.type !== pc.BODYTYPE_DYNAMIC) {
        console.error("First Person Movement script needs to have a DYNAMIC 'rigidbody' component");
    }
};

// update code called every frame
FirstPersonMovement.prototype.update = function(dt) {
// If a camera isn't assigned from the Editor, create one
    if (!this.camera) {
        this._createCamera();
    }

    var force = this.force;
    var app = this.app;

    fpsCamera = this.camera;
    var forward = this.camera.forward;
    var right = this.camera.right;

    // movement 
    var x = 0;
    var z = 0;

    const convaiFormEl = document.getElementById("convai-input");
    // use w-a-s-d
    if(app.keyboard.isPressed(pc.KEY_A) && !(document.activeElement === convaiFormEl)){
         x -= right.x;
         z -= right.z;
    }

      if (app.keyboard.isPressed(pc.KEY_D) && !(document.activeElement === convaiFormEl)) {
        x += right.x;
        z += right.z;
    }

    if (app.keyboard.isPressed(pc.KEY_W) && !(document.activeElement === convaiFormEl)) {
        x += forward.x;
        z += forward.z;
    }

    if (app.keyboard.isPressed(pc.KEY_S) && !(document.activeElement === convaiFormEl)) {
        x -= forward.x;
        z -= forward.z;
    }

    // use direction from keypresses to apply a force to the character
    if (x !== 0 || z !== 0) {
        force.set(x, 0, z).normalize().scale(this.power);
        this.entity.rigidbody.applyForce(force);
    }

    // update camera angle from mouse events
    this.camera.setLocalEulerAngles(this.eulers.y, this.eulers.x, 0);
};

FirstPersonMovement.prototype._onMouseMove = function (e) {
    // If pointer is disabled
    // If the left mouse button is down update the camera from mouse movement
    if (pc.Mouse.isPointerLocked() || e.buttons[0]) {
        this.eulers.x -= this.lookSpeed * e.dx;
        this.eulers.y -= this.lookSpeed * e.dy;
    }

    const convaiChat = document.getElementById("convai-chat")
    convaiChat.addEventListener("mouseover",()=>{
    overChat = true;
    })

    convaiChat.addEventListener("mouseout",()=>{
    overChat = false;
    })
};

FirstPersonMovement.prototype._createCamera = function () {
    // If user hasn't assigned a camera, create a new one
    this.camera = new pc.Entity();
    this.camera.setName("First Person Camera");
    this.camera.addComponent("camera");
    this.entity.addChild(this.camera);
    this.camera.translateLocal(0, 0.5, 0);
};
```

