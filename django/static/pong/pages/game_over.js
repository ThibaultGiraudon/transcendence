function renderGameOverPage(gameID) {
	fetchAPI('/api/isAuthenticated').then(data => {
		if (data.isAuthenticated) {
			fetchAPI('/api/get_game_over/' + gameID).then(data => {
				if (data.success) {	
					if (data.redirectGameMode) {
						finalGameMode = data.redirectGameMode;
						router.navigate('/pong/wait_players/' + finalGameMode);
					}
					fetchAPI('/api/change_status/online').then(data => {
						if (data.user_id) {
							changeStatus(data.user_id, 'online');
						}
					});
					if (data.message) {
						send_message(data.room_id, 0, data.message);
					}

					score = data.score;
					position = data.position;
					if (position == 1) {
						position = '1st';
						if (data.gameMode == 'init_death_game') {
							score = 10;
						}
					} else if (position == 2) {
						position = '2nd';
						if (data.gameMode == 'init_death_game') {
							console.log("2");
							score = 7;
						}
					} else if (position == 3) {
						position = '3rd';
						if (data.gameMode == 'init_death_game') {
							score = 3;
						}
					} else {
						position = position + 'th';
						if (data.gameMode == 'init_death_game') {
							score = 0;
						}
					}

					positionText = '<h3>You finished ' + position + '</h3>';
					if (typeof score !== 'undefined' && score.length > 1) {
						positionText = '';
					}

					let html = `
						<h1>Game Over</h1>
					`;
					if (typeof score !== 'undefined') {
						html += `
							<h3>Score: ${score}</h3>
							${positionText}
						`;
					}
					document.getElementById('app').innerHTML = html;
				} else {
					router.navigate('/');
				}
			});
		// If the user is not connected
		} else {
			router.navigate('/sign_in/');
		}
	});
}