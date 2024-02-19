function renderPracticePage() {
	fetchAPI('/api/isAuthenticated').then(data => {
		if (data.isAuthenticated) {
			let html = `
				<h1>Practice game</h1>
			
				<button class="practice-button" id="init_local_game">
					LOCAL GAME
				</button>
				<button class="practice-button" id="init_ai_game">
					1 VS AI
				</button>
				<button class="practice-button" id="init_alcatraz_game">
					ALCATRAZ
				</button>
			`;

			document.getElementById('app').innerHTML = html;

			document.querySelectorAll('.practice-button').forEach(button => {
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