function statusProcess() {
	// Init the socket
	// let websocketProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
	// let websocketPort = window.location.protocol === 'https:' ? ':8001' : ':8000';
	// const socketUrl = websocketProtocol + '//' + window.location.hostname + websocketPort + '/ws/status/';
	const socketUrl = window.location.protocole === 'https' ? 'wss://localhost:8001/ws/status_secure/' : 'ws://localhost:8000/ws/status/';

	statusSocket = {
		socket: new WebSocket(socketUrl),
		url: socketUrl,
		shouldClose: false
	};

	console.log('Status socket created', statusSocket.socket);

	// Update the status of users
	statusSocket.socket.onmessage = function(e) {
		const data = JSON.parse(e.data);
		const id = data.id;
		const status = data.status;
		console.log('Status of user ' + id + ' changed to ' + status);

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
			console.log('Status socket closed. Reconnecting...');
			statusSocket.socket = new WebSocket(statusSocket.url);
			console.log('Status socket recreated', statusSocket.socket);
		}
		else {
			console.log('Status socket closed');
		}
	};

	
	// Close the socket when the user leaves the page
	window.onbeforeunload = function() {
		statusSocket.shouldClose = true;
		statusSocket.socket.close();
	}
}