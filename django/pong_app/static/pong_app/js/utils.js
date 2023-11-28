export function getPaddleID(key) {
	if (key === 'ArrowUp' || key === 'ArrowDown') {
		return 'right';
	} else if (key === 'w' || key === 's') {
		return 'left';
	}
}

export function getPaddleDirection(key) {
	if (key === 'ArrowUp' || key === 'w') {
		return 'up';
	} else if (key === 'ArrowDown' || key === 's') {
		return 'down';
	}
}