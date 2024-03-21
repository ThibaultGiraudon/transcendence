function renderWaitPlayers(gameMode) {
	fetchAPI('/api/isAuthenticated').then(data => {
		if (data.isAuthenticated) {
			fetchGamePage(gameMode)
			fetchAPI('/api/get_game_info').then(data => {
				if (data.success) {
					fetchAPI('/api/change_status/waiting-game').then(data => {
						if (data.user_id) {
							changeStatus(data.user_id, 'waiting-game');
						}
					});
					gameID = data.game_id;
					playerID = data.player_id;

					let html = `
						<div class="all-screen">
							<div class="waiting-game-infos">
								<h2 class="waiting-game-title"></h2>
								<img class="waiting-game-gif" src="/static/main/img/loading.gif" alt="waiting">
							</div>
							<button class="choose-back-btn cancel-game-button" id="quit">↩ Quit game</button>
						</div>
					`;
					document.getElementById('app').innerHTML = html;

					quitButton = document.getElementById('quit')
					if (quitButton) {
						document.getElementById('quit').addEventListener('click', () => {
							fetchAPI('/api/quit_game').then(data => {
								if (data.success) {
									if (data.message == 'send-quit') {
										send_message(data.room_id, 0, 'Invitation canceled')
									}
									pongSocket.socket.close();
									pongSocket = null;
									router.navigate('/pong/');
								}
							});
						});
					}

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
		
					gameProcess(true, gameMode, gameID, playerID)
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