# Microphone Permission Issues

If you see the microphone indicator turning on in the top left corner, but no user transcript in the chat UI and the character's response doesn't seem coherant to what you said, then it is likely that the game or Unity is nto accessing the correct microphone or does not have sufficient microphone privilege. To fix this, please follow along.

<figure><img src="../../../.gitbook/assets/image (34).png" alt=""><figcaption><p>Microphone indicator is on but there is no user transcript in the chat UI.</p></figcaption></figure>

<figure><img src="../../../.gitbook/assets/image (35).png" alt=""><figcaption><p>Character did not respond accurately to your specific query.</p></figcaption></figure>

## For Windows

First, we want to ensure that the correct microphone is set as the default microphone.&#x20;

<figure><img src="../../../.gitbook/assets/image (36).png" alt=""><figcaption></figcaption></figure>

Second, we head into microphone properties (the > icon on the right of the selected Microphone) and ensure the we have access to the microphone.

<figure><img src="../../../.gitbook/assets/image (38).png" alt=""><figcaption><p>Click allow so that apps can access the microphone.</p></figcaption></figure>

<figure><img src="../../../.gitbook/assets/image (39).png" alt=""><figcaption><p>Set the mic as the default sound device.</p></figcaption></figure>
