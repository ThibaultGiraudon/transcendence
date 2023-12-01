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
        };
        socket.send(JSON.stringify(message));
    });

    socket.addEventListener('message', (event) => {
        let message = JSON.parse(event.data);

        if (message.type === 'init_paddle_position') {
            initPaddlePosition(message);
        }

        if (message.type === 'update_paddle_position') {
            updatePaddlePosition(message);
        }

        if (message.type === 'update_ball_position') {
            updateBallPosition(message);
        }
    });
});


var phaserGame;
var config = {
    type: Phaser.AUTO,
    // TODO change to dynamic
    width: 800,
    height: 800,
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
    },
    backgroundColor: '#080808',
};

phaserGame = new Phaser.Game(config);
const elements = {
    paddles: {
    },
    ball: null,
};

function preload() {
    // this.load.image('paddle', 'test.jpg');
}

function create() {
    for (let i = 0; i < 4; i++) {
        elements.paddles['id' + i] = this.add.rectangle(0, 0, 0, 0, 0xFFFFFF).setVisible(false);
    }
    elements.ball = this.add.circle(0, 0, 0, 0xFDF3E1).setVisible(false);
}

function update() {
    // pass
}

function initPaddlePosition(message) {
    if (message.id == 0) {
        // TODO eviter la pile de if avec une function
        elements.paddles.id0.setVisible(true)
        elements.paddles.id0.x = parseFloat(message.x)
        elements.paddles.id0.y = parseFloat(message.y)
        elements.paddles.id0.width = parseFloat(message.width)
        elements.paddles.id0.height = parseFloat(message.height)
        elements.paddles.id0.setFillStyle(message.color, 1);
    } else if (message.id == 1) {
        elements.paddles.id1.setVisible(true)
        elements.paddles.id1.x = parseFloat(message.x)
        elements.paddles.id1.y = parseFloat(message.y)
        elements.paddles.id1.width = parseFloat(message.width)
        elements.paddles.id1.height = parseFloat(message.height)
        elements.paddles.id1.setFillStyle(message.color, 1);
    }
}

function updatePaddlePosition(message) {
    if (message.id == 0) {
        elements.paddles.id0.y = parseFloat(message.y)
    } else if (message.id == 1) {
        elements.paddles.id1.y = parseFloat(message.y)
    }
}

function updateBallPosition(message) {
    elements.ball.setVisible(true)
    elements.ball.x = parseFloat(message.x)
    elements.ball.y = parseFloat(message.y)
    elements.ball.radius = parseFloat(message.radius)
    elements.ball.setFillStyle(message.color, 1);
}