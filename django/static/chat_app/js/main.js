const roomName = JSON.parse(document.getElementById('room-name').textContent);
    
let		websocketProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
let		websocketPort = window.location.protocol === 'https:' ? ':8001' : ':8000';
const	socketUrl = websocketProtocol + '//' + window.location.hostname + websocketPort + '/ws/chat/' + roomName + "/";
const	chatSocket = new WebSocket(socketUrl);

document.addEventListener('DOMContentLoaded', (event) => {
    // Votre code ici
	console.log(chatSocket)

	chatSocket.onmessage = function(e) {
		const data = JSON.parse(e.data);
		const blockedUsers = JSON.parse(document.getElementById('blocked-users').textContent);
		
		if (!blockedUsers.includes(parseInt(data.sender, 10))) {
			const messageContainer = document.createElement('p');
			messageContainer.textContent = data.username + ': ' + data.message;
			messageContainer.className = data.sender === "{{ request.user.id }}" ? 'my-message' : 'other-message';
			document.querySelector('#chat-log').appendChild(messageContainer);
			var chatLog = document.querySelector('.chat-log');
			chatLog.scrollTop = chatLog.scrollHeight;
		}
	};

	chatSocket.onopen = function(e) {
		document.querySelector('#chat-log').innerHTML = '';
	};

	chatSocket.onclose = function(e) {
		console.error('Chat socket closed unexpectedly');
	};

	chatSocket.onerror = function(e) {
		console.error('WebSocket error: ', e);
	};

	document.querySelector('#chat-message-input').focus();
	document.querySelector('#chat-message-input').onkeyup = function(e) {
		if (e.key === 'Enter') {
			document.querySelector('#chat-message-submit').click();
		}
	};

	document.querySelector('#chat-message-submit').onclick = null;
	document.querySelector('#chat-message-submit').onclick = function(e) {
		const messageInputDom = document.querySelector('#chat-message-input');
		const message = messageInputDom.value.trim();
		if (!message)
		return;
	const sender = "{{ request.user.id }}";
		const username = "{{ request.user.username }}";
		chatSocket.send(JSON.stringify({
			'message': message,
			'sender': sender,
			'username': username,
		}));
		messageInputDom.value = '';
	};
});