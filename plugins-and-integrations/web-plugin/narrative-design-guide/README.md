---
description: Narrative Design - Narrative based NPCs with convai on web.
---

# Narrative Design Guide

Narrative design is a method of structuring interactive stories, particularly for convai non-player characters (NPCs) in web-based environments. It utilizes a graph-based system where each node represents a step in the story progression.

## Convai Playground

1. Select your Character in which you want to enable Narrative Design.
2. Open Narrative Design section in convai playground.\
   \
   <img src="../../../.gitbook/assets/image (385).png" alt="" data-size="original">\

3. According to your storyline create a narrative map/graph. Shown bellow is an example. The blue boxes represent triggers (used to initiate a line in the graph) and the black boxes represent sections (what you want the character to speak about). \
   ![](<../../../.gitbook/assets/image (386).png>)\

4.  Each section has an objective and decisions. Based on whats written in Objective the character would speak/respond. You can give the character exact dialogues using `<speak>{your dialogue}</speak>` tags.\
    For decisions add messages as context on how the character can decide on which objective to move to own its own. The once you want to control can be through invokeTrigger in the next section.\


    <figure><img src="../../../.gitbook/assets/Screenshot (114).png" alt=""><figcaption></figcaption></figure>
