---
description: >-
  This page demonstrates how to use the knowledge bank to add more information
  to your character than you can using the backstory alone.
---

# Knowledge Bank

### Introduction

We know that language models are helpful for a variety of different tasks. But their capabilities are severely limited by the input length of these models. What this means for our character chatbot is that we now have access to a knowledge bank where you can store large amounts of text-based knowledge for your character.

### Overview

Let us look at the knowledge bank interface and then drill down into each element.

<figure><img src="../../.gitbook/assets/Screenshot 2023-02-20 at 6.21.26 PM.png" alt=""><figcaption><p>Knowledge Bank Dashboard</p></figcaption></figure>

We have two main ways to add a knowledge bank:

1. Use the Text Box
2. Upload files (Limited Right now to 1MB)

Let us go through these and see how to use each of these ways.

{% hint style="info" %}
Two things must be mentioned here:

1. Currently, we support a total file size of 1 MB. That means the total size of all the files an account uploads is limited to 1 MB.
2. Please separate your file names with an underscore when uploading them or creating a file using the text box.
{% endhint %}

### Text Box

### Using File Upload

Right now, we support only uploading text files as a knowledge bank. You can add information for your character as text files. You can upload files simply by clicking on the “Upload” button. You can click on the highlighted button to upload files from your computer.

<figure><img src="../../.gitbook/assets/KB-Upload-1_2.jpg" alt=""><figcaption><p>Upload Files</p></figcaption></figure>

Once you have uploaded the file, it will require some time before it is available for use (we currently have an upper limit of around 10 minutes for this). Once done, your file will appear under the “Available files on your account”, and the “Connect” button will become green like in the image above. You can then choose to associate the file with the current character.

Once connected, you can ask questions which would be only present in the knowledge bank and get the relevant information from your character.

### Using the Knowledge Bank

Using the knowledge bank is pretty simple; once you have uploaded the knowledge bank for your character, you can use the chat UI or the `/getResponse` API to ask about anything stored in the knowledge bank. You should receive accurate results.\
Let us look at an example. We have a file called "mb4.txt", which is a made-up story about a Moon Base and its commander, Samantha. We can be sure that it was not part of the training data for our models because this story was made up just for this tutorial. Let us see how the character chatbot responds when asked about our dashing commander Samantha without the correct document connected to this character.&#x20;

<figure><img src="../../.gitbook/assets/Screenshot 2023-02-20 at 8.01.06 PM.png" alt=""><figcaption><p>Without Connecting Relevant the File</p></figcaption></figure>

That definitely does not look correct, it is just a generic response without any particulars. Moreover, there is no mention of the moon base at all. Let us use the UI to connect the relevant file.

<figure><img src="../../.gitbook/assets/Connect-mb4.jpg" alt=""><figcaption><p>Click to Connect</p></figcaption></figure>

Once we have connected the file, you will get a pop-up when the connection is complete. Let us ask our character once again about Samantha and see if we get the correct answer.&#x20;

{% hint style="info" %}
As soon as you connect the character, you should make sure to refresh the page if a chat is already underway. Otherwise, the model might get conflicting information from the chat history and knowledge bank, producing inconsistencies.
{% endhint %}

<figure><img src="../../.gitbook/assets/Screenshot 2023-02-20 at 8.33.49 PM.png" alt=""><figcaption><p>Conversation after connecting the Knowledge Bank</p></figcaption></figure>

The correct information is present in the reply this time. It means our operation was successful.&#x20;

We hope this page gives you enough information about how to use the knowledge bank to start utilising it for your own purposes. Feel free to contact us at support@convai.com if you have any questions.&#x20;
