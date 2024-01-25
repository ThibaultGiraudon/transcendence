const elements = {
	paddles: [],
	ball: null,
}

const   keyState = {
    w: false,
    s: false,
    o: false,
    l: false,
};

function getPaddleID(key) {
	if (key === 'w' || key === 's') {
		return '0';
	} else if (key === 'o' || key === 'l') {
		return '1';
	}
}

function getPaddleDirection(key) {
	if (key === 'o' || key === 'w') {
		return 'up';
	} else if (key === 'l' || key === 's') {
		return 'down';
	}
}

function createGameCanvas() {
	const canvasSize = 800;

	const gameCanvas = document.getElementById('gameCanvas');
    gameCanvas.width = canvasSize;
    gameCanvas.height = canvasSize;

    const gameContext = gameCanvas.getContext('2d');
    gameContext.fillStyle = "#212121";
    gameContext.fillRect(0, 0, gameCanvas.width, gameCanvas.height);

	createGameField(gameContext, canvasSize);

	return (gameCanvas, gameContext)	
}

// function clearGameContext(gameCanvas, gameContext) {
// 	gameContext.clearRect(0, 0, gameCanvas.width, gameCanvas.height);
// 	gameCanvas, gameContext = createGameCanvas();
// 	return (gameCanvas, gameContext)
// }

function createGameField(gameContext, size) {
	fieldSize = 30;
    const gameField = {
        x: fieldSize,
        y: fieldSize,
        width: size - fieldSize * 2,
        height: size - fieldSize * 2
    };
    gameContext.fillStyle = "#404040";
    gameContext.fillRect(gameField.x, gameField.y, gameField.width, gameField.height);
}

function createPaddle(gameContext, paddleID, position) {
	const paddleXpos = [10, 770, position, position];
	const paddleYpos = [position, position, 10, 770];
    const paddleColors = ['#E21E59', '#1598E9', '#2FD661', '#F19705'];

	posX = paddleXpos[paddleID];
	posY = paddleYpos[paddleID];
	color = paddleColors[paddleID];

	paddleWidth = 20;
	paddleHeight = 100;
	if (paddleID >= 2) {
		paddleWidth = 100;
		paddleHeight = 20;
	}

	if (elements.paddles[paddleID] == null) {
		elements.paddles[paddleID] = {
			x: posX,
			y: posY,
			width: paddleWidth,
			height: paddleHeight
		};
		paddle = elements.paddles[paddleID];

		gameContext.fillStyle = color;
		gameContext.fillRect(paddle.x, paddle.y, paddle.width, paddle.height);
	}
}

function updatePaddlePosition(gameContext, paddleID, position) {
	paddle = elements.paddles[paddleID];
	gameContext.clearRect(paddle.x, paddle.y, paddle.width, paddle.height);
	// paddle.y = position;
	// gameContext.fillStyle = "#E21E59";
	// gameContext.fillRect(paddle.x, paddle.y, paddle.width, paddle.height);

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

function gameProcessLoaded(isWaitingPage) {
	const gameIDElement = document.getElementById('game_id');
	const gameModeElement = document.getElementById('game_mode');
	const playerIDELement = document.getElementById('player_id');
	if (!gameIDElement || !gameModeElement || !playerIDELement) {
		setTimeout(function() {gameProcessLoaded(isWaitingPage)}, 200);
		return;
	}
	const gameID = JSON.parse(gameIDElement.textContent);
	const gameMode = JSON.parse(gameModeElement.textContent);
	const playerID = JSON.parse(playerIDELement.textContent);

	if (!isWaitingPage) {
		gameCanvas, gameContext = createGameCanvas();
	}

	const socket = getSocket(gameID);

    socket.socket.onopen = function() {
		if (isWaitingPage) {
			return;
		}
		const message = {
			type: gameMode,
			playerID: playerID,
			action: 'newPlayer'
		};
		socket.socket.send(JSON.stringify(message));
        console.log('Message envoyé :', message);
    };

    socket.socket.onmessage = function(event) {
        const message = JSON.parse(event.data);

		if (message.type === 'init_paddle_position') {
			createPaddle(gameContext, message.id, message.position);
		}

		if (message.type === 'update_paddle_position') {
			updatePaddlePosition(gameContext, message.id, message.position);
		}

        console.log('Message reçu:', message);
    };

    socket.socket.onclose = function(event) {
        console.log('Connexion WebSocket fermée', event);
    };

    document.addEventListener('keydown', function(event) {
        if (!keyState[event.key] && keyState.hasOwnProperty(event.key)) {
            keyState[event.key] = true;
            const message = {
                type: 'paddle_move',
                key: 'keydown',
                direction: getPaddleDirection(event.key),
                id: getPaddleID(event.key),
            };
			console.log("keydown");
            socket.socket.send(JSON.stringify(message));
        }

        if (event.key === "ArrowUp" || event.key === "ArrowDown") {
            event.preventDefault();
        }
    });

    document.addEventListener('keyup', function(event) {
        if (keyState.hasOwnProperty(event.key)) {
            keyState[event.key] = false;
            const message = {
                type: 'paddle_move',
                key: 'keyup',
                direction: getPaddleDirection(event.key),
                id: getPaddleID(event.key),
            };
            socket.socket.send(JSON.stringify(message));
        }
    });
}

function gameProcess(isWaitingPage) {
	gameProcessLoaded(isWaitingPage);
}