document.addEventListener('DOMContentLoaded', function () {
	// Init the socket
	// let websocketProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
	// let websocketPort = window.location.protocol === 'https:' ? ':8001' : ':8000';
	// const socketUrl = websocketProtocol + '//' + window.location.hostname + websocketPort + '/ws/notifications/';
	const socketUrl = window.location.protocole === 'https' ? 'wss://localhost:8001/ws/notifications_secure/' : 'ws://localhost:8000/ws/notifications/';

	notificationSocket = {
		socket: new WebSocket(socketUrl),
		url: socketUrl,
		shouldClose: false
	};

	console.log('Notification socket created', notificationSocket.socket);

	// Update the notification count
	notificationSocket.socket.onmessage = function(e) {
		document.getElementById('notification-count').textContent = parseInt(
			document.getElementById('notification-count').textContent
		) + 1;
	};

	
	// Close the socket
	notificationSocket.socket.onclose = function(e) {
		if (!notificationSocket.shouldClose) {
			console.log('Notification socket closed. Reconnecting...');
			notificationSocket.socket = new WebSocket(notificationSocket.url);
			console.log('Notification socket recreated', notificationSocket.socket);
		}
		else {
			console.log('Notification socket closed');
		}
	};


	// Close the socket when the user leaves the page
	window.onbeforeunload = function() {
		notificationSocket.shouldClose = true;
		notificationSocket.socket.close();
	}
});