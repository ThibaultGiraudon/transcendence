let statusSocket = null;

document.addEventListener('DOMContentLoaded', function () {
	// Init the socket
	let websocketProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
	let websocketPort = window.location.protocol === 'https:' ? ':8443' : ':8000';
	const statusSocketUrl = websocketProtocol + '//' + window.location.hostname + websocketPort + '/ws/status/';

	statusSocket = {
		socket: new WebSocket(statusSocketUrl),
		url: statusSocketUrl,
		shouldClose: false
	};


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
		if (!statusSocket.shouldClose && this.readyState !== WebSocket.CLOSED) {
			statusSocket.socket = new WebSocket(statusSocket.url);
		}
	};

	// Close the socket when the user leaves the page
	window.onbeforeunload = function() {
		if (statusSocket !== null && statusSocket.socket.readyState === WebSocket.OPEN) {
			statusSocket.shouldClose = true;
			statusSocket.socket.close();
		}
	};
});


function SignOutProcess(id) {
	// Send a message to the websocket when the user logged out
	var signOutButton = document.getElementById('sign-out');
	if (signOutButton) {
		try {
			statusSocket.socket.send(JSON.stringify({
				'id': id,
				'status': 'offline'
			}));
		} catch (error) {}
	}
}

function SignInProcess(id) {
	// Send a message to the websocket when the user logged in
	var signInButton = document.getElementById('set-status-online');
	if (signInButton) {
		var socketConnectedPromise = new Promise(function(resolve, reject) {
			var checkSocketStatus = setInterval(function() {
				if (statusSocket.socket.readyState === WebSocket.OPEN) {
					clearInterval(checkSocketStatus);
					resolve();
				} else if (statusSocket.socket.readyState === WebSocket.CLOSED || statusSocket.socket.readyState === WebSocket.CLOSING) {
					clearInterval(checkSocketStatus);
					reject(new Error('Socket connection failed.'));
				}
			}, 100);
		});

		socketConnectedPromise.then(function() {
			statusSocket.socket.send(JSON.stringify({
				'id': id,
				'status': 'online'
			}));
		}).catch(function(error) {});
	}
}