// Global variables
let chatSockets = {};
let currentRoomID = '';


// Check changes on the chat page
function handleMutation() {
	const roomIDElement = document.getElementById('room-id');

	if (roomIDElement) {
		const roomID = JSON.parse(roomIDElement.textContent);
		
		// Change the room if the room ID has changed
		if (roomID !== currentRoomID) {
			currentRoomID = roomID;
			
			// Create a new socket if it doesn't exist
			if (!chatSockets[currentRoomID]) {
				let websocketProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
				let websocketPort = window.location.protocol === 'https:' ? ':8001' : ':8000';
				const socketUrl = websocketProtocol + '//' + window.location.hostname + websocketPort + '/ws/chat/' + roomID + "/";

				chatSockets[roomID] = {
					socket: new WebSocket(socketUrl),
					url: socketUrl,
					shouldClose: false
				};

			}
		}

		// Fetch the message history if the chat log is empty
		const chatLog = document.querySelector('#chat-log');
		if (chatLog && chatLog.innerHTML === '') {
			fetchMessageHistory(currentRoomID);
		}


		// Handle messages history
		function fetchMessageHistory(ID) {

			// Fetch the messages
			fetch('/api/chat/history/' + ID)
			.then(response => response.json())
			.then(messages => {

				const blockedUsersElement = document.getElementById('blocked-users');
				const blockedUsers = blockedUsersElement ? JSON.parse(blockedUsersElement.textContent) : [];
				
				const isPrivateElement = document.getElementById('is-private');
				const isPrivate = isPrivateElement ? JSON.parse(isPrivateElement.textContent) : false;

				// Display the messages
				for (const message of messages) {
					if (blockedUsers.includes(parseInt(message.sender, 10)))
						continue;

					const messageContainer = document.createElement('p');

					const username = typeof message.username === 'string' ? message.username.replace(/"/g, '') : '';
					messageContainer.textContent = isPrivate ? message.message : username + ': ' + message.message;
					
					const idElement = document.getElementById('id');
					messageContainer.className = idElement && message.sender === idElement.textContent ? 'my-message' : 'other-message';
					
					const chatLog = document.querySelector('#chat-log');
					if (chatLog) {
						chatLog.appendChild(messageContainer);
						chatLog.scrollTop = chatLog.scrollHeight;
					}
				}
			});
		}


		// Handle incoming messages
		chatSockets[currentRoomID].socket.onmessage = function(e) {
			const data = JSON.parse(e.data);
			
			const blockedUsersElement = document.getElementById('blocked-users');
			const blockedUsers = blockedUsersElement ? JSON.parse(blockedUsersElement.textContent) : [];
			
			const isPrivateElement = document.getElementById('is-private');
			const isPrivate = isPrivateElement ? JSON.parse(isPrivateElement.textContent) : false;

			if (data.sender && !blockedUsers.includes(parseInt(data.sender, 10))) {
				const messageContainer = document.createElement('p');

				const username = typeof data.username === 'string' ? data.username.replace(/"/g, '') : '';
				messageContainer.textContent = isPrivate ? data.message : username + ': ' + data.message;
				
				const idElement = document.getElementById('id');
				messageContainer.className = idElement && data.sender === idElement.textContent ? 'my-message' : 'other-message';
				
				const chatLog = document.querySelector('#chat-log');
				if (chatLog) {
					chatLog.appendChild(messageContainer);
					chatLog.scrollTop = chatLog.scrollHeight;
				}
			}
		};
		

		// Handle closing the socket
		chatSockets[currentRoomID].socket.onclose = function(e) {
			if (!this.shouldClose) {
				chatSockets[currentRoomID].socket = new WebSocket(chatSockets[currentRoomID].url);

				const chatLog = document.querySelector('#chat-log');
				if (chatLog) {
					chatLog.innerHTML = '';
					fetchMessageHistory(currentRoomID);
				}
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
			
			if (chatSockets[currentRoomID].socket.readyState === WebSocket.OPEN) {
				chatSockets[currentRoomID].socket.send(JSON.stringify({
					'message': message,
					'sender': sender,
					'username': username,
				}));
			}

			messageInputDom.value = '';
		};
	}
};


// Observe changes on the chat page
const observer = new MutationObserver(handleMutation);
observer.observe(document, { childList: true, subtree: true });