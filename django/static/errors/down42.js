function renderDown42Page() {
	document.getElementById('app').innerHTML = `
		<div class="error-container">
			<p class="error-code">401</p>
			<p class="error-title">The 42 API is down</p>
			<p class="error-infos">Please contact the administrator.</p>
		</div>
	`;
}