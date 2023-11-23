# Convai UI Prefabs

We provide several UI options to display character and user's transcript out of the box that players can use with the Convai Plugin. You can use and customize these prefabs.&#x20;

The ConvaiNPC and ConvaiGRPCAPI scripts look for GameObjects with Convai Chat UI Handler as a component, and send any transcripts to the script so that it can be displayed on screen.

## Types of UI

### Subtitle

**Prefab Name**: Convai Transcript Canvas - Subtitle

The user and character transcripts are displayed in the bottom like subtitles.

<figure><img src="../../.gitbook/assets/image (12).png" alt=""><figcaption></figcaption></figure>

### Question-Answer

**Prefab Name**: Convai Transcript Canvas - QA

The user's transcript is displayed in the top where as the character's transcript is displayed in the bottom.

<figure><img src="../../.gitbook/assets/image (11).png" alt=""><figcaption></figcaption></figure>

### ChatBox

**Prefab Name**: Convai Transcript Canvas - Chat

Both the user's and the character's transcripts are displayed one after other in a scrollable chat box.

<figure><img src="../../.gitbook/assets/image (10).png" alt=""><figcaption></figcaption></figure>

### Android

**Prefab Name**: Convai Transcript Canvas - Android

Identical to [#subtitle](convai-ui-prefabs.md#subtitle "mention") UI. Includes a button that can be pressed and held for the user to speak. Ideal for portrait orientation of screen.

<figure><img src="../../.gitbook/assets/image (13).png" alt=""><figcaption></figcaption></figure>

## Convai Chat UI Handler Component

<figure><img src="../../.gitbook/assets/image (9).png" alt=""><figcaption></figcaption></figure>

<table><thead><tr><th width="210">Field</th><th>Function</th></tr></thead><tbody><tr><td>Character Name</td><td>The name of the character that is currently speaking.</td></tr><tr><td>Character Text</td><td>The transcript of what the character is speaking.</td></tr><tr><td>Character Text Color</td><td>The color of the text or the speaker name when the transcript is displayed when the character is speaking.</td></tr><tr><td>User Name</td><td>The name of the user that is currently speaking.</td></tr><tr><td>User Text</td><td>The transcript of what the user is speaking.</td></tr><tr><td>User Text Color</td><td>The color of the text or the speaker name when the transcript is displayed when the user is speaking.</td></tr><tr><td>Is Character Talking</td><td>A flag that is true when the character is currently speaking.</td></tr><tr><td>Is User Talking</td><td>A flag that is true when the user is currently speaking.</td></tr><tr><td>User Text Field</td><td>Text mesh pro field for the user's transcript to be displayed.</td></tr><tr><td>Character Text Field</td><td>Text mesh pro field for the character's transcript to be displayed.</td></tr><tr><td>UI Type</td><td>The type of the UI that we are displaying.</td></tr></tbody></table>

### Functions to Know

<table><thead><tr><th width="265"></th><th></th></tr></thead><tbody><tr><td>SendCharacterText</td><td>A public function that sends a string of text to be displayed  as character transcript along with the name of the character who said it. </td></tr><tr><td>SendUserText</td><td>A public function that sends a string of text to be displayed  as user transcript.</td></tr></tbody></table>

