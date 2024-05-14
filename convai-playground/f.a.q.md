# F.A.Q

We'll be updating this page with the most frequently asked questions from our users! \
\
Our [Discord](https://discord.com/invite/TG98s8FWKN) and [YouTube Channels](https://www.youtube.com/@convai) are also great resources if you have further questions or want to learn more!

1. **What is "Character Concurrency"?**
   * _Character Concurrency is the **number of users who can interact** with the NPC at the **same time.**_&#x20;
     * _For example, there are 5 people using separate instances of your application. In order for everyone to be able to interact with the NPC at the same time, the character concurrency limit for your account needs to be at least 5 or more._
   * **Character Concurrency Example**\
     _If there are two NPCs in the game, will the system allow three users to interact with NPC A and another three users to interact with NPC B at the same time?_&#x20;
     * _Only if you have a character concurrency limit of at least 6._
   * _Does the "Character Concurrency" limit apply individually to each NPC?_
     * _No, the limit applies to the API key being deployed. You can think of them as a limit on **actively**_ _**connected sessions**. With a character concurrency limit of 1, you can have 10 AI NPC's or more, but you will only be able to have one user speaking to any of the NPCs at the same time._
2. **How do I get my character to stick to their knowledge bank and backstory?**
   * _Utilize the Moderation & Guardrails toggle and minimize external information. We continue to work on improving character cohesion and prevent hallucinations in conversation responses._
3. **What LLM's are powering Convai?**
   * _Convai utilizes a variety of models across the text-to-speech, input, and speech-to-text output, including fine-tuned open source, as well as commercial foundational models like ChatGPT. The best model for the current context (audio, text, video, etc) is used._
4. **Is there an API to change my character's information?**
   * _Yes! You can see the list of API calls and their functions for characters_ [_here._](https://docs.convai.com/api-docs/reference/core-api-reference/character-tool-api/character-api)
5. **Do the SDK's support Custom Characters?**
   * _Yes, you can use custom characters! here is the_ [_Unreal custom character tutorial_](https://youtu.be/JJf1avEy0aM)_, and the Unity video will be shared soon._
