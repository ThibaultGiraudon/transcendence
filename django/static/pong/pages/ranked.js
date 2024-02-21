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

			document.querySelectorAll('.ranked-button').forEach(button => {
				button.addEventListener('click', async function(event) {
					const gameMode = event.target.id;
					console.log(gameMode);

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
									console.log(data);
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

	console.log(tmpSocket);

	tmpSocket.socket.onopen = function(event) {
		console.log('Sending message');
		tmpSocket.socket.send(JSON.stringify({
			'message': "Tournament game is starting! Players get ready!",
			'sender': 0,
			'username': 'System Info',
		}));
	};
}