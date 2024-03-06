
function renderStatsPage() {
	
	fetchAPI('/api/isAuthenticated').then(data => {
		if (data.isAuthenticated) {
			
			fetchAPI('/api/get_user').then(data => {
				if (data.user) {
					const user = data.user;
					const player = user.player;

					document.getElementById('app').innerHTML = `
						<h1>Statistics</h1>
					`;
				} else {
					router.navigate('/pong/');
				}
			});

		} else {
			router.navigate('/sign_in/');
		}
	});
}