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
};

class Field {
	constructor(size) {
		this.x = 30;
		this.y = 30;
		this.width = size - 60;
		this.height = size - 60;
	}

	draw(context) {
		context.fillStyle = "#404040";
		context.fillRect(this.x, this.y, this.width, this.height);
	}
}

class Paddle {
	constructor(paddleID, position) {
		const paddleXpos = [10, 770, position, position];
		const paddleYpos = [position, position, 10, 770];
		const paddleColors = ['#E21E59', '#1598E9', '#2FD661', '#F19705'];

		this.x = paddleXpos[paddleID];
		this.y = paddleYpos[paddleID];
		this.color = paddleColors[paddleID];
		this.id = paddleID;
		this.width = 20;
		this.height = 100;
		if (paddleID >= 2) {
			this.width = 100;
			this.height = 20;
		}
	}

	draw(context) {
		context.fillStyle = this.color;
		context.fillRect(this.x, this.y, this.width, this.height);
	}
	
	clear(context) {
		context.fillStyle = "#212121";
		const clearXList = [0, 770, 0, 0]
		const clearYList = [0, 0, 0, 770]
		const clearWidthList = [30, 30, 800, 800]
		const clearHeightList = [800, 800, 30, 30]
		const clearX = clearXList[this.id]
		const clearY = clearYList[this.id]
		const clearWidth = clearWidthList[this.id]
		const clearHeight = clearHeightList[this.id]
		context.fillRect(clearX, clearY, clearWidth, clearHeight);
	}
}

class Ball {
	constructor(x, y, color, radius) {
		this.x = x;
		this.y = y;
		this.color = color;
		this.radius = radius;
	}

	draw(context) {
		context.fillStyle = this.color;
		context.beginPath();
		context.arc(this.x, this.y, this.radius, 0, 2 * Math.PI);
		context.fill();
	}

	clear(context) {
		context.fillStyle = "#212121";
		context.beginPath();
		context.arc(this.x, this.y, this.radius + 1, 0, 2 * Math.PI);
		context.fill();
	}
}


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

	elements.field = new Field(canvasSize);
	elements.field.draw(gameContext);

	return (gameCanvas, gameContext)
}

function initPaddlePosition(gameContext, paddleID, position) {
	elements.paddles[paddleID] = new Paddle(paddleID, position);
	elements.paddles[paddleID].draw(gameContext);
}

function updatePaddlePosition(gameContext, paddleID, position) {
	elements.paddles[paddleID].clear(gameContext);
	elements.paddles[paddleID].y = position;
	elements.paddles[paddleID].draw(gameContext);
}

function updateBallPosition(gameContext, x, y) {
	if (elements.ball) {
		elements.ball.clear(gameContext);
	}
	elements.ball = new Ball(x, y, '#FFFFFF', 10);
	elements.ball.draw(gameContext);
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
			initPaddlePosition(gameContext, message.id, message.position);
		}

		if (message.type === 'update_paddle_position') {
			updatePaddlePosition(gameContext, message.id, message.position);
		}

		if (message.type === 'update_ball_position') {
			updateBallPosition(gameContext, message.x, message.y);
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