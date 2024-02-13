function renderToken42Page() {
	document.getElementById('app').innerHTML = `
		<div class="error-container">
			<p class="error-code">498</p>
			<p class="error-title">The token has expired</p>
			<p class="error-infos">Please contact the administrator.</p>
		</div>
	`;
}