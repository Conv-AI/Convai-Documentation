---
description: This document explains how to add simple actions to your Convai characters.
---

# Simple actions

Steps to add simple actions to your Convai character:-&#x20;

* Select your Convai Character and navigate to the Details panel. Within this interface, locate the  `Convai Info` section.&#x20;

<figure><img src="../../../../../.gitbook/assets/ConvaiInfo.jpg" alt="" width="296"><figcaption><p>Convai Info section in Outliner. </p></figcaption></figure>

* Select the `Add Element` icon `(+)` and input the desired action you wish to execute. For example, `Print.`

<figure><img src="../../../../../.gitbook/assets/image (23) (1).png" alt="" width="291"><figcaption><p>Custom Action</p></figcaption></figure>

* Open the character blueprint to which you have just now added the action.&#x20;
*   Add a new event with the same name. `Print` in this case and define the logic for the function you just named and run the function `Handle Actions Completion` with `Is Successful` set to true. \


    <figure><img src="../../../../../.gitbook/assets/image (7).png" alt=""><figcaption><p>Print action implementation</p></figcaption></figure>
* Hit compile and ask your Convai Character to perform the action.&#x20;

<figure><img src="../../../../../.gitbook/assets/image (27).png" alt=""><figcaption><p>The Convai Character Prints when asked to perform. </p></figcaption></figure>
