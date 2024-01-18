function gameProcess() {
	console.log("OK");

	const gameCanvas = document.getElementById('gameCanvas');
    const gameContext = gameCanvas.getContext('2d');
	const canvasSize = 600;

    gameCanvas.width = canvasSize;
    gameCanvas.height = canvasSize;
	console.log(gameCanvas.width);

    gameContext.fillStyle = "#212121";
    gameContext.fillRect(0, 0, gameCanvas.width, gameCanvas.height);


}