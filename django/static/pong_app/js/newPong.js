function createGameField(gameContext, size) {
	fieldSize = 30;
    const gameField = {
        x: fieldSize,
        y: fieldSize,
        width: size - fieldSize * 2,
        height: size - fieldSize * 2
    };
    gameContext.fillStyle = "#404040";
    gameContext.fillRect(gameField.x, gameField.y, gameField.width, gameField.height);
}

function createGameCanvas() {
	const canvasSize = 800;

	const gameCanvas = document.getElementById('gameCanvas');
    gameCanvas.width = canvasSize;
    gameCanvas.height = canvasSize;

    const gameContext = gameCanvas.getContext('2d');
    gameContext.fillStyle = "#212121";
    gameContext.fillRect(0, 0, gameCanvas.width, gameCanvas.height);

	createGameField(gameContext, canvasSize);

	return (gameCanvas, gameContext)	
}

function gameProcess() {
	gameCanvas, gameContext = createGameCanvas();
}