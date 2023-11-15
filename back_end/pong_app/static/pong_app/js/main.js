const canvas = document.getElementById("pongCanvas");
const ctx = canvas.getContext("2d");
const startPaddle = canvas.height / 2 - 75

const ball = {
    x: canvas.width / 2,
    y: canvas.height / 2
};

const velocity = 3;
const startingAngle = 70;
const rad = 20;
let moveX = Math.cos(Math.PI / 180 * startingAngle) * velocity;
let moveY = Math.sin(Math.PI / 180 * startingAngle) * velocity;

const drawMe = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    if (ball.x > canvas.width - rad || ball.x < rad) 
        moveX = -moveX;
    if (ball.y > canvas.height - rad || ball.y < rad)
        moveY = -moveY; ball.x += moveX;
    ball.y += moveY; ctx.beginPath();
    ctx.fillStyle = 'green';
    ctx.arc(ball.x, ball.y, rad, 0, Math.PI * 2);
    ctx.fill();
    ctx.closePath();
}

// function darwPaddle() {
//     ctx.clearRect(0, 0, canvas.width, canvas.height);
//     ctx.fillStyle = "black";
//     ctx.fillRect(0, 0, canvas.width, canvas.height);
//     ctx.beginPath()
//     ctx.fillStyle = "purple"
//     ctx.fill()
//     ctx.fillRect(5, startPaddle + deltaY, 20, 150);
//     ctx.closePath();
// }

// document.addEventListener('keydown', move, false);

// var deltaY = 0
setInterval(drawMe, 10);
// darwPaddle()

// function move(e) {
//     switch(e.key) {
//         case 'w':
//             if ((startPaddle + deltaY - 10) > 0)
//             deltaY -= 10
//         break;
//         case 's':
//             if ((startPaddle + deltaY + 10) < canvas.height - 150)
//                 deltaY += 10
//             break;
//     }
//     e.preventDefault();

//     darwPaddle()
// }



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
