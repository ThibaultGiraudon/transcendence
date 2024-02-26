function renderGameOverPage(gameID) {
	fetchAPI('/api/isAuthenticated').then(data => {
		if (data.isAuthenticated) {
			fetchAPI('/api/get_game_over/' + gameID).then(data => {
				if (data.success) {	
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

					positionText = '<p>You finished ' + position + '</p>';
					if (score.length > 1) {
						positionText = '';
					}

					let html = `
						<h1>Game Over (id = ${gameID})</h1>
						<p>Score: ${score}</p>
						${positionText}
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