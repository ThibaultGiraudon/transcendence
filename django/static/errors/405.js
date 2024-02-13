function render405Page() {
	document.getElementById('app').innerHTML = `
		<div class="error-container">
			<p class="error-code">405</p>
			<p class="error-title">Method Not Allowed</p>
			<p class="error-infos">Please check the URL and try again.</p>
		</div>
	`;
}