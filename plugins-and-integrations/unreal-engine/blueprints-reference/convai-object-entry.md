---
description: >-
  The ConvaiObjectEntry structure parses information about a character or an
  object in the scene, which is then included in the Environment object.
---

# Convai Object Entry

**Convai Object Entry** structure allows for parsing of information about an object or character in the scene. It takes in the name of the object or character and can also include a reference to the object or character, a description, and a position vector (optional). This information is then added to the Environment object.

## Properties

<table><thead><tr><th width="347.3333333333333">Property</th><th width="98">Type</th><th>Description</th></tr></thead><tbody><tr><td>Ref</td><td>FString</td><td>A reference to a character or object. (Optional)</td></tr><tr><td>Optional Position Vector</td><td>FVector</td><td>A related position vector. (Optional)</td></tr><tr><td>Name</td><td>FString</td><td>The Name of the character or object.</td></tr><tr><td>Description</td><td>FString</td><td>The bio/description for the character/object. (Optional)</td></tr></tbody></table>
