function renderChooseModePage() {

	fetchAPI('/api/isAuthenticated').then(data => {

		// If the user is not connected
		if (!data.isAuthenticated) {
			router.navigate('/sign_in/');
			return ;
		}

		// Modes page
		const modesPage = `
			<h1>Pong game</h1>
			<h3 id="set-status-online">Choose a mode</h3>
			
			<div class="choose-buttons">
				<button class="choose-btn" data-route="/pong/practice/">
					<img class="choose-img" src="/static/pong/img/practice.png" class="choose-img">
					<p class="choose-btn-title">Practice Mode</p>
					<p class="choose-btn-text">
						These games do not count for statistics. Several training game modes are offered.
					</p>
				</button>
				
				<button class="choose-btn" data-route="/pong/ranked/">
					<img class="choose-img" src="/static/pong/img/ranked.png" class="choose-img">
					<p class="choose-btn-title">Ranked Mode</p>
					<p class="choose-btn-text">
						These games count for statistics. You will face random opponents from all over the world.
					</p>
				</button>
			</div>
		`;
		
		fetchAPI('/api/get_user').then(dataUser => {
			// If the user is not connected
			if (!dataUser.isAuthenticated) {
				router.navigate('/sign_in/');
				return;
			}

			if (!dataUser.user.player.currentGameID) {
				document.getElementById('app').innerHTML = modesPage;
			
			} else {
				let html = `
					<h1>Pong game</h1>
					<h3 id="set-status-online">You are already in a game</h3>
					
					<div class="choose-buttons">
						<button class="choose-btn" data-route="/pong/wait_players/${dataUser.user.player.gameMode}">
							<img class="choose-img" src="/static/pong/img/continue.png" class="choose-img">
							<p class="choose-btn-title">Continue</p>
							<p class="choose-btn-text">
								Click here to continue.
							</p>
						</button>
					`;
				
				console.log(dataUser.user.player.gameMode);
				if ((dataUser.user.player.gameMode in ['init_wall_game', 'init_ai_game', 'init_local_game']) || dataUser.user.player.isReady == false) {
					html += `
							<button class="choose-btn" id="quit-game">
								<img class="choose-img" src="/static/pong/img/quit.png" class="choose-img">
								<p class="choose-btn-title">Quit</p>
								<p class="choose-btn-text">
									Click here to quit.
								</p>
							</button>
						</div>
					`;
				}
				else {
					html += `</div>`;
				}
				document.getElementById('app').innerHTML = html;
			}
			
			if (document.getElementById('quit-game')) {
				document.getElementById('quit-game').addEventListener('click', () => {
					fetchAPI('/api/quit_game').then(data => {
						if (data.success) {
							if (data.message == 'send-quit') {
								send_message(data.room_id, 0, 'Invitation canceled');
							}
							pongSocket.socket.close();
							pongSocket = null;
							router.navigate('/pong/');
						}
					});
				});
			}
			SignInProcess(dataUser.user.id);
		});
	})
}