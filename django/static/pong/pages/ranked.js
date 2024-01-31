function renderRankedPage() {
	fetchAPI('/api/isAuthenticated').then(data => {
		if (data.isAuthenticated) {
			let html = `
				<h1>Ranked game</h1>
			
				<a href="#" data-route="{% url 'wait_players' 'init_ranked_solo_game' %}" onclick="navigateTo(event, this.dataset.route)">
					1 VS 1 SOLO
				</a>
				<a href="#" data-route="{% url 'wait_players' 'init_death_game' %}" onclick="navigateTo(event, this.dataset.route)">
					DEATH GAME (4 players)
				</a>
				<a href="#" data-route="{% url 'wait_players' 'init_tournament_game' %}" onclick="navigateTo(event, this.dataset.route)">
					TOURNAMENT (4 players)
				</a>
			`;

			document.getElementById('app').innerHTML = html;
		} else {
			router.navigate('/sign_in/');
		}
	});
}