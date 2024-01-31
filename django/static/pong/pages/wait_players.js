function renderWaitPlayers(gameMode) {
	fetchAPI('/api/isAuthenticated').then(data => {
		if (data.isAuthenticated) {
			let html = `
				<h1>Wait for players ${gameMode}</h1>

				<div class="score_bar" id="wait_player"></div>
				<div id="pong_game"></div>

				<p>{{ gameID }}</p>
			`;

			document.getElementById('app').innerHTML = html;





		} else {
			router.navigate('/sign_in/');
		}
	});
}