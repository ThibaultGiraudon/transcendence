function render404Page() {
	// 1 chance to get a funny error message
	const random = Math.random();
	let errorInfos = "Please check the URL and try again.";
	if (random < 0.1) {
		errorInfos = "You are lost in the woods. You should have listened to your mother and stayed on the path.";
	}

	document.getElementById('app').innerHTML = `
		<div class="error-container">
			<p class="error-code">404</p>
			<p class="error-title">Page not found</p>
			<p class="error-infos">${errorInfos}</p>
		</div>
	`;
}