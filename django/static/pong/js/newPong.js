const elements = {
	field: null,
	paddles: [],
	ball: null,
}

const   keyState = {
    w: false,
    s: false,
    o: false,
    l: false,
	z: false,
	x: false,
	ArrowLeft: false,
	ArrowRight: false,
    ArrowUp: false,
    ArrowDown: false,
};

const	sizes = {
    canvas: 800,
    paddleSize: 100,
    paddleThickness: 20,
    offset: 20,
};
sizes.field = sizes.paddleThickness + sizes.offset;

function createGameCanvas() {
	const gameCanvas = document.getElementById('gameCanvas');
    gameCanvas.width = sizes.canvas;
    gameCanvas.height = sizes.canvas;

    const gameContext = gameCanvas.getContext('2d');
    gameContext.fillStyle = "#212121";
    gameContext.fillRect(0, 0, gameCanvas.width, gameCanvas.height);

	elements.field = new Field(sizes.canvas);
	elements.field.draw(gameContext);

	return (gameCanvas, gameContext)
}

function gameProcess(isWaitingPage, gameMode, gameID, playerID) {
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

		if (message.type === 'reload_page') {
			router.navigate('/pong/game/' + gameMode);
		}

		if (message.type === 'init_paddle_position') {
			initPaddlePosition(message.id, message.position);
		}

		if (message.type === 'update_score') {
			updateScore(message);
		}

		if (message.type === 'update_paddle_position') {
			updatePaddlePosition(message.id, message.position);
		}

		if (message.type === 'update_ball_position') {
			updateBallPosition(message.x, message.y, message.color, message.radius);
		}
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
				playerID: playerID,
                paddleKey: event.key,
            };
            socket.socket.send(JSON.stringify(message));
        }

        if (event.key === "ArrowUp" || event.key === "ArrowDown" || 
            event.key === "ArrowLeft" || event.key === "ArrowRight") {
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
				playerID: playerID,
                paddleKey: event.key,
            };
            socket.socket.send(JSON.stringify(message));
        }
    });
}