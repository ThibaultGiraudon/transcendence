function renderPracticePage() {
	fetchAPI('/api/isAuthenticated').then(data => {
		if (data.isAuthenticated) {
			let html = `
				<h1>Practice game</h1>
			
				<button class="practice_button" id="init_local_game">
					LOCAL GAME
				</button>
				<button class="practice_button" id="init_ai_game">
					1 VS AI
				</button>
				<button class="practice_button" id="init_alcatraz_game">
					ALCATRAZ
				</button>
			`;

			document.getElementById('app').innerHTML = html;
		} else {
			router.navigate('/sign_in/');
		}
	});
}