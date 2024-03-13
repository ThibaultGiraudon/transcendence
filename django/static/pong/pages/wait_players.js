function renderWaitPlayers(gameMode) {
	fetchAPI('/api/isAuthenticated').then(data => {
		if (data.isAuthenticated) {
			fetchGamePage(gameMode)
			fetchAPI('/api/get_game_info').then(data => {
				if (data.success) {
					gameID = data.game_id;
					playerID = data.player_id;
					changeStatus(data.user_id, 'waiting for game')

					let html = `
						<div class="all-screen">
							<div class="waiting-game-infos">
								<h2 class="waiting-game-title"></h2>
								<img class="waiting-game-gif" src="/static/main/img/loading.gif" alt="waiting">
							</div>
						</div>
					`;
					document.getElementById('app').innerHTML = html;

					// Dynamic title
					let dots = 0;
					setInterval(() => {
						if (dots == 4) {
							dots = 0;
						}
						if (document.querySelector('.waiting-game-title') != null) {
							document.querySelector('.waiting-game-title').innerHTML = 'Waiting for players' + '.'.repeat(dots);
						} else {
							clearInterval();
						}
						dots++;
					}, 500);
		
					gameProcess(true, gameMode, gameID, playerID, null)
				} else {
					router.navigate('/pong/');
				}
			});
		} else {
			router.navigate('/sign_in/');
		}
	});
}

async function fetchGamePage(gameMode) {
	// Send data to the server
	const response = await fetch('/pong/wait_players/' + gameMode, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': getCookie('csrftoken'),
		},
		body: JSON.stringify({gameMode})
	});

	if (response.headers.get('content-type').includes('application/json')) {
		const responseData = await response.json();

		if (responseData.success && responseData.redirect == '/pong/game/') {
			router.navigate(responseData.redirect + responseData.gameMode);
		}
	}
}