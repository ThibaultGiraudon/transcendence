function render403Page() {
	document.getElementById('app').innerHTML = `
		<div class="error-container">
			<p class="error-code">403</p>
			<p class="error-title">Forbidden</p>
			<p class="error-infos">Access denied</p>
		</div>
	`;
}