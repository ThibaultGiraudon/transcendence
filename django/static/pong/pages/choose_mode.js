function renderChooseModePage() {

	fetchAPI('/api/isAuthenticated').then(data => {

		// If the user is connected
		if (data.isAuthenticated) {
			document.getElementById('app').innerHTML = `
				<h1 id="set-status-online">Pong game</h1>
				<button class="choose-btn" data-route="/pong/ranked/">
					Ranked Mode
				</button>
				<button class="choose-btn" data-route="/pong/practice/">
					Practice Mode
				</button>
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