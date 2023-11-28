import * as utils from './utils.js';

let     websocketProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
let     websocketPort = window.location.protocol === 'https:' ? ':8001' : '';
const   socketUrl = websocketProtocol + '//' + window.location.host + websocketPort + '/ws/some_path/';
const   socket = new WebSocket(socketUrl);

const   keyState = {
    ArrowUp: false,
    ArrowDown: false,
    w: false,
    s: false,
};

const   paddlePosition = {
    left: 0,
    right: 0,
    // TODO add top and bottom
};

const   ballPosition = {
    x: 10,
    y: 10,
};

// EVENTS
document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('keydown', function(event) {
        if (!keyState[event.key] && keyState.hasOwnProperty(event.key)) {
            keyState[event.key] = true;
            const message = {
                type: 'paddle_move',
                key: 'keydown',
                direction: utils.getPaddleDirection(event.key),
                id: utils.getPaddleID(event.key),
            };
            socket.send(JSON.stringify(message));
        }
    });

    document.addEventListener('keyup', function(event) {
        if (keyState.hasOwnProperty(event.key)) {
            keyState[event.key] = false;
            const message = {
                type: 'paddle_move',
                key: 'keyup',
                direction: utils.getPaddleDirection(event.key),
                id: utils.getPaddleID(event.key),
            };
            socket.send(JSON.stringify(message));
        }
    });

    socket.addEventListener('open', (event) => {
        const message = {
            type: 'init_game',
            canvasWidth: config.width,
            canvasHeight: config.height,
            paddlePositionLeft: paddlePosition.left,
            paddlePositionRight: paddlePosition.right,
            ballPositionX: ballPosition.x,
            ballPositionY: ballPosition.y,
        };
        socket.send(JSON.stringify(message));
    });

    socket.addEventListener('message', (event) => {
        let message = JSON.parse(event.data);

        if (message.type === 'update_paddle_position') {
            if (message.id === 'left') {
                paddlePosition.left = parseFloat(message.position);
                updatePaddlePosition()
            } else if (message.id === 'right') {
                paddlePosition.right = parseFloat(message.position);
                updatePaddlePosition()
            }
        }

        if (message.type === 'update_ball_position') {
            ballPosition.x = parseFloat(message.x);
            ballPosition.y = parseFloat(message.y);
            updateBallPosition()
        }
    });
});


var phaserGame;
var config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    physics: {
        default: 'arcade',
        arcade: {
            gravity: { y: 0 },
            debug: false
        }
    },
    scene: {
        preload: preload,
        create: create,
        update: update,
        updatePaddlePosition: updatePaddlePosition,
        updateBallPosition: updateBallPosition,
    }
};

phaserGame = new Phaser.Game(config);
const elements = {
    paddles: {
        left: null,
        right: null,
    },
    ball: null,
};

function preload() {
    // this.load.image('paddle', 'test.jpg');
}

function create() {
    // var rect = new Phaser.Geom.Rectangle(400, 300, 100, 100);
    elements.paddles.left = this.add.rectangle(10, paddlePosition.left + 50, 10, 100, 0xffffff);
    elements.paddles.right = this.add.rectangle(config.width - 10, paddlePosition.right + 50, 10, 100, 0xffffff);

    elements.ball = this.add.circle(ballPosition.x, ballPosition.y, 8, 0xffffff);
}

function update() {
    // elements.paddles.left.y = paddlePosition.left;
    // elements.paddles.right.y = paddlePosition.right;
    // elements.ball.x = ballPosition.x;
    // elements.ball.y = ballPosition.y;
}

function updatePaddlePosition() {
    elements.paddles.left.y = paddlePosition.left + 50;
    elements.paddles.right.y = paddlePosition.right + 50;
}

function updateBallPosition() {
    elements.ball.x = ballPosition.x;
    elements.ball.y = ballPosition.y;
}