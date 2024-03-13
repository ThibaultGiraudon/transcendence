function renderAuth42Page() {
	document.getElementById('app').innerHTML = `
		<div class="error-container">
			<p class="error-code">403</p>
			<p class="error-title">Access refused.</p>
			<p class="error-infos">You should authorize the website to use your account.</p>
		</div>
	`;
}