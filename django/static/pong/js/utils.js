function getPaddleDirection(key) {
	if (key === 'o' || key === 'w' || key === 'x' || key === 'ArrowRight' || key === 'ArrowUp') {
		return 'up';
	} else if (key === 'l' || key === 's' || key === 'z' || key === 'ArrowLeft' || key === 'ArrowDown') {
		return 'down';
	}
}

function getSocket(gameID) {
	let socketUrl;
	if (window.location.protocol === 'https:') {
		socketUrl = 'wss://localhost:8001/wss/game/';
	} else {
		socketUrl = 'ws://localhost:8000/ws/game/';
	}
	socketUrl += gameID + '/';

	socket = {
		socket: new WebSocket(socketUrl),
		url: socketUrl,
		shouldClose: false
	};
	return (socket)
}