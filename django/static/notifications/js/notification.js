document.addEventListener('DOMContentLoaded', function () {
	// Init the socket
	let websocketProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
	let websocketPort = window.location.protocol === 'https:' ? ':8001' : ':8000';
	const socketUrl = websocketProtocol + '//' + window.location.hostname + websocketPort + '/ws/notifications/';

	chatSocket = {
		socket: new WebSocket(socketUrl),
		url: socketUrl,
		shouldClose: false
	};

	console.log('Notifications socket created', chatSocket.socket);

	// Update the notification count
	chatSocket.socket.onmessage = function(e) {
		console.log('Notification received', e.data);
		document.getElementById('notification-count').textContent = parseInt(
			document.getElementById('notification-count').textContent
		) + 1;
	};

	// Close the socket
	chatSocket.socket.onclose = function(e) {
		if (!chatSocket.shouldClose) {
			console.error('Chat socket closed unexpectedly');
			chatSocket.socket = new WebSocket(chatSocket.url);
		} else {
			console.log('Chat socket closed');
		
		}
	};

	// Close the socket when the user leaves the page
	window.onbeforeunload = function() {
		console.log('Leaving the page so close the socket:');
		chatSocket.shouldClose = true;
		chatSocket.socket.close();
	}
});