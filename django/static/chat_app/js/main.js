// Global variables
let chatSocket = null;

// Check changes on the chat page
function chatProcess() {
	const roomIDElement = document.getElementById('room-id');
	const roomID = JSON.parse(roomIDElement.textContent);
		
	if (chatSocket !== null) {
		chatSocket.shouldClose = true;
		chatSocket.socket.close();
	}

	// Create a new socket
	let websocketProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
	let websocketPort = window.location.protocol === 'https:' ? ':8001' : ':8000';
	const socketUrl = websocketProtocol + '//' + window.location.hostname + websocketPort + '/ws/chat/' + roomID + "/";

	chatSocket = {
		socket: new WebSocket(socketUrl),
		url: socketUrl,
		shouldClose: false
	};
	
	// Got to the bottom of the chat
	const chatLog = document.querySelector('#chat-log');
	if (chatLog) {
		chatLog.scrollTop = chatLog.scrollHeight;
	}


	// Handle incoming messages
	chatSocket.socket.onmessage = function(e) {
		const data = JSON.parse(e.data);
		
		const blockedUsersElement = document.getElementById('blocked-users');
		const blockedUsers = blockedUsersElement ? JSON.parse(blockedUsersElement.textContent) : [];
		
		const isPrivateElement = document.getElementById('is-private');
		const isPrivate = isPrivateElement ? JSON.parse(isPrivateElement.textContent) : false;

		if (data.sender && !blockedUsers.includes(parseInt(data.sender, 10))) {
			let username = '[UserNotfound]';

			// Get the username of the sender
			fetch('/api/get_username/' + data.sender)
			.then(response => response.json())
			.then(data_username => {
				if (!data_username)
					username = '[UserNotfound]';
				else
					username = data_username.username;
				
				// Create the message container
				const messageContainer = document.createElement('p');
				messageContainer.setAttribute('data-sender', data.sender);
				messageContainer.textContent = data.message;
				
				// Create the username container
				const usernameContainer = document.createElement('p');
				usernameContainer.textContent = username;
				usernameContainer.className = 'other-username';

				// Check if the message is from the current user
				const idElement = document.getElementById('id');
				messageContainer.className = idElement && data.sender === idElement.textContent ? 'my-message' : 'other-message';
				

				// Display the message
				const chatLog = document.querySelector('#chat-log');
				if (chatLog) {
					// Display the username of the sender
					if (data.sender !== idElement.textContent && !isPrivate) {
						if (chatLog.lastElementChild && chatLog.lastElementChild.dataset.sender !== data.sender) {
							chatLog.appendChild(usernameContainer);
						}
					}

					// Display the message
					chatLog.appendChild(messageContainer);

					// Got to the bottom of the chat
					chatLog.scrollTop = chatLog.scrollHeight;
				}
			});
		}
	};


	// Close the socket when the user leaves the page
	window.onbeforeunload = function() {
		if (chatSocket !== null) {
			chatSocket.shouldClose = true;
			chatSocket.socket.close();
		}
	};


	// Handle closing the socket
	chatSocket.socket.onclose = function(e) {
		if (!this.shouldClose) {
			chatSocket.socket = new WebSocket(chatSocket.url);
		}
	};


	// Get the enter key to submit the message
	document.querySelector('#chat-message-input').focus();
	document.querySelector('#chat-message-input').onkeyup = function(e) {
		if (e.key === 'Enter') {
			document.querySelector('#chat-message-submit').click();
		}
	};


	// Send a message
	document.querySelector('#chat-message-submit').onclick = function(e) {
		const messageInputDom = document.querySelector('#chat-message-input');
		const message = messageInputDom.value.trim();
		
		if (!message)
			return;

		const sender = document.getElementById('id').textContent;
		const username = document.getElementById('username').textContent;
		
		if (chatSocket.socket.readyState === WebSocket.OPEN) {
			chatSocket.socket.send(JSON.stringify({
				'message': message,
				'sender': sender,
				'username': username,
			}));
		}

		messageInputDom.value = '';
	};
};