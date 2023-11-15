const canvas = document.getElementById("pongCanvas");
const context = canvas.getContext("2d");

console.log("OK");

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
