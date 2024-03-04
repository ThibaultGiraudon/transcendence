function renderChooseModePage() {

	fetchAPI('/api/isAuthenticated').then(data => {

		// If the user is connected
		if (data.isAuthenticated) {
			document.getElementById('app').innerHTML = `
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
				if (!dataUser.isAuthenticated) {
					router.navigate('/sign_in/');
					return;
				}
				SignInProcess(dataUser.user.id);
			});
		// If the user is not connected
		} else {
			router.navigate('/sign_in/');
			return ;
		}
	})
}