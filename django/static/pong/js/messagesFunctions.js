function initPaddlePosition(paddleID, position) {
	elements.paddles[paddleID] = new Paddle(paddleID);
	elements.paddles[paddleID].draw(position);
}

function updatePaddlePosition(paddleID, position) {
	elements.paddles[paddleID].clear();
	elements.paddles[paddleID].draw(position);
}

function updateScore(message) {
    const backgroundColors = ['#E21E59', '#1598E9', '#2FD661', '#F19705'];
    const scoreSpans = document.querySelectorAll('.player_score');

    if (message.nbPaddles == 2) {
        scoreSpans[message.id].style.width = '50%';
    } else if (message.nbPaddles == 4) {
        scoreSpans[message.id].style.width = '25%';
    }
    scoreSpans[message.id].textContent = message.score;
    scoreSpans[message.id].style.backgroundColor = backgroundColors[message.id];
	if (message.score >= 10) {
		scoreSpans[message.id].style.backgroundColor = '#212121';
		scoreSpans[message.id].style.color = '#DADADA';
		elements.paddles[message.id].clear();
		elements.paddles[message.id].draw();
	}
}

function updateBallPosition(x, y, color, radius) {
	if (elements.ball) {
		elements.ball.clear();
	}
	elements.ball = new Ball(x, y, color, radius);
	elements.ball.draw(x, y, color, radius);
}