function render500Page() {
	document.getElementById('app').innerHTML = `
		<div class="error-container">
			<p class="error-code">500</p>
			<p class="error-title">Internal Server Error</p>
			<p class="error-infos">Please try again later.</p>
		</div>
	`;
}