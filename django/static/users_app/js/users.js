function statusProcess() {
	// Init the socket
	let websocketProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
	let websocketPort = window.location.protocol === 'https:' ? ':8001' : ':8000';
	const socketUrl = websocketProtocol + '//' + window.location.hostname + websocketPort + '/ws/status/';

	statusSocket = {
		socket: new WebSocket(socketUrl),
		url: socketUrl,
		shouldClose: false
	};


	// Update the status of users
	statusSocket.socket.onmessage = function(e) {
		const data = JSON.parse(e.data);
		const id = data.id;
		const status = data.status;

		var userElement = document.querySelector('.container[data-user-id="' + id + '"]');

		if (userElement) {
			var statusElement = userElement.querySelector('.status');
			if (statusElement) {
				statusElement.textContent = status;
			}
		}
	};


	// Close the socket
	statusSocket.socket.onclose = function(e) {
		if (!statusSocket.shouldClose) {
			statusSocket.socket = new WebSocket(statusSocket.url);
		}
	};

	
	// Close the socket when the user leaves the page
	window.onbeforeunload = function() {
		statusSocket.shouldClose = true;
		statusSocket.socket.close();
	}
}