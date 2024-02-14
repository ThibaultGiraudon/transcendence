function initPaddlePosition(paddleID, position) {
	elements.paddles[paddleID] = new Paddle(paddleID);
	elements.paddles[paddleID].draw(position);
}

function updatePaddlePosition(paddleID, position) {
	if (!elements.paddles[paddleID]) {
		return
	}
	elements.paddles[paddleID].clear();
	elements.paddles[paddleID].draw(position);
}

function updateScore(message) {
    const backgroundColors = ['#E21E59', '#1598E9', '#2FD661', '#F19705'];
    const scoreSpans = document.querySelectorAll('.player_score');

	if (message.nbPaddles == 1) {
		scoreSpans[message.id].style.width = '100%';
	} else if (message.nbPaddles == 2) {
        scoreSpans[message.id].style.width = '50%';
    } else if (message.nbPaddles == 4) {
        scoreSpans[message.id].style.width = '25%';
    }

	scoreSpans[message.id].textContent = message.score;
    scoreSpans[message.id].style.backgroundColor = backgroundColors[message.id];
	if (message.score >= 10) {
		if (message.nbPaddles == 2) {
			paddleID = message.id ^ 1;
		} else {
			paddleID = message.id;
		}
		scoreSpans[paddleID].style.backgroundColor = '#212121';
		scoreSpans[paddleID].style.color = '#DADADA';
		if (!elements.paddles[paddleID]) {
			return
		}
		elements.paddles[paddleID].clear();
		elements.paddles[paddleID].draw();
	}
}

function updateBallPosition(x, y, color, radius) {
	if (elements.ball) {
		elements.ball.clear();
	}
	elements.ball = new Ball(x, y, color, radius);
	elements.ball.draw(x, y, color, radius);
}

function gameOver(message) {
	router.navigate('/gameOver/' + message.gameMode);
	
	// const gameOverDiv = document.getElementById('gameOver');
	// gameOverDiv.style.display = 'block';
}