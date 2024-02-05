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
	constructor(paddleID) {
		this.id = paddleID;
		this.width = sizes.paddleThickness;
		this.height = sizes.paddleSize;
		if (paddleID >= 2) {
			this.width = sizes.paddleSize;
			this.height = sizes.paddleThickness;
		}
		const canvas = document.getElementById('paddle' + (parseInt(paddleID) + 1) + 'Layer');
		if (!canvas) {
			return;
		}
		canvas.width = sizes.canvas;
		canvas.height = sizes.canvas;		
		this.context = canvas.getContext('2d');
	}

	draw(position) {
		const bottomLimit = sizes.offset;
		const topLimit = sizes.canvas - sizes.field;

		const paddleXpos = [bottomLimit, topLimit, position, position];
		const paddleYpos = [position, position, bottomLimit, topLimit];
		const paddleColors = ['#E21E59', '#1598E9', '#2FD661', '#F19705'];

		this.x = paddleXpos[this.id];
		this.y = paddleYpos[this.id];
		this.color = paddleColors[this.id];
		if (!this.context) {
			return;
		}
		this.context.fillStyle = this.color;
		this.context.fillRect(this.x, this.y, this.width, this.height);
	}
	
	clear() {
		if (this.context) {
			this.context.clearRect(0, 0, sizes.canvas, sizes.canvas)
		}
	}
}

class Ball {
	constructor(x, y, color, radius) {
		this.x = x;
		this.y = y;
		this.color = color;
		this.radius = radius;
		const canvas = document.getElementById('ballLayer');
		if (!canvas) {
			return;
		}
		canvas.width = sizes.canvas;
		canvas.height = sizes.canvas;
		this.context = canvas.getContext('2d');
	}

	draw(x, y, color, radius) {
		this.x = x;
		this.y = y;
		this.color = color;
		this.radius = radius;
		if (!this.context) {
			return;
		}
		this.context.fillStyle = this.color;
		this.context.beginPath();
		this.context.arc(this.x, this.y, this.radius, 0, 2 * Math.PI);
		this.context.fill();
	}

	clear() {
		if (this.context) {
			this.context.clearRect(0, 0, sizes.canvas, sizes.canvas)
		}
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

function initPaddlePosition(paddleID, position) {
	elements.paddles[paddleID] = new Paddle(paddleID);
	elements.paddles[paddleID].draw(position);
}

function updatePaddlePosition(paddleID, position) {
	elements.paddles[paddleID].clear();
	elements.paddles[paddleID].draw(position);
}

function updateScore(message) {
    const backgroundColors = ['#E21E59', '#1598E9', '#2FD661', '#F19705'];
    const scoreSpans = document.querySelectorAll('.player_score');

    if (message.nbPaddles == 2) {
        scoreSpans[message.id].style.width = '50%';
    } else if (message.nbPaddles == 4) {
        scoreSpans[message.id].style.width = '25%';
    }
    scoreSpans[message.id].textContent = message.score;
    scoreSpans[message.id].style.backgroundColor = backgroundColors[message.id];
	if (message.score >= 10) {
		scoreSpans[message.id].style.backgroundColor = '#212121';
		scoreSpans[message.id].style.color = '#DADADA';
		elements.paddles[message.id].clear();
		elements.paddles[message.id].draw();
	}
}

function updateBallPosition(x, y, color, radius) {
	if (elements.ball) {
		elements.ball.clear();
	}
	elements.ball = new Ball(x, y, color, radius);
	elements.ball.draw(x, y, color, radius);
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
                id: getPaddleID(event.key),
            };
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