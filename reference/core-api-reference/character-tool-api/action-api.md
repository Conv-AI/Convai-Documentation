---
description: This page describes the Action API and how to use it.
---

# Action API

### Introduction

Conversations can be made even more engaging if they result in driving the behaviour of your character and give it the ability to manipulate the environment. The Action API enables this by allowing you to define various actions that the character can perform. The actions are often tied to the available objects in the environment.&#x20;

To get the most use of the Action API, a few things must be understood to get the most out of it. Here we explain some principles that should guide how to write each of these.

This tutorial will use code examples and comments to show how to use the Action API effectively.

### Setup

The following things need to be set up in order to successfully follow along with this tutorial. Make a colab notebook would suffice without installing any packages to be able to follow along.

```python
# Importing a couple of libraries
import base64
import json
import requests

# This function will be useful for passing the request
def convert(l):
  """This little function will help us convert
  the list of dictionaries to the required format"""
  o = ""
  for each in l:
    o += json.dumps(each) + ";"
  return o

# Use your character id here
CHAR_ID = "<your character id>"

# You should set your Convai API key here
CONVAI_KEY = "<your convai api key>"

# This is the URL which will generate actions and responses
action_url = "https://api.convai.com/character/getResponse"

# URL for updating the backstory
url = "https://api.convai.com/character/update"
```

### Components of the Action API

The building blocks of what is needed to generate actions in an environment are the following.

1. Actions
2. Objects
3. Characters
4. Backstory

Let us now discuss these in some detail. We are listing these out here, but you should return to each section as you are setting them up.

### Objects

Same as actions, there are a few details regarding objects that the user should be aware of. If you have multiple similar objects, it's best to number them. For example, instead of putting “5 Chairs”, you should put “Chair#1”, “Chair#2”, and so on. If you need your character to bring you a specific object, you should also ask specifically for it, i.e. “Bring me chair number 3”. You can also mention the action which can interact with the object to increase effectiveness.

Below we provide two examples of how to define objects and describe how to best define them.

```python
## Basic Definition
# The easiest way to define actions is in the following way, using the convert()
# function, we can directly convert it to the form required by the API, the 
# API reference will explain how to make the API calls.

# objects = [{"name": "Mojito","description": "For once, a VIRGIN Mojito."},
#            {"name": "Tequilla Sunrise","description": "Not my personal favourite."},
#            {"name": "White Russian","description": "The Dude's favourite drink."},
#            {"name": "A Jukebox","description": "A jukebox with lots of songs."},
#            {"name": "Freshly sliced oranges","description": "Some zesty oranges to freshen you up."},
#            {"name": "Fish and Chips","description": "Good old fish n' chips."},
#            {"name": "Some Samosas","description": "A tasty Indian snack."},
#            {"name": "Book","description": "A book to pass your time as you enjoy your meal."},
#            ]

## Advanced (and Better) Definition
# A better way to define objects is to also specify what kind of actions can be 
# performed on them in the name. Remember, DO NOT USE ; in either the "name" or 
# the "description" fields since they are used as separators in the API call and
# might cause unstable behaviour.
#
# While defining objects like this might be more difficult, in our experience 
# it vastly improves performance."Play, Serve, Give, Call Cab"
objects = [{"name": "Mojito (Can be: Served|Cannot be: Played, Given)","description": "For once, a VIRGIN Mojito."},
           {"name": "Tequilla Sunrise (Can be: Served|Cannot be: Played, Given)","description": "Not my personal favourite."},
           {"name": "White Russian (Can be: Served|Cannot be: Played, Given)","description": "The Dude's favourite drink."},
           {"name": "A Jukebox (Can be: Played|Cannot be: Served, Given)","description": "A jukebox with lots of songs."},
           {"name": "Freshly sliced oranges (Can be: Served|Cannot be: Played, Given)","description": "Some zesty oranges to freshen you up."},
           {"name": "Fish and Chips (Can be: Served|Cannot be: Played, Given)","description": "Good old fish n' chips."},
           {"name": "Some Samosas (Can be: Served|Cannot be: Played, Given)","description": "A tasty Indian snack."},
           {"name": "Book (Can be: Given|Cannot be: Played, Served)","description": "A book to pass your time as you enjoy your meal."},
           ]
```

### Backstory

It is important to know that the backstory also influences how the action API performs. The most important thing that can be done for effective action generation is to put some information about the objects, characters and actions in the backstory itself. (You can also use the knowledge bank to put this information in, but we recommend using the backstory to do this instead) We shall provide an example of how to do this here. You can see how we state what kind of objects are in the scene and some information about them. It is also good to specify some information about the environment here if you can.

Any information about the character itself can be placed in the knowledge bank.

```python
backstory = """A bartender character who can help carry out different tasks. 

It can serve a few drinks:
1. Mojito
2. Tequilla Sunrise
3. White Russian

There are a few objects around it as well; these are:
1. A Jukebox
2. A bowl of peanuts
3. Freshly sliced oranges
4. Fish and Chips
5. Some Samosas
6. Book

There are a few actions which this character can perform with the objects listed above. 
The character can agree or disagree to perform the tasks the user requires. 
Similarly, if asked to do something with the other objects, the character can only do them if 
the available actions can work on the available objects. The character can also perform the Call Cab
action if requested."""

# As an aside we also provide the code to update the backstory in case you want
# change things and try for yourself.
payload = json.dumps({
  "charID": CHAR_ID,
  "backstory": backstory,
})
headers = {
  'CONVAI-API-KEY': CONVAI_KEY,
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)

```

### Actions

Actions are the core of this API. To create effective actions, you need to ensure that the actions can be applied generally and are simple. Try not to make the actions too specific. For example, an action called “Show” will be more effective than “Demonstrate”. Similarly, “Walks To” or “Runs To” would be less effective than “Moves To” or “Go To” since the second set is in some sense more “general” than the first.

You should also maintain consistent casing while defining actions. If you go with lowercase, then write all actions in lowercase and so on. To get the best performance, the actions must also make sense in the context of the character’s background.

Actions can be sent via the API call or can be set in the Playground UI. We demonstrate the API call version here. If you want to set them using the UI, go to [https://convai.com/pipeline/dashboard/character](https://convai.com/pipeline/dashboard/character) and click on the Actions button and add your actions and finally, click the `Update` button.

```python
actions = "Play, Serve, Give, Call Cab"
```

### Characters

This is pretty simple, just provide the characters that are present in the scene. You can add more than two characters; for example, if you are in a restaurant with multiple people, you can add all of them here.

You should make sure that you include important information about your characters in the either the knowledge bank or the backstory. And not use the bio for any truly important information.

```python
characters = [{"name": "User", "bio": "It's the guy using the Action API."},
              {"name": "Action-API-Doc-Bot", "bio": "Helping create docs here at Convai."},]
```

### API Reference

We now we can finish up this tutorial with an API reference and all the ways you can call the Action API.

```python
userText = input("Enter your command: ")

payload={'userText': userText,
  'charID': CHAR_ID,
  'sessionID': '-1',
  'voiceResponse': 'false',
  'actions': actions,
  'classification':'multistep', 
  'objects': convert(objects),
  'characters': convert(characters),
  }

files = []

headers = {
  'CONVAI-API-KEY': CONVAI_KEY 
}

response = requests.request("POST", action_url, headers=headers, data=payload, files=files)

response = json.loads(response.text)

print(json.dumps(response, indent=4))

# Respone body
# {
#     "userQuery": "Can you give me a drink?",
#     "charID": "17e9cbde-abcd-11ed-9d60-42010a80000d",
#     "sessionID": "4ba18da3db1627953bf04f3a4021779f",
#     "text": "Sure! What would you like? I have Mojito, Tequilla Sunrise, and White Russian available.",
#     "response": "Sure! What would you like? I have Mojito, Tequilla Sunrise, and White Russian available.",
#     "actionSequence": " \nServe Mojito\n Serve Tequilla Sunrise\n Serve White Russian"
# }
```
