function getPaddleDirection(key) {
	if (key === 'o' || key === 'w' || key === 'x' || key === 'ArrowRight' || key === 'ArrowUp') {
		return 'up';
	} else if (key === 'l' || key === 's' || key === 'z' || key === 'ArrowLeft' || key === 'ArrowDown') {
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

	// let socketUrl;
	// if (window.location.protocol === 'https:') {
	// 	socketUrl = 'wss://localhost:8443/wss/game/';
	// } else {
	// 	socketUrl = 'ws://localhost:8000/ws/game/';
	// }
	// socketUrl += gameID + '/';

	// socket = {
	// 	socket: new WebSocket(socketUrl),
	// 	url: socketUrl,
	// 	shouldClose: false
	// };
	return (socket)
}