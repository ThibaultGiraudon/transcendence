document.addEventListener('DOMContentLoaded', function () {
	// Init the socket
	let websocketProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
	let websocketPort = window.location.protocol === 'https:' ? ':8001' : ':8000';
	const socketUrl = websocketProtocol + '//' + window.location.hostname + websocketPort + '/ws/notifications/';

	notificationSocket = {
		socket: new WebSocket(socketUrl),
		url: socketUrl,
		shouldClose: false
	};

	// Update the notification count
	notificationSocket.socket.onmessage = function(e) {
		document.getElementById('notification-count').textContent = parseInt(
			document.getElementById('notification-count').textContent
		) + 1;
	};

	
	// Close the socket
	notificationSocket.socket.onclose = function(e) {
		if (!this.shouldClose) {
			notificationSocket.socket = new WebSocket(notificationSocket.url);
		}
	};


	// Close the socket when the user leaves the page
	window.onbeforeunload = function() {
		if (notificationSocket !== null) {
			notificationSocket.shouldClose = true;
			notificationSocket.socket.close();
		}
	}
});