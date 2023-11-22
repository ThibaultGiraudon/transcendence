// TODO voir p5 pour les canvas

// VARIABLES
let     websocketProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
let     websocketPort = window.location.protocol === 'https:' ? ':8001' : '';
const   socketUrl = websocketProtocol + '//' + window.location.host + websocketPort + '/ws/some_path/';
const   socket = new WebSocket(socketUrl);

const   PLAYER_WIDTH = 20
const   PLAYER_HEIGHT = 150
const   canvas = document.getElementById("pongCanvas");
const   context = canvas.getContext("2d");

const   keyState = {
    ArrowUp: false,
    ArrowDown: false,
    w: false,
    s: false,
};

const   paddlePosition = {
    left: 0,
    right: 0,
};

const   ballPosition = {
    x: 0,
    y: 0,
};

// FUNCTIONS
function drawBackground() {
    context.fillStyle = "black";
    context.fillRect(0, 0, canvas.width, canvas.height);
    
    context.strokeStyle = 'white';
    context.beginPath();
    context.moveTo(canvas.width / 2, 0);
    context.lineTo(canvas.width / 2, canvas.height);
    context.stroke();
    context.closePath();
}

function drawPaddles(paddlePosition) {
    drawBackground();

    console.log(ballPosition, " -> ", paddlePosition);
    context.fillStyle = 'white';
    context.fillRect(5, paddlePosition.left, PLAYER_WIDTH, PLAYER_HEIGHT);
    context.fillRect(canvas.width - PLAYER_WIDTH - 5, paddlePosition.right, PLAYER_WIDTH, PLAYER_HEIGHT);
}

function drawBall(ballPosition) {
    context.beginPath();
    context.fillStyle = 'white';
    context.arc(ballPosition.x, ballPosition.y, 16, 0, Math.PI * 2, false);
    // TODO 16 est le rayon
    context.fill();
}

// EVENTS
document.addEventListener('DOMContentLoaded', function() {
    function getPaddle(key) {
        if (key === 'ArrowUp' || key === 'ArrowDown') {
            return 'right';
        } else if (key === 'w' || key === 's') {
            return 'left';
        }
    }

    function getPaddleDirection(key) {
        if (key === 'ArrowUp' || key === 'w') {
            return 'up';
        } else if (key === 'ArrowDown' || key === 's') {
            return 'down';
        }
    }

    document.addEventListener('keydown', function(event) {
        if (!keyState[event.key] && keyState.hasOwnProperty(event.key)) {
            keyState[event.key] = true;
            const message = {
                type: 'paddle_move',
                key: 'keydown',
                direction: getPaddleDirection(event.key),
                paddle: getPaddle(event.key),
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
                direction: getPaddleDirection(event.key),
                paddle: getPaddle(event.key),
            };
            socket.send(JSON.stringify(message));
        }
    });

    socket.addEventListener('open', (event) => {
        const message = {
            type: 'init_game',
            canvas_width: canvas.width,
            canvas_height: canvas.height,
        };
        socket.send(JSON.stringify(message));
    });

    socket.addEventListener('message', (event) => {
        let message = JSON.parse(event.data);

        if (message.type === 'init_game') {
            paddlePosition.left = message.paddlePosition.left;
            paddlePosition.right = message.paddlePosition.right;
            ballPosition.x = message.ballPosition.x;
            ballPosition.y = message.ballPosition.y;

            // TODO a deplacer
            socket.send(JSON.stringify({
                type: 'ball_move',
            }));

            drawPaddles(paddlePosition)
            drawBall(ballPosition)
        }

        if (message.type === 'update_paddle_position') {
            if (message.paddle === 'left') {
                paddlePosition.left = parseFloat(message.position);
                drawPaddles(paddlePosition);
            } else if (message.paddle === 'right') {
                paddlePosition.right = parseFloat(message.position);
                drawPaddles(paddlePosition);
            }
        }

        if (message.type === 'update_ball_position') {
            ballPosition.x = parseFloat(message.position.x);
            ballPosition.y = parseFloat(message.position.y);
            drawBall(ballPosition);
        }
    });
});













// function draw() {
//     drawBackground()
//     drawScore()
//     drawBall()
//     drawPaddles()
// }

// function drawScore() {
//     context.fillStyle = 'white'
//     context.font = "50px serif"
//     context.fillText(game.computer.score, 50, 55)
//     context.fillText(game.player.score, canvas.width - 75, 55)
// }

// function drawPaddles() {
//     context.fillStyle = 'white';
//     context.fillRect(5, game.player.y , PLAYER_WIDTH, PLAYER_HEIGHT);
//     context.fillRect(canvas.width - PLAYER_WIDTH - 5, game.computer.y, PLAYER_WIDTH, PLAYER_HEIGHT);
// }

// function play() {
//     draw();
    
//     // computerMove();
//     ballMove();
//     requestAnimationFrame(play);
// }

// document.addEventListener('keydown', playerOneMove, false);
// document.addEventListener('keydown', playerTwoMove, false);


// function playerOneMove(e) {
//     switch(e.key) {
//         case 'w':
//             if ((game.player.y - 10) > 0)
//             game.player.y -= 10
//         break;
//         case 's':
//             if ((game.player.y + 10) < canvas.height - 150)
//                 game.player.y += 10
//             break;
//     }
//     e.preventDefault();
// }

// function playerTwoMove(e) {
//     switch(e.key) {
//         case 'ArrowUp':
//             if ((game.computer.y - 10) > 0)
//             game.computer.y -= 10
//         break;
//         case 'ArrowDown':
//             if ((game.computer.y + 10) < canvas.height - 150)
//                 game.computer.y += 10
//             break;
//     }
//     e.preventDefault();
// }

// function computerMove() {
//         game.computer.y += game.ball.speed.y * 0.85;
// }

// function ballMove() {
//     if (game.ball.y + game.ball.r > canvas.height || game.ball.y - game.ball.r < 0) {
//         game.ball.speed.y *= -1;
//     }

//     if (game.ball.x + game.ball.r > canvas.width - PLAYER_WIDTH - 5) {
//         collide(game.computer);
//     } else if (game.ball.x - game.ball.r < PLAYER_WIDTH + 5) {
//         collide(game.player);
//     }

//     game.ball.x += game.ball.speed.x;
//     game.ball.y += game.ball.speed.y;
// }

// function collide(player) {
//     // The player does not hit the ball
//     if (game.ball.y < player.y || game.ball.y > player.y + PLAYER_HEIGHT) {
//         // Set ball and players to the center
//         game.ball.x = canvas.width / 2;
//         game.ball.y = canvas.height / 2;
//         game.computer.y = canvas.height / 2 - PLAYER_HEIGHT / 2;
//         player.score++
//         // Reset speed
//         if (game.ball.speed.x > 0)
//             game.ball.speed.x = 2;
//         else 
//             game.ball.speed.x = -2
//     } else {
//         // Increase speed and change direction
//         game.ball.speed.x *= -1.2;
//     }
// }

// document.addEventListener('DOMContentLoaded', function () {
//     game = {
//         player: {
//             y: canvas.height / 2 - PLAYER_HEIGHT / 2,
//             score: 0
//         },
//         computer: {
//             y: canvas.height / 2 - PLAYER_HEIGHT / 2,
//             score: 0
//         },
//         ball: {
//             x: canvas.width / 2,
//             y: canvas.height / 2,
//             r: 10,
//             speed: {
//                 x: -2,
//                 y: 2
//             }
//         }
//     }

//     draw();
//     play()
// })