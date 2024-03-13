function renderRankedPage() {
	fetchAPI('/api/isAuthenticated').then(data => {
		if (data.isAuthenticated) {
			let html = `
				<h1>Ranked game</h1>
				<h3>Choose a game mode</h3>
			
				<div class="choose-buttons">
					<button class="ranked-btn" id="init_ranked_solo_game">
						<img class="choose-img" src="/static/pong/img/global.png" class="choose-img">
						<p class="choose-btn-title">1 vs 1</p>
						<p class="choose-btn-text">
							Solo play against a random opponent from around the world.
						</p>
					</button>

					<button class="ranked-btn" id="init_death_game">
						<img class="choose-img" src="/static/pong/img/death.png" class="choose-img">
						<p class="choose-btn-title">Deathmatch Game</p>
						<p class="choose-btn-text">
							4 players play on the same board.
							The last one standing wins the game.
						</p>
					</button>

					<button class="ranked-btn" id="init_tournament_game">
						<img class="choose-img" src="/static/pong/img/tournament.png" class="choose-img">
						<p class="choose-btn-title">Tournament</p>
						<p class="choose-btn-text">
							4 players play on 2 boards in 1v1.
							The 2 winners play against each other.
							The last one standing wins the tournament.
						</p>
					</button>
				</div>

				<button class="choose-back-btn" data-route="/pong/">↩ Back to menu</button>
			`;

			document.getElementById('app').innerHTML = html;

			document.querySelectorAll('.ranked-btn').forEach(button => {
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
							if (gameMode == 'init_tournament_game') {
								fetchAPI('/api/join_tournament').then(data => {
									if (data.room_id) {
										send_tournament_message(data.room_id);
										return;
									}
								});
							}
							router.navigate(responseData.redirect + responseData.gameMode);
							return ;
						}
					}
				});
			});
		} else {
			router.navigate('/sign_in/');
			return ;
		}
	});
}

function send_tournament_message(room_id) {
	let websocketProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
	let websocketPort = window.location.protocol === 'https:' ? ':8443' : ':8000';
	const socketUrl = websocketProtocol + '//' + window.location.hostname + websocketPort + '/ws/chat/' + room_id + "/";

	let tmpSocket

	tmpSocket = {
		socket: new WebSocket(socketUrl),
		url: socketUrl,
		shouldClose: false
	};

	tmpSocket.socket.onopen = function(event) {
		tmpSocket.socket.send(JSON.stringify({
			'message': "Tournament game is starting! Players get ready!",
			'sender': 0,
			'username': 'System Info',
		}));
	};
}