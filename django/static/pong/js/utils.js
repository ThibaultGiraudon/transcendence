function getPaddleDirection(key) {
	if (key === 'o' || key === 'w' || key === 'x' || key === 'ArrowLeft' || key === 'ArrowUp') {
		return 'up';
	} else if (key === 'l' || key === 's' || key === 'z' || key === 'ArrowRight' || key === 'ArrowDown') {
		return 'down';
	}
}

function getSocket(gameID) {
	let websocketProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
	let websocketPort = window.location.protocol === 'https:' ? ':8443' : ':8000';
	const socketUrl = websocketProtocol + '//' + window.location.hostname + websocketPort + '/ws/game/' + gameID + "/";

	socket = {
		socket: new WebSocket(socketUrl),
		url: socketUrl,
		shouldClose: false
	};
	return (socket)
}