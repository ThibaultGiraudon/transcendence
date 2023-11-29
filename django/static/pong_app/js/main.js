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
    id0: 0,
    id1: 0,
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
            // paddlePositionLeft: paddlePosition.id0,
            // paddlePositionRight: paddlePosition.id1,
            // ballPositionX: ballPosition.x,
            // ballPositionY: ballPosition.y,
        };
        socket.send(JSON.stringify(message));
    });

    socket.addEventListener('message', (event) => {
        let message = JSON.parse(event.data);

        if (message.type === 'update_paddle_position') {
            console.log(message);
            updatePaddlePosition(message);
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
        id0: null,
        id1: null,
    },
    ball: null,
};

function preload() {
    // this.load.image('paddle', 'test.jpg');
}

function create() {
    elements.paddles.id0 = this.add.rectangle(0, 0, 10, 100, 0xffffff).setVisible(false);
    elements.paddles.id1 = this.add.rectangle(0, 0, 10, 100, 0xffffff).setVisible(false);

    elements.ball = this.add.circle(ballPosition.x, ballPosition.y, 8, 0xffffff);
}

function update() {
    // pass
}

function updatePaddlePosition(message) {
    if (message.id == 0) {
        elements.paddles.id0.setVisible(true);
        elements.paddles.id0.y = parseFloat(message.position) + 50
    } else if (message.id == 1) {
        elements.paddles.id1.setVisible(true);
        elements.paddles.id1.y = parseFloat(message.position) + 50
    }
}

function updateBallPosition() {
    elements.ball.x = ballPosition.x;
    elements.ball.y = ballPosition.y;
}