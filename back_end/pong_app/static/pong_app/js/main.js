
const canvas = document.getElementById("pongCanvas");
const ctx = canvas.getContext("2d");
var game;
const startPaddle = canvas.height / 2 - 75

const PLAYER_WIDTH = canvas.width / 100
const PLAYER_HEIGHT = canvas.height / 5

function draw() {
    drawBackground()
    drawScore()
    drawBall()
    darwPaddles()
}

function drawScore() {
    ctx.fillStyle = 'white'
    ctx.font = "50px serif"
    ctx.fillText(game.computer.score, 50, 55)
    ctx.fillText(game.player.score, canvas.width - 75, 55)
}

function darwPaddles() {
    ctx.fillStyle = 'white';
    ctx.fillRect(5, game.player.y , PLAYER_WIDTH, PLAYER_HEIGHT);
    ctx.fillRect(canvas.width - PLAYER_WIDTH - 5, game.computer.y, PLAYER_WIDTH, PLAYER_HEIGHT);
}

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

function drawBall() {
    ctx.beginPath();
    ctx.fillStyle = 'white';
    ctx.arc(game.ball.x, game.ball.y, game.ball.r, 0, Math.PI * 2, false);
    ctx.fill();
}

function play() {
    draw();
    
    // computerMove();
    ballMove();
    requestAnimationFrame(play);
}

document.addEventListener('keydown', playerOneMove, false);
document.addEventListener('keydown', playerTwoMove, false);


function playerOneMove(e) {
    switch(e.key) {
        case 'w':
            if ((game.player.y) > 0)
            game.player.y -= 10
        break;
        case 's':
            if ((game.player.y) < canvas.height - PLAYER_HEIGHT)
                game.player.y += 10
            break;
    }
    e.preventDefault();
}

function playerTwoMove(e) {
    switch(e.key) {
        case 'ArrowUp':
            if ((game.computer.y) > 0)
            game.computer.y -= 10
        break;
        case 'ArrowDown':
            if ((game.computer.y) < canvas.height - PLAYER_HEIGHT)
                game.computer.y += 10
            break;
    }
    e.preventDefault();
}

function computerMove() {
        game.computer.y += game.ball.speed.y * 0.85;
}

function ballMove() {
    if (game.ball.y + game.ball.r > canvas.height || game.ball.y - game.ball.r < 0) {
        game.ball.speed.y *= -1;
    }

    if (game.ball.x + game.ball.r > canvas.width - PLAYER_WIDTH - 5) {
        collide(game.computer);
    } else if (game.ball.x - game.ball.r < PLAYER_WIDTH + 5) {
        collide(game.player);
    }

    game.ball.x += game.ball.speed.x;
    game.ball.y += game.ball.speed.y;
}

function collide(player) {
    // The player does not hit the ball
    if (game.ball.y < player.y || game.ball.y > player.y + PLAYER_HEIGHT) {
        // Set ball and players to the center
        game.ball.x = canvas.width / 2;
        game.ball.y = canvas.height / 2;
        game.computer.y = canvas.height / 2 - PLAYER_HEIGHT / 2;
        player.score++
        // Reset speed
        if (game.ball.speed.x > 0)
            game.ball.speed.x = 2;
        else 
            game.ball.speed.x = -2
    } else {
        // Increase speed and change direction
        game.ball.speed.x *= -1.2;
    }
}

document.addEventListener('DOMContentLoaded', function () {
    game = {
        player: {
            y: canvas.height / 2 - PLAYER_HEIGHT / 2,
            score: 0
        },
        computer: {
            y: canvas.height / 2 - PLAYER_HEIGHT / 2,
            score: 0
        },
        ball: {
            x: canvas.width / 2,
            y: canvas.height / 2,
            r: canvas.height / 50,
            speed: {
                x: -2,
                y: 2
            }
        }
    }

    draw();
    play()
})



// const socket = new WebSocket("ws://" + window.location.host + "/ws/some_path/");

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
