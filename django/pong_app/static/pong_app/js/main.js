let     websocketProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
let     websocketPort = window.location.protocol === 'https:' ? ':8001' : '';
const   socketUrl = websocketProtocol + '//' + window.location.host + websocketPort + '/ws/some_path/';
const   socket = new WebSocket(socketUrl);

document.addEventListener('DOMContentLoaded', function() {
    const keyState = {
        ArrowUp: false,
        ArrowDown: false,
        w: false,
        s: false,
    };

    document.addEventListener('keydown', function(event) {
        if (!keyState[event.key] && (event.key === 'ArrowUp' || event.key === 'ArrowDown' || event.key === 'w' || event.key === 's')) {
            keyState[event.key] = true;
            const message = {
                type: 'paddle_move',
                key: 'keydown',
                direction: getPaddleDirection(event.key),
                paddle: getPaddle(event.key),
                // TODO get paddle position qui renvoie en fonction de event.key
            };
            socket.send(JSON.stringify(message));
        }
    });

    document.addEventListener('keyup', function(event) {
        if (event.key === 'ArrowUp' || event.key === 'ArrowDown' || event.key === 'w' || event.key === 's') {
            keyState[event.key] = false;
            const message = {
                type: 'paddle_move',
                key: 'keyup',
                direction: getPaddleDirection(event.key),
                paddle: getPaddle(event.key),
                // TODO get paddle position qui renvoie en fonction de event.key
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
        // console.log('Message reçu:', message);

        let message = JSON.parse(event.data);
        if (message.type === 'update_paddle_position') {

            console.log('update_paddle_position');
            if (message.paddle === 'left') {
                const newPosition = parseFloat(message.position);
                drawLeftPaddles(newPosition);
            } else if (message.paddle === 'right') {
                const newPosition = parseFloat(message.position);
                drawRightPaddle(newPosition);
            }
        }
    });
});

function getPaddle(key) {
    if (key === 'ArrowUp' || key === 'ArrowDown') {
        return 'left';
    } else if (key === 'w' || key === 's') {
        return 'right';
    }
}

function getPaddleDirection(key) {
    if (key === 'ArrowUp' || key === 'w') {
        return 'up';
    } else if (key === 'ArrowDown' || key === 's') {
        return 'down';
    }
}

const PLAYER_WIDTH = 20
const PLAYER_HEIGHT = 150
const canvas = document.getElementById("pongCanvas");
const ctx = canvas.getContext("2d");
var game;

function drawLeftPaddles(position) {
    drawBackground();
    ctx.fillStyle = 'white';
    ctx.fillRect(5, position, PLAYER_WIDTH, PLAYER_HEIGHT);
}

function drawRightPaddle(position) {
    drawBackground();
    ctx.fillStyle = 'white';
    ctx.fillRect(canvas.width - PLAYER_WIDTH - 5, position, PLAYER_WIDTH, PLAYER_HEIGHT);
}

// TODO voir p5 pour les canvas



const startPaddle = canvas.height / 2 - 75

function drawBackground() {
    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    ctx.strokeStyle = 'white';
    ctx.beginPath();
    ctx.moveTo(canvas.width / 2, 0);
    ctx.lineTo(canvas.width / 2, canvas.height);
    ctx.stroke();
    ctx.closePath();
}




// Exécuté lorsque la connexion WebSocket est fermée
socket.addEventListener('close', (event) => {
    console.log('WebSocket fermé !');
});

// Exécuté en cas d'erreur WebSocket
socket.addEventListener('error', (event) => {
    console.error('Erreur WebSocket:', event);
});



// function draw() {
//     drawBackground()
//     drawScore()
//     drawBall()
//     drawPaddles()
// }

// function drawScore() {
//     ctx.fillStyle = 'white'
//     ctx.font = "50px serif"
//     ctx.fillText(game.computer.score, 50, 55)
//     ctx.fillText(game.player.score, canvas.width - 75, 55)
// }

// function drawPaddles() {
//     ctx.fillStyle = 'white';
//     ctx.fillRect(5, game.player.y , PLAYER_WIDTH, PLAYER_HEIGHT);
//     ctx.fillRect(canvas.width - PLAYER_WIDTH - 5, game.computer.y, PLAYER_WIDTH, PLAYER_HEIGHT);
// }



// function drawBall() {
//     ctx.beginPath();
//     ctx.fillStyle = 'white';
//     ctx.arc(game.ball.x, game.ball.y, game.ball.r, 0, Math.PI * 2, false);
//     ctx.fill();
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



// const socket = new WebSocket("ws://" + window.location.host + "/ws/some_path/");
// const socket = new WebSocket("ws://" + window.location.host + ":8000/ws/some_path/");

// document.addEventListener("keydown", handleKeyDown);

// function handleKeyDown(event) {
//     // Envoyer un message WebSocket lorsque la touche flèche vers le haut est pressée
//     if (event.key === "ArrowUp") {
// 		console.log("ArrowUp pressed");
//         const message = {
//             type: "move_paddle",
//             direction: "up"
//         };
//         socket.send(JSON.stringify(message));
//     }
// }

// // Écouter les messages WebSocket
// socket.addEventListener("message", (event) => {
//     const message = JSON.parse(event.data);
//     if (message.type === "update_paddle") {
//         // Mettre à jour la position du paddle en fonction du message du serveur
//         updatePaddle(message.position);
//     }
// });

// function updatePaddle(newPosition) {
//     // Mettez en œuvre la logique pour mettre à jour la position du paddle sur le canvas
//     // en fonction de la nouvelle position reçue du serveur
//     // ...

//     console.log("New Paddle Position:", newPosition);
//     // Exemple basique : déplacez simplement le paddle verticalement
//     context.clearRect(0, 0, canvas.width, canvas.height);
//     context.fillRect(50, newPosition, 10, 50);
// }

// let websocketProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
// let websocketPort = window.location.protocol === 'https:' ? ':8001' : '';

// const testSocket = new WebSocket(`${websocketProtocol}//${window.location.host}${websocketPort}/ws/some_path/`);

// testSocket.addEventListener("open", (event) => {
//     console.log("WebSocket ouvert !");
//     testSocket.send(JSON.stringify({ message: "Hello, WebSocket!" }));
// });

// testSocket.addEventListener("message", (event) => {
//     const message = JSON.parse(event.data);
//     console.log("Message reçu:", message);
// });