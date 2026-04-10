---
description: This gives the player the ability for conversation with the chat bot.
---

# Change the parent class for Player.

{% hint style="info" %}
This can be applied to first person player (FPP) or third person player (TPP).
{% endhint %}



Steps to change parent class of a First person player (FPP): -

1. Create a new project as a first person project or import into your already existing project.\
   **Steps to import : -** `Content Browser > Add > Add feature or content pack to the project > First Person > Add to Project.`

<figure><img src="https://lh4.googleusercontent.com/FSOGqzlc8NxLzWbLqNYHwft0Ow9v_e1W9pChuu1OzVbKNlRXx13ZQqEfmG_v14dhxwFeVQbrdcswCwYcm7MXQPLjVKccOdYS6lwxQdK1kBPYN5evG1AREYqMTLJI_24wpzdKw3Ib4tqzYow_G61xa0A" alt="" width="375"><figcaption></figcaption></figure>

<figure><img src="https://lh4.googleusercontent.com/HdzDrA79R0xedYTQmJFOkjCq9IXczPyWPxiwezKJMesOaff6TYvFXPVsrVWl00174KaLdF0q9666Ekx8haPQtmcWzu2brcLrUAAZzcXsrVILb4d4VBpi_tIIq1wYS4YeqDWTfCHt_pU7akoaf4mww1U" alt="" width="375"><figcaption><p>Importing Content Package.</p></figcaption></figure>

Steps to make your game a default First Person game: -&#x20;

**Steps: -** `Edit > Project Settings > Maps and modes > Default Mode > Default GameMode > BP_FirstPersonGameMode`.

<figure><img src="https://lh3.googleusercontent.com/gHObx9QUsJR99DcfscisTcd-a5remqR-__7JfxUTYeHHeSSkmSfXnii24ZzmJpUehGx9RS4iRUbtLbZtglUFMnt3tt2D9TW_hcXzABpYdjFIQc6x_IItmG3M1JXjzTTGk6ZuFIsHjhedPvsynf_aASE" alt="" width="375"><figcaption></figcaption></figure>

<figure><img src="https://lh4.googleusercontent.com/63iSr_Bj1trCNUNpHVg0Ir0toMlYPEBZkFfBeqBJ5UTX_RJNzAZhurQu88pPpXrLPy5cojovhwAXmWCwHO6rlAd8dxNy9nqLOOL15Qyu-95FMn0kREPx5Xw9pe62xFzopelYdTm3vTyyrvR3o3sCH5w" alt="" width="375"><figcaption><p>Choose defalut game mode.</p></figcaption></figure>

2. Then go to **`All > Content > FirstPerson > Blueprints > BP_FirstPersonCharacter`**.
3. Click Class Settings then in the Details section Under **`‘Class Options’`** change the parent class to **`‘ConvaiBasePlayer’.`**

<img src="https://lh3.googleusercontent.com/yXsy1Zy7lfMCTEcj8wqpTZI44UbaDDYiasR9dWFnhzZmTvkV2cXy5-B0U9jNRI2U2lg9jBSkai57RIQ_InSSuaImlCuQIh9LNJaCrZ4Y3wTme_fj6gfMzsBf_HfWE9ICt7Tk_V4J5gs4JH6Ibvlq-Sc" alt="" data-size="line">

<figure><img src="https://lh4.googleusercontent.com/IIukEpo8niZHMAox4z4f-dkre2apO9DHZMKTGzCHfbYFSOZBSboGPnvhlKTDJdDvMTzuN7XND-3z52x42GlpiH1omXDrEeAq3crnK79_EFBobHAByuQtOP1QJbg04ZemJq0eojJb4DiRwyZoo4WNCuY" alt="" width="375"><figcaption><p>Set Parent Class</p></figcaption></figure>

4. Hit save and compile and you will be good to go.



{% hint style="info" %}
For Third Person Player follow the same steps just by looking for Third Person
{% endhint %}
