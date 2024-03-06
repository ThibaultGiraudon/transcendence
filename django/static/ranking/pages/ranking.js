
function renderRankingPage(sortedBy) {
	
	fetchAPI('/api/isAuthenticated').then(data => {
		if (data.isAuthenticated) {
			fetchAPI('/api/get_ranking_points/' + sortedBy).then(data => {
				if (data.success) {
					fetchAPI('/api/get_user').then(ndata => {
						if (ndata.user) {
							const users = data.users;
							console.log(users);
							let i = 0;
							let html = `
								<h1>Ranking</h1>
								<table class="ranking-table">
									<tr>
										<th>Position</th>
										<th>User</th>
										<th>
											<button class="rank-sort" data-route="/ranking/solo">Solo Points</button>
										</th>
										<th>
											<button class="rank-sort" data-route="/ranking/death">Deathmatch Points</button>
										</th>
										<th>
											<button class="rank-sort" data-route="/ranking/tournament">Tournament Points</button>
										</th>
										<th>
											<button class="rank-sort" data-route="/ranking/total">Total Points</button>
										</th>
									</tr>
							`;

							for (const user of Object.values(users)) {
								if (user.username == ndata.user.username) {
									console.log(user.username);
									html += `
										<tr class="rank-user">
									`;
								}
								else {
									html += `
										<tr>
									`;
								}
								html += `
										<td class="rank-position">${++i}</td>
										<td>
											<button class="rank-user-info" data-route="/profile/${user.username}">
												<img class="rank-image" src="${user.photo_url}" alt="photo">
												${user.username}
											</button>
										</td>
										<td>${user.player.soloPoints[user.player.soloPoints.length - 1]}</td>
										<td>${user.player.deathPoints[user.player.deathPoints.length - 1]}</td>
										<td>${user.player.tournamentPoints[user.player.tournamentPoints.length - 1]}</td>
										<td class="rank-total">${user.player.totalPoints[user.player.totalPoints.length - 1]}</td>
									</tr>
								`;
							}

							html += `
								</table>
							`;

							document.getElementById('app').innerHTML = html;
						}			
					});
				} else {
					router.navigate('/pong/');
				}
			});
		} else {
			router.navigate('/sign_in/');
		}
	});
}