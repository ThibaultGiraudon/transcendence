class Field {
	constructor(size) {
		this.x = sizes.field;
		this.y = sizes.field;
		this.width = size - sizes.field * 2;
		this.height = size - sizes.field * 2;
	}

	draw(context) {
		context.fillStyle = "#404040";
		context.fillRect(this.x, this.y, this.width, this.height);
	}
}

class Ball {
	constructor(x, y, color, radius) {
		this.x = x;
		this.y = y;
		this.color = color;
		this.radius = radius;
		const canvas = document.getElementById('ballLayer');
		if (!canvas) {
			return;
		}
		canvas.width = sizes.canvas;
		canvas.height = sizes.canvas;
		this.context = canvas.getContext('2d');
	}

	draw(x, y, color, radius) {
		this.x = x;
		this.y = y;
		this.color = color;
		this.radius = radius;
		if (!this.context) {
			return;
		}
		this.context.fillStyle = this.color;
		this.context.beginPath();
		this.context.arc(this.x, this.y, this.radius, 0, 2 * Math.PI);
		this.context.fill();
	}

	clear() {
		if (this.context) {
			this.context.clearRect(0, 0, sizes.canvas, sizes.canvas)
		}
	}
}

class Paddle {
	constructor(paddleID) {
		this.id = paddleID;
		this.width = sizes.paddleThickness;
		this.height = sizes.paddleSize;
		if (paddleID >= 2) {
			this.width = sizes.paddleSize;
			this.height = sizes.paddleThickness;
		}
		const canvas = document.getElementById('paddle' + (parseInt(paddleID) + 1) + 'Layer');
		if (!canvas) {
			return;
		}
		canvas.width = sizes.canvas;
		canvas.height = sizes.canvas;		
		this.context = canvas.getContext('2d');
	}

	draw(position) {
		const bottomLimit = sizes.offset;
		const topLimit = sizes.canvas - sizes.field;

		const paddleXpos = [bottomLimit, topLimit, position, position];
		const paddleYpos = [position, position, bottomLimit, topLimit];
		const paddleColors = ['#E21E59', '#1598E9', '#2FD661', '#F19705'];

		this.x = paddleXpos[this.id];
		this.y = paddleYpos[this.id];
		this.color = paddleColors[this.id];
		if (!this.context) {
			return;
		}
		this.context.fillStyle = this.color;
		this.context.fillRect(this.x, this.y, this.width, this.height);
	}
	
	clear() {
		if (this.context) {
			this.context.clearRect(0, 0, sizes.canvas, sizes.canvas)
		}
	}
}