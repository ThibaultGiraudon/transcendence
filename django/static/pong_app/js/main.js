// TODO separer dans des fichiers differents

const   keyState = {
    o: false,
    l: false,
    w: false,
    s: false,
    z: false,
    x: false,
    n: false,
    m: false,
};

var phaserGame;
var config = {
    type: Phaser.AUTO,
    width: 0,
    height: 0,
    physics: {
        default: 'arcade',
        arcade: {
            gravity: { y: 0 },
            debug: false
        }
    },
    scene: {
        create: create,
        updatePaddlePosition: updatePaddlePosition,
        updateBallPosition: updateBallPosition,
    },
    backgroundColor: '#212121',
};

const elements = {
    scoreText: [],
    paddles: [],
    ball: null,
    field: null,
};

function create() {
    elements.field = this.add.rectangle(0, 0, 0, 0, 0x404040, 0.4).setVisible(true);
    elements.ball = this.add.circle(0, 0, 0, 0xFDF3E1).setVisible(false);
    for (let i = 0; i < 4; i++) {
        elements.paddles[i] = this.add.rectangle(0, 0, 0, 0, 0xFFFFFF).setVisible(false);
    }
}

function displayGameOver(message) {
    elements.ball.setVisible(false);
    elements.paddles.forEach(element => {
        element.setVisible(false);
    });
    phaserGame.destroy();

    // TODO add player from message
    const route = '/pong/game_over/elias';
    navigateTo(event, route);
}

function initsquareSize(message) {
    config.width = message.size;
    config.height = message.size;
    phaserGame = new Phaser.Game(config);
}

function initPaddlePosition(message, paddle) {
    paddle.setVisible(true)
    paddle.x = parseFloat(message.x)
    paddle.y = parseFloat(message.y)
    paddle.width = parseFloat(message.width)
    paddle.height = parseFloat(message.height)
    paddle.setFillStyle(message.color, 1);
    const limit = parseFloat(message.limit);
    elements.field.x = limit
    elements.field.y = limit
    elements.field.width = config.width - limit * 2
    elements.field.height = config.height - limit * 2
}

function initScore(message) {
    const backgroundColors = ['#E21E59', '#1598E9', '#2FD661', '#F19705'];
    const scoreSpans = document.querySelectorAll('.player_score');

    if (message.nbPaddles == 2) {
        scoreSpans[message.id].style.width = '50%';
    } else if (message.nbPaddles == 4) {
        scoreSpans[message.id].style.width = '25%';
    }
    scoreSpans[message.id].textContent = message.score;
    scoreSpans[message.id].style.backgroundColor = backgroundColors[message.id];
    changeAllScores(message);
}

function updatePaddlePosition(message) {
    if (message.id == 0) {
        elements.paddles[0].y = parseFloat(message.position)
    } else if (message.id == 1) {
        elements.paddles[1].y = parseFloat(message.position)
    } else if (message.id == 2) {
        elements.paddles[2].x = parseFloat(message.position)
    } else if (message.id == 3) {
        elements.paddles[3].x = parseFloat(message.position)
    }
}

function updateBallPosition(message) {
    elements.ball.setVisible(true)
    elements.ball.x = parseFloat(message.x)
    elements.ball.y = parseFloat(message.y)
    elements.ball.radius = parseFloat(message.radius)
    elements.ball.setFillStyle(message.color, 1);
}

function updateScore(message) {
    const scoreSpans = document.querySelectorAll('.player_score');
    scoreSpans[message.id].textContent = message.score;
    changeAllScores(message);
}

function changeAllScores(message) {
    if (message.score >= 10) {
        if (message.nbPaddles == 4) {
            scoreSpans[message.id].style.backgroundColor = '#212121';
            scoreSpans[message.id].style.color = '#DADADA';
            elements.paddles[message.id].setVisible(false);
        } 
    }
}

function gameProcess() {
    let     websocketProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    let     websocketPort = window.location.protocol === 'https:' ? ':8001' : ':8000';
    const   socketUrl = websocketProtocol + '//' + window.location.hostname + websocketPort + '/ws/some_path/';
    const   socket = new WebSocket(socketUrl);

    document.addEventListener('keydown', function(event) {
        if (!keyState[event.key] && keyState.hasOwnProperty(event.key)) {
            keyState[event.key] = true;
            const message = {
                type: 'paddle_move',
                key: 'keydown',
                direction: getPaddleDirection(event.key),
                id: getPaddleID(event.key),
            };
            socket.send(JSON.stringify(message));
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
            socket.send(JSON.stringify(message));
        }
    });
        
    socket.addEventListener('open', (event) => {
        console.log('socket open');
        const gameMode = document.querySelector('script[data-game-mode]').getAttribute('data-game-mode');
        // const gameMode = document.getElementById('game-mode').getAttribute('data-game-mode');
        // const gameMode = document.getElementById('game-mode').textContent;
        console.log(gameMode);
        const message = {
            type: gameMode,
        };
        socket.send(JSON.stringify(message));
    });

    socket.addEventListener('message', (event) => {
        let message = JSON.parse(event.data);

        if (message.type === 'game_over') {
            console.log(message);
            displayGameOver(message);
        }

        if (message.type === 'init_game_size') {
            initsquareSize(message);
        }

        if (message.type === 'init_paddle_position') {
            initPaddlePosition(message, elements.paddles[message.id]);
        }

        if (message.type === 'init_score') {
            initScore(message);
        }

        if (message.type === 'update_paddle_position') {
            updatePaddlePosition(message);
        }

        if (message.type === 'update_ball_position') {
            updateBallPosition(message);
        }

        if (message.type === 'update_score') {
            updateScore(message);
        }
    });

    console.log('game page');
}