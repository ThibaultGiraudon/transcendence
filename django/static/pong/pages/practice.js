function renderPracticePage() {
	fetchAPI('/api/isAuthenticated').then(data => {
		if (data.isAuthenticated) {
			let html = `
				<h1>Practice game</h1>
			
				<a href="#" data-route="{% url 'game' 'init_local_game' %}" onclick="navigateTo(event, this.dataset.route)">
					LOCAL GAME
				</a>
				<a href="#" data-route="{% url 'game' 'init_ai_game' %}" onclick="navigateTo(event, this.dataset.route)">
					1 VS AI
				</a>
			`;

			document.getElementById('app').innerHTML = html;
		} else {
			router.navigate('/sign_in/');
		}
	});
}