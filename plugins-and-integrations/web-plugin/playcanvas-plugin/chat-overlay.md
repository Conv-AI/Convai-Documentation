# Chat Overlay

Let's add a chat window to enhance user interaction and immersion. Create a New entity called Convai Chat.&#x20;

### Convai Chat script

\
The `ConvaiChat` script is responsible for managing the chat interface and displaying the conversation between the user and an AI-powered virtual character. It handles rendering user messages and AI responses, maintaining a chat history, and ensuring smooth scrolling behavior within the chat container.

```javascript
// Create a new script called 'convaiChat'
var ConvaiChat = pc.createScript('convaiChat');

// Add an attribute to store the CSS asset
ConvaiChat.attributes.add('css', { type: 'asset', assetType: 'css', title: 'CSS Asset' });

// Add an attribute to store the HTML asset
ConvaiChat.attributes.add('html', { type: 'asset', assetType: 'html', title: 'HTML Asset' });

// Initialize code called once per entity
ConvaiChat.prototype.initialize = function() {
    // Create a new div element for the chat box container
    this.htmlEl = document.createElement('div');
    this.htmlEl.classList.add('chatbox__container');
    this.htmlEl.setAttribute("id", "convai-chat");
    document.body.appendChild(this.htmlEl);

    // Set the HTML content of the chat box container
    this.htmlEl.innerHTML = this.html.resource || '';

    // Create a STYLE element for the CSS
    this.cssEl = document.createElement('style');
    document.head.appendChild(this.cssEl);
    this.cssEl.innerHTML = this.css.resource || '';

    // Initialize variables
    this.asset = null;
    this.assetId = 0;
    this.currentNpcText = "";
    this.currentUserText = "";
    this.ChatHistory = [];
    this.createNewUserChatEl = true;
    this.createNewNpcChatEl = true;
    this.userChatEl = null;
    this.npcChatEl = null;
};

// Function to add a conversation to the chat history
ConvaiChat.prototype.addToChatHistory = function(userQuery, npcResponse) {
    // Create an object representing the conversation
    const conversation = {
        userQuery: userQuery.trim(),
        response: npcResponse.trim(),
    };

    // Push the conversation object to the chat history array
    this.ChatHistory.push(conversation);
};

// Function to add a user message to the chat container
ConvaiChat.prototype.addUserMessage = function(message) {
    const chatContainer = document.getElementById("chatbot__activeChat");
    if (this.createNewUserChatEl) {
        const userMessage = document.createElement("div");
        userMessage.classList.add("user_message");
        this.userChatEl = userMessage;
        chatContainer.appendChild(this.userChatEl);
    }
    this.userChatEl.textContent = message;
};

// Function to add an AI response to the chat container
ConvaiChat.prototype.addNpcMessage = function(message) {
    const chatContainer = document.getElementById("chatbot__activeChat");
    if (this.createNewNpcChatEl) {
        const convaiMessage = document.createElement("div");
        convaiMessage.classList.add("convai_message");
        this.npcChatEl = chatContainer.appendChild(convaiMessage);
    }
    this.npcChatEl.textContent = message;
};

// Function to handle the chat updates
ConvaiChat.prototype.handleChat = function() {
    // Set userText when the conversation is active
    if (window.conversationActive && (window.userTextStream !== this.currentUserText) && window.userTextStream !== "") {
        this.currentUserText = window.userTextStream;
        // UI for current user chat (also trim in the UI)
        this.addUserMessage(this.currentUserText);
        this.createNewUserChatEl = false;
    }

    // Set npcText when the conversation is active
    if (window.conversationActive && (window.npcTextStream !== this.currentNpcText) && window.npcTextStream !== "") {
        this.currentNpcText = window.npcTextStream;
        // UI for current NPC chat (also trim in the UI)
        this.addNpcMessage(this.currentNpcText);
        this.createNewNpcChatEl = false;
    }

    // Add the conversation to the chat history when it's finished
    if (!window.conversationActive && this.currentUserText !== "" && this.currentNpcText !== "") {
        this.addToChatHistory(this.currentUserText, this.currentNpcText);
        this.currentUserText = "";
        this.currentNpcText = "";
        this.createNewUserChatEl = true;
        this.createNewNpcChatEl = true;
    }

    // Scroll to the bottom of the chat container
    this.scrollTop();
};

// Function to scroll to the bottom of the chat container
ConvaiChat.prototype.scrollTop = function(dt) {
    if (window.conversationActive) {
        var chatBox = document.getElementById("chatbot__activeChat");
        chatBox.scrollTop = chatBox.scrollHeight - chatBox.clientHeight;
    }
};

// Update code called every frame
ConvaiChat.prototype.update = function(dt) {
    this.handleChat();
};
```

