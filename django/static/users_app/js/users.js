function statusProcess() {
	// Init the socket
	const socketUrl = window.location.protocole === 'https' ? 'wss://localhost:8001/ws/status_secure/' : 'ws://localhost:8000/ws/status/';

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

		// Dont display if the user is in a chat
		if (status.indexOf('chat') !== -1) {
			status = 'online';
		}

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