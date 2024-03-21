function renderPracticePage() {
	fetchAPI('/api/isAuthenticated').then(data => {
		if (data.isAuthenticated) {

			fetchAPI('/api/get_user').then(dataUser => {
				if (dataUser.user.player.currentGameID) {
					router.navigate('/pong/');
					return ;
				}

				let html = `
					<h1>Practice game</h1>
					<h3>Choose a game mode</h3>
				
					<div class="choose-buttons">
						<button class="practice-btn" id="init_local_game">
							<img class="choose-img" src="/static/pong/img/local.png" class="choose-img">
							<p class="choose-btn-title">Local game</p>
							<p class="choose-btn-text">
								1v1 game between you and a friend on the same computer.
							</p>
						</button>

						<button class="practice-btn" id="init_ai_game">
							<img class="choose-img" src="/static/pong/img/ai.png" class="choose-img">
							<p class="choose-btn-title">1 vs AI</p>
							<p class="choose-btn-text">
								1v1 game between you and an opponent controlled by artificial intelligence.
							</p>
						</button>

						<button class="practice-btn" id="init_wall_game">
							<img class="choose-img" src="/static/pong/img/wall.png" class="choose-img">
							<p class="choose-btn-title">Wall game</p>
							<p class="choose-btn-text">
								Play alone against a wall.
							</p>
						</button>
					</div>

					<button class="choose-back-btn" data-route="/pong/">↩ Back to menu</button>
				`;

				document.getElementById('app').innerHTML = html;

				document.querySelectorAll('.practice-btn').forEach(button => {
					button.addEventListener('click', async function(event) {
						const gameMode = event.target.id;

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

							if (responseData.success) {
								router.navigate(responseData.redirect + responseData.gameMode);
								return ;
							}
						}
					});
				});
			});
			
		} else {
			router.navigate('/sign_in/');
			return ;
		}
	});
}