Add the following files as an attachment to convaiChat script after parsing the script.

### HTML

```html
<div class="chatbot__activeChat" id="chatbot__activeChat">    
</div>
<form id="convai-form">
      <input
        type="text"
        placeholder="Hold [T] to talk"
        class="convai_input"
        id="convai-input"
        name="convai-input"
      />
      <button type="submit" class="convai_chat_submit send-button">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          height="35px"
          viewBox="0 0 24 24"
          width="35px"
          fill="#e5e5e5"
        >
          <path d="M0 0h24v24H0z" fill="none" />
          <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
        </svg>
      </button>
</form>
```

### CSS

```css
*{
  box-sizing: border-box;
}

.chatbox__container{
    position: fixed;
    bottom: 1vw;
    left: 1vw;
    background-color: rgba(0, 0, 0, 0.7);
    border-radius: 16px;
    width: 30vw;
    z-index: 10;
}
.chatbot__activeChat{
  width: 100%;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  min-height: 20vh;
  max-height: 60vh;
  padding: 2%;
}
/* width */
::-webkit-scrollbar {
  width: 0px;
}
/* Track */
::-webkit-scrollbar-track {
  background: transparent;
}

/* Handle */
::-webkit-scrollbar-thumb {
  background: transparent;
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: transparent;
}

.user_message, .convai_message {
    margin-bottom: 8px;
    padding: 8px;
    color: white;
    background: rgba(255, 255, 255, 0.07);
    backdrop-filter: blur( 2px );
    -webkit-backdrop-filter: blur( 2px );
    border-radius: 16px;
}
.user_message{
  color: #e5e5e5;
  align-self: flex-start;
  max-width: 80%;
}
.convai_message {
  background-color: rgba(14, 114, 75, 0.4);
  color: #e5e5e5;
  align-self: flex-end;
  max-width: 80%;
}
@media only screen and (min-device-width: 0px) {
  #convai-form {
    box-sizing: border-box;
    display: flex;
    position: relative;
    padding: 2%;
    height: auto;
    bottom: 0;
    width: 100%;
    max-width: 100vw;
    column-gap: 2%;
    justify-content: space-between;
    align-items: center;
    background-color: transparent;
  }
  #convai-input {
    width: 90%;
    background: rgba(255, 255, 255, 0.07);
    border-radius: 30px;
    padding: 2%;
    color: #e5e5e5;
    outline: none;
    box-sizing: border-box;
    transition: 0.3s;
    border: none;
  }
  #convai-input::placeholder{
    color: #e5e5e5;
  }

  .active_input {
    width: 70%;
    border: 1px solid #ca7f1c;
    box-shadow: 0 0 10px rgba(255, 225, 137, 0.6);
    transition: 0.4s;
  }
}

/* Form buttons  */

.convai_chat_submit {
  box-sizing: border-box;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 100%;
  height: 100%;
  aspect-ratio: 1/1;
  color: #e5e5e5;
  border: 2px solid #e5e5e5;
  background-color: transparent;
  font-weight: 500;
}
.send-button {
  width: 30px;
  height: 30px;
  box-sizing: border-box;
  display: flex;
  border: 2px solid #e5e5e5;
  transition: 0.4s;
  cursor: pointer;
}

.convai-logo{
  position: fixed;
  bottom: 1vw;
  right: 1vw;
  height: 5%;
  object-fit: contain;
  width: auto;
}
```



<figure><img src="../../../.gitbook/assets/Screenshot (37).png" alt=""><figcaption><p>Chat Integration </p></figcaption></figure>
