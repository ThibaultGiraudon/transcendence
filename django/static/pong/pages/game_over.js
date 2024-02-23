function renderGameOverPage(gameID) {
	fetchAPI('/api/isAuthenticated').then(data => {
		if (data.isAuthenticated) {
			fetchAPI('/api/get_game_over/' + gameID).then(data => {
				if (data.success) {	
					playerID = data.player_id;

					let html = `
						<h1>Game Over (id = ${gameID})</h1>
						<p>Winner: ${playerID}</p>
					`;
					document.getElementById('app').innerHTML = html;
				}
			});
		// If the user is not connected
		} else {
			router.navigate('/sign_in/');
		}
	})
}