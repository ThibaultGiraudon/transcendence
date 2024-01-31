function renderRankedPage() {
	fetchAPI('/api/isAuthenticated').then(data => {
		if (data.isAuthenticated) {
			let html = `
				<h1>Ranked game</h1>
			
				<button class="ranked-button" id="init_ranked_solo_game">
					1 VS 1 SOLO
				</button>
				<button class="ranked-button" id="init_death_game">
					DEATH GAME (4 players)
				</button>
				<button class="ranked-button" id="init_tournament_game">
					TOURNAMENT (4 players)
				</button>
			`;

			document.getElementById('app').innerHTML = html;

			document.querySelector('.ranked-button').addEventListener('click', async function(event) {
				const gameMode = event.target.id;
				console.log(gameMode);

				// Send data to the server
				const response = await fetch('/pong/wait_players/', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'X-CSRFToken': getCookie('csrftoken'),
					},
					body: JSON.stringify({gameMode})
				});
			});

		} else {
			router.navigate('/sign_in/');
		}
	});
}