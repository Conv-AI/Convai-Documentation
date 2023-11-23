# ConvaiTextInOut.cs

A simple script that enables the user to send a text input and receive a text output from Convai.&#x20;

#### Awake()

In the awake function, we will initialize the API Key.&#x20;

```csharp
private void Awake()
```

#### Start()

In the start function, we will initialize the gRPC components, so that we can send the data to the servers.

```csharp
void Start()
```

#### Update()

In the update function, we send the data to the server for processing when the return key is pressed.

```csharp
void Update()
```

#### SendTextData()

In this function, we will first initialize the configuration of the type of data that we will send to the servers and initiate the link to the server. In this case, that will be data with no audio. Then we start the coroutine to receive data back from the server. And finally, we send the actual data to the server for processing. After we have sent the data, we close the link to the server, which lets the server know that we have no more data to send.

```csharp
async Task SendTextData()
```

#### ReceiveResultFromServer()

This function listens to the server until the server has closed the request from its side and displays any response that it gets from the server.&#x20;

{% code overflow="wrap" %}
```csharp
async Task ReceiveResultFromServer(AsyncDuplexStreamingCall<GetResponseRequest, GetResponseResponse> call)
```
{% endcode %}
