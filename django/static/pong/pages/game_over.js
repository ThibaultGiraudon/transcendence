function renderGameOverPage(gameID) {
	fetchAPI('/api/isAuthenticated').then(data => {
		if (data.isAuthenticated) {
			fetchAPI('/api/get_game_over/' + gameID).then(data => {
				if (data.success) {	
					playerID = data.player_id;
					score = data.score;
					position = data.position;
					if (position == 1) {
						position = '1st';
					} else if (position == 2) {
						position = '2nd';
					} else if (position == 3) {
						position = '3rd';
					} else {
						position = position + 'th';
					}

					let html = `
						<h1>Game Over (id = ${gameID})</h1>
						<p>Player ID: ${playerID}</p>
						<p>Score: ${score}</p>
						<p>You finished ${position}</p>
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