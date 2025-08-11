---
description: Character Conversation API - Code Example for Roblox integration with Convai.
---

# Character Conversation API

The following piece of code is the most essential section to make a successful call to the Convai server to get a response in a conversation with a character.

{% hint style="info" %}
Refer to [Character API Doc](../../../../api-reference/core-api-reference/character-api.md) for more details on the endpoint.
{% endhint %}

{% hint style="info" %}
This portion of the code is present in the **GlobalFunctions** script in the **Convai Roblox Integration Demo** that you just tried out in the previous section.

The call is handled by the **Chat\_Character** file present within the character model in the game Workspace.
{% endhint %}

```lua
function my_functions.callConvai(msg, sessionID, apiKey, charID)
	local httpSrv = game:GetService("HttpService")
	local baseUrl = "https://api.convai.com/character/getResponse"
	local gpt_response
	
	local function request()
		-- We restrict from making unnecessary calls if the following values are not set properly
		if apiKey == "" then
			print("Please provide a valid API Key")
			return
		end
		if charID == "" then
			print("Please enter a valid Character ID")
			return
		end
		
		-- REST API Cal
		local response = httpSrv:RequestAsync({
			Url = baseUrl,
			Method = "POST",
			Headers = {
				-- This is the most convenient way to send form-data in Roblox
				["Content-Type"] = "application/x-www-form-urlencoded",
				["CONVAI-API-KEY"] = apiKey
			},
			
			Body = string.format([[&userText=%s&sessionID=%s&charID=%s&voiceResponse=%s]], msg, sessionID, charID, 'False')
		})
		
		-- Inspect the response table
		if response.Success then
			print("Status code:", response.StatusCode, response.StatusMessage)
			print("Response body:\n", response.Body)
			local data = httpSrv:JSONDecode(response.Body)
			print("Response Text: ", data.text)
			print("Response Session ID: ", data.sessionID)
			gpt_response = response.Body --data.text
		else
			print("The request failed:", response.StatusCode, response.StatusMessage)
		end
	end

	-- Wrap the function in a 'pcall' to prevent the script from breaking if the request fails
	local success, message = pcall(request)
	--print("Status code: ", message)
	if gpt_response == nil then
		gpt_response = httpSrv:JSONEncode({sessionID = sessionID, text = "Sorry, I can't chat right now."})
	end
	return gpt_response
end

```

The above function is called in the chatbox implementation in the demo game. Here is an overview of what each part is doing:

```lua
function my_functions.callConvai(msg, sessionID, apiKey, charID)
```

The function accepts the **message** we get from the user. We send that along with the **sessionID, and characterID.** We also pass the **API Key** that we have set previously.

```lua
local httpSrv = game:GetService("HttpService")
```

HttpService allows HTTP requests to be sent from game servers. [Details](https://create.roblox.com/docs/reference/engine/classes/HttpService).

Now for the most important portion of the code:

```lua
-- REST API Cal
local response = httpSrv:RequestAsync({
	Url = baseUrl,
	Method = "POST",
	Headers = {
		-- This is the most convenient way to send form-data in Roblox
		["Content-Type"] = "application/x-www-form-urlencoded",
		["CONVAI-API-KEY"] = apiKey
	},
	
	Body = string.format([[&userText=%s&sessionID=%s&charID=%s&voiceResponse=%s]], msg, sessionID, charID, 'False')
}
```

{% hint style="info" %}
Notice how **Content-Type** is set to **"application/x-www-form-urlencoded"**. This is the only acceptable way to send form-data in Roblox. Since the endpoint only accepts form data, we had to parse the data in a suitable format to send it to the server.
{% endhint %}

While the **Body** of the request might look like a complicated string, it is actually quite simple. To break it down into its simple components, it can be viewed as:

```json
{
    'userText': '<msg>',
    'sessionID': '<session-id>',
    'charID': '<character-id>',
    'voiceResponse': 'False'
}
```

{% hint style="info" %}
The value for **voiceResponse** is set to **False.** Since we have no utility of the audio data that the server will generate, we just completely skip that audio generation. The reason is mentioned in the **Constraints** before.
{% endhint %}

The rest of the part is a simple response handling code. Since the response, we receive is JSON data, we have to decode that on the client side to read its content:

```lua
local data = httpSrv:JSONDecode(response.Body)
print("Response Text: ", data.text)
print("Response Session ID: ", data.sessionID)
```

That concludes our discussion on the **/getResponse** API.
