function renderChooseModePage() {

	fetchAPI('/api/is_authenticated').then(data => {

		// If the user is connected
		if (data.isAuthenticated) {
			document.getElementById('app').innerHTML = `
				<h1 id="set-status-online">Pong game</h1>
				<a href="#" data-route="{% url 'ranked' %}" onclick="navigateTo(event, this.dataset.route)" class="choose-btn">
					Ranked Mode
				</a>
				<a href="#" data-route="{% url 'practice' %}" onclick="navigateTo(event, this.dataset.route)" class="choose-btn">
					Practice Mode
				</a>
			`;
		
		// If the user is not connected
		} else {
			router.navigate('/sign_in/');
		}
	})
}