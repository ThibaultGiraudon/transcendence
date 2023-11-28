export function getPaddleID(key) {
	if (key === 'ArrowUp' || key === 'ArrowDown') {
		return '1';
	} else if (key === 'w' || key === 's') {
		return '0';
	}
}

export function getPaddleDirection(key) {
	if (key === 'ArrowUp' || key === 'w') {
		return 'up';
	} else if (key === 'ArrowDown' || key === 's') {
		return 'down';
	}
}