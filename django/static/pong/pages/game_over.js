function renderGameOverPage(gameID) {
	fetchAPI('/api/isAuthenticated').then(data => {
		if (data.isAuthenticated) {
			// fetchAPI('/api/get_game_info').then(data => {
			// })
			document.getElementById('app').innerHTML = `
				<h1>Game Over</h1>
			`;




		// If the user is not connected
		} else {
			router.navigate('/sign_in/');
		}
	})
}