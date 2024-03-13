
function renderRankingPage(sortedBy) {
	
	fetchAPI('/api/isAuthenticated').then(data => {
		
		if (data.isAuthenticated) {
			
			// Check if the argument is valid
			const validValues = ['solo', 'death', 'tournament', 'total', 'game', 'average', 'solo_inversed', 'death_inversed', 'tournament_inversed', 'total_inversed', 'game_inversed', 'average_inversed'];
			if (!validValues.includes(sortedBy)) {
				router.navigate('/ranking/total');
				return;
			}

			fetchAPI('/api/get_ranking_points/' + sortedBy).then(data => {
				
				if (data.success) {
					fetchAPI('/api/get_user').then(ndata => {
						
						if (ndata.user) {

							const users = data.users;
							split = sortedBy.includes('_');

							let html = `
								<div class="ranking-title">
									<h1>Ranking</h1>
									<button class="ranking-title-info">
										<img class="ranking-title-info-img" src="/static/chat/img/info.png" alt="Info">
									</button>
								</div>

								<table class="ranking-table" id="ranking-table">
									<tr>
										<th>
											<button class="rank-sort" data-route="/ranking/${sortedBy.includes('_') == false ? sortedBy + "_inversed" : sortedBy.split('_')[0]}">Position  ${sortedBy.includes('_') ? "▲": "▼"}</button>
										</th>
										<th><input class="ranking-search" id="userSearch" type="text" placeholder="User"></th>
										<th class="${sortedBy.split('_')[0] == "solo" ? "selected-row" : "ranking-row"}">
											<button class="rank-sort" data-route="/ranking/solo">Solo Points</button>
										</th>
										<th class="${sortedBy.split('_')[0] == "death" ? "selected-row" : "ranking-row"}">
											<button class="rank-sort" data-route="/ranking/death">Deathmatch Points</button>
										</th>
										<th class="${sortedBy.split('_')[0] == "tournament" ? "selected-row" : "ranking-row"}">
											<button class="rank-sort" data-route="/ranking/tournament">Tournament Points</button>
										</th>
										<th class="${sortedBy.split('_')[0] == "total" ? "selected-row" : "ranking-row"}">
											<button class="rank-sort" data-route="/ranking/total">Total Points</button>
										</th>
										<th class="${sortedBy.split('_')[0] == "game" ? "selected-row" : "ranking-row"}">
											<button class="rank-sort" data-route="/ranking/game">Games played</button>
										</th>
										<th class="${sortedBy.split('_')[0] == "average" ? "selected-row" : "ranking-row"}">
											<button class="rank-sort" data-route="/ranking/average">Average Points</button>
										</th>
									</tr>
							`;

							for (const user of Object.values(users)) {
								if (user.username == ndata.user.username) {
									html += `
										<tr class="rank-user">
									`;
								} else {
									html += `
										<tr>
									`;
								}

								html += `
										<td class="rank-position">${user.rank}</td>
										<td>
											<button class="rank-user-info" data-route="/profile/${user.username}">
												<img class="rank-image" src="${user.photo_url}" alt="photo">
												${user.username}
											</button>
										</td>
										<td class="${sortedBy.split('_')[0] == "solo" ? "selected-row" : "ranking-row"}">${user.player.soloPoints[user.player.soloPoints.length - 1]}</td>
										<td class="${sortedBy.split('_')[0] == "death" ? "selected-row" : "ranking-row"}">${user.player.deathPoints[user.player.deathPoints.length - 1]}</td>
										<td class="${sortedBy.split('_')[0] == "tournament" ? "selected-row" : "ranking-row"}">${user.player.tournamentPoints[user.player.tournamentPoints.length - 1]}</td>
										<td class="${sortedBy.split('_')[0] == "total" ? "selected-row" : "ranking-row"}">${user.player.totalPoints[user.player.totalPoints.length - 1]}</td>
										<td class="${sortedBy.split('_')[0] == "game" ? "selected-row" : "ranking-row"}">${user.player.totalPoints.length - 1}</td>
										<td class="${sortedBy.split('_')[0] == "average" ? "selected-row" : "ranking-row"}">${user.player.averagePoints}</td>
									</tr>
								`;
							}

							html += `
								</table>
							`;

							document.getElementById('app').innerHTML = html;

							document.getElementById('userSearch').addEventListener('input', function(e) {
								var input = e.target.value.toUpperCase();
								var table = document.getElementById('ranking-table');
								var trs = table.getElementsByTagName('tr');
							
								for (var i = 0; i < trs.length; i++) {
									var tds = trs[i].getElementsByTagName('td');
									if (tds.length > 0) {
										var txtValue = tds[1].textContent || tds[1].innerText;
										if (txtValue.toUpperCase().indexOf(input) > -1) {
											trs[i].style.display = "";
										} else {
											trs[i].style.display = "none";
										}
									}
								}
							});


							// Handle the informations of ranking system
							document.querySelector('.ranking-title-info').addEventListener('click', () => {
								// Create the popup background
								let popupBackgroundHTML = '<div class="popup-background" id="popup-background"></div>';

								// Create the popup
								let popupHTML = `
									<div class="popup">
										<h3 class="title-popup">Ranking system</h3>
										<p class="popup-info-title">Solo games:</p>
										<p class="popup-info">The points won after a game represent the number of points scored during that game.</p>
								
										<p class="popup-info-title">DeathMatch games:</p>
										<p class="popup-info">
											10 points for the winner.</br>
											7 points for the second.</br>
											3 points for the third.</br>
											0 point for the last one.
										</p>

										<p class="popup-info-title">Tournament games:</p>
										<p class="popup-info">
											20 points for the winner.</br>
											15 points for the second.</br>
											7 points for the third.</br>
											0 point for the last one.
										</p>
									</div>
								`;

								// Create the popup background and the popup
								let popupBackground = document.createElement('div');
								popupBackground.innerHTML = popupBackgroundHTML;
								document.body.appendChild(popupBackground);

								let popup = document.createElement('div');
								popup.innerHTML = popupHTML;
								document.body.appendChild(popup);

								// Handle the click on the close button
								document.getElementById('popup-background').addEventListener('click', () => {
									popup.remove();
									popupBackground.remove();
								});
							});

						}});
				} else {
					router.navigate('/pong/');
				}
			});
		} else {
			router.navigate('/sign_in/');
		}
	});
}