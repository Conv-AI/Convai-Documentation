# Stage 3: Custom Actions with Single Parameter

Actions can have parameters, for example: `Picks Up` is an action that expects an object that will be picked up, in this guide we will see how to parse these parameters as well as other types of parameters such as text.

### Referencing Objects or Characters

Referencing objects or characters in your AI character is very important for two goals: First, it will have knowledge that the object/character exists, and second, you will be able to get a reference to these objects or characters when actions that relate to them are triggered, such as `Move to - Pick up - Follow` will always be triggered with objects or characters

Referencing objects requires that you add the object to the [Environment](../../blueprints-reference/convai-environment.md) object that is inside the [ConvaiChatbot](../../blueprints-reference/convai-chatbot.md) component. There are two ways to do so:

1.  The first method is to select the character in the scene and then under the details panel, add the references to the Objects array under `Convai Info`, this method requires that you inherit from the `ConvaiBaseCharacter` blueprint.\


    <div align="center">

    <figure><img src="../../../../.gitbook/assets/image (4) (2).png" alt="" width="405"><figcaption></figcaption></figure>

    </div>
2.  At the `begin play` event on the character blueprint, loop over all the objects that you want the character to know about then add to the environment object, in the following blueprint, we tagged the objects we want to add to the environment to make it easier to fetch those at begin play, then we used the second and third tags for names and descriptions respectively.

    <figure><img src="../../../../.gitbook/assets/image (5) (2).png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
* Adding, editing or removing objects at runtime is possible.
* Use `Add Object` function for objects and `Add Character` for Characters.
* Adding the player and other characters in the environment is handled if you're using `CovnaiBaseCharacter as the parent class.`
{% endhint %}

### Parsing Object and Character Types

Once you have managed to add your objects and characters to the environment, let's go over a quick scenario to see how we handle the response:

*   Create an action named `Looks At`  that forces the AI character to look towards a certain object or character.\


    <figure><img src="../../../../.gitbook/assets/image (373).png" alt=""><figcaption></figcaption></figure>
*   Create an event with the same name in the character blueprint, and add an input parameter of type [Convai Result Action](../../blueprints-reference/convai-result-action.md), this will contain the parameters required for the action which is in our case the object/character to look at.\


    <figure><img src="../../../../.gitbook/assets/image (1) (6).png" alt=""><figcaption></figcaption></figure>
*   Now let's finish the implementation as follows, we will break the `Action Parameter` structure and then set the `The Related Object Or Character` as the `Main Character`, note that this is a quick trick to get the AI character to look at the referenced object or character.\


    <figure><img src="../../../../.gitbook/assets/image (2) (6).png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
*   Break the `Related Object Or Character` structure to get more details about the object or character such as its reference, name and description.\


    <figure><img src="../../../../.gitbook/assets/image (3) (5).png" alt=""><figcaption></figcaption></figure>
* If you have not added the reference for the object you will get an invalid reference but you will still get the name and description.
{% endhint %}



### Parsing Other Parameter Types

To be continued..
