function renderUsed42Page() {
	document.getElementById('app').innerHTML = `
		<div class="error-container">
			<p class="error-code">403</p>
			<p class="error-title">Failed to connect</p>
			<p class="error-infos">Your 42 email is already used, please log manually.</p>
		</div>
	`;
}