function getPaddleID(key) {
	if (key === 'o' || key === 'l') {
		return '1';
	} else if (key === 'w' || key === 's') {
		return '0';
	}
}

function getPaddleDirection(key) {
	if (key === 'o' || key === 'w') {
		return 'up';
	} else if (key === 'l' || key === 's') {
		return 'down';
	}
}