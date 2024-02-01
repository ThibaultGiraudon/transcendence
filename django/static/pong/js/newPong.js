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

const	sizes = {
    canvas: 800,
    paddleSize: 100,
    paddleThickness: 20,
    offset: 20,
};
sizes.field = sizes.paddleThickness + sizes.offset;

class Field {
	constructor(size) {
		this.x = sizes.field;
		this.y = sizes.field;
		this.width = size - sizes.field * 2;
		this.height = size - sizes.field * 2;
	}

	draw(context) {
		context.fillStyle = "#404040";
		context.fillRect(this.x, this.y, this.width, this.height);
	}
}

class Paddle {
	constructor(paddleID, position) {
		const bottomLimit = sizes.offset;
		const topLimit = sizes.canvas - sizes.field;

		const paddleXpos = [bottomLimit, topLimit, position, position];
		const paddleYpos = [position, position, bottomLimit, topLimit];
		const paddleColors = ['#E21E59', '#1598E9', '#2FD661', '#F19705'];

		this.x = paddleXpos[paddleID];
		this.y = paddleYpos[paddleID];
		this.color = paddleColors[paddleID];
		this.id = paddleID;
		this.width = sizes.paddleThickness;
		this.height = sizes.paddleSize;
		if (paddleID >= 2) {
			this.width = sizes.paddleSize;
			this.height = sizes.paddleThickness;
		}
	}

	draw(context) {
		context.fillStyle = this.color;
		context.fillRect(this.x, this.y, this.width, this.height);
	}
	
	clear(context) {
		const bottomLimit = sizes.offset;
		const topLimit = sizes.canvas - sizes.field;

		context.fillStyle = "#212121";
		const clearXList = [0, topLimit, 0, 0]
		const clearYList = [0, 0, 0, topLimit]
		const clearWidthList =  [sizes.field, sizes.field, sizes.canvas, sizes.canvas]
		const clearHeightList = [sizes.canvas, sizes.canvas, sizes.field, sizes.field]
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
		// Here we add 10px because the ball is 20px diameter
		const bottomLimit = sizes.field + 10
		const topLimit = sizes.canvas - sizes.field - 10
		if (this.x < bottomLimit || this.x > topLimit || this.y < bottomLimit || this.y > topLimit) {
			context.fillStyle = "#212121";
			context.beginPath();
			context.arc(this.x, this.y, this.radius + 1, 0, 2 * Math.PI);
			context.fill();
		}
		elements.field.draw(context);
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

function initPaddlePosition(gameContext, paddleID, position) {
	elements.paddles[paddleID] = new Paddle(paddleID, position);
	elements.paddles[paddleID].draw(gameContext);
}

function updatePaddlePosition(gameContext, paddleID, position) {
	elements.paddles[paddleID].clear(gameContext);
	elements.paddles[paddleID].y = position;
	elements.paddles[paddleID].draw(gameContext);
}

// TODO add radius from message
function updateBallPosition(gameContext, x, y, color) {
	if (elements.ball) {
		elements.ball.clear(gameContext);
	}
	elements.ball = new Ball(x, y, color, 10);
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

var gameSocket = null;

function gameProcess(isWaitingPage, gameMode, gameID, playerID) {
	if (!isWaitingPage) {
		gameCanvas, gameContext = createGameCanvas();
	}

	gameSocket = getSocket(gameID);

    gameSocket.socket.onopen = function() {
		if (isWaitingPage) {
			return;
		}
		const message = {
			type: gameMode,
			playerID: playerID,
			action: 'newPlayer'
		};
		gameSocket.socket.send(JSON.stringify(message));
        console.log('Message envoyé :', message);
    };

    gameSocket.socket.onmessage = function(event) {
        const message = JSON.parse(event.data);

		if (message.type === 'reload_page') {
			router.navigate('/pong/game/' + gameMode);
		}

		if (message.type === 'init_paddle_position') {
			initPaddlePosition(gameContext, message.id, message.position);
		}

		if (message.type === 'update_paddle_position') {
			updatePaddlePosition(gameContext, message.id, message.position);
		}

		if (message.type === 'update_ball_position') {
			updateBallPosition(gameContext, message.x, message.y, message.color);
		}
    };

    gameSocket.socket.onclose = function(event) {
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
            gameSocket.socket.send(JSON.stringify(message));
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
            gameSocket.socket.send(JSON.stringify(message));
        }
    });
}