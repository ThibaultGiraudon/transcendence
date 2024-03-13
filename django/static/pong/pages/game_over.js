function renderGameOverPage(gameID) {
	fetchAPI('/api/isAuthenticated').then(data => {
		if (data.isAuthenticated) {
			fetchAPI('/api/get_game_over/' + gameID).then(data => {
				if (data.success) {	
					if (data.redirectGameMode) {
						finalGameMode = data.redirectGameMode
						router.navigate('/pong/wait_players/' + finalGameMode)
					}
					fetchAPI('/api/change_status/online').then(data => {});
					changeStatus(data.user_id, 'online')

					score = data.score
					position = data.position
					if (position == 1) {
						position = '1st'
					} else if (position == 2) {
						position = '2nd'
					} else if (position == 3) {
						position = '3rd'
					} else {
						position = position + 'th'
					}

					positionText = '<h3>You finished ' + position + '</h3>'
					if (score.length > 1) {
						positionText = ''
					}

					let html = `
						<h1>Game Over</h1>
						<h3>Score: ${score}</h3>
						${positionText}
					`
					document.getElementById('app').innerHTML = html
				} else {
					router.navigate('/')
				}
			})
		// If the user is not connected
		} else {
			router.navigate('/sign_in/')
		}
	})
}