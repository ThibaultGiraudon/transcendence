function renderGamePage(gameMode) {
	fetchAPI('/api/isAuthenticated').then(data => {
		if (data.isAuthenticated) {
			fetchAPI('/api/get_game_info').then(data => {
				if (data.success) {
					gameID = data.game_id;
					playerID = data.player_id;
		
					let html = `
						<h1>Pong game</h1>
						
						<h2>Game Mode: ${gameMode}</h2>
						<p>${gameID}</p>
						
						<div class="score_bar" id="pong_game">
							<span class="player_score id0"></span>
							<span class="player_score id1"></span>
							<span class="player_score id2"></span>
							<span class="player_score id3"></span>
						</div>
						
						<canvas id="gameCanvas">
						
						</canvas>
					`;
		
					document.getElementById('app').innerHTML = html;
		
					gameProcess(false, gameMode, gameID, playerID)
				} else {
					router.navigate('/pong/');
				}
			});
		} else {
			router.navigate('/sign_in/');
		}
	});
}