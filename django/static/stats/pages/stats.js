function renderStatsPage() {
	fetchAPI('/api/isAuthenticated').then(data => {
		if (data.isAuthenticated) {
			fetchAPI('/api/get_user').then(data => {
				if (data.user) {
					user = data.user;
					player = user.player;
					totalPoints = player.totalPoints;
					soloPoints = player.soloPoints;
					deathPoints = player.deathPoints;
					tournamentPoints = player.tournamentPoints;
					console.log(totalPoints);
					let html = ``;

					html += `
						<h1>Stats</h1>
						<div class="all-stats-container">
							<div class="stats-container0">
								<canvas id="totalPoint-canvas"></canvas>
							</div>
							<div class="stats-container1">
								<canvas id="soloPoint-canvas"></canvas>
							</div>
							<div class="stats-container2">
								<canvas id="deathPoint-canvas"></canvas>
							</div>
							<div class="stats-container3">
								<canvas id="tournamentPoint-canvas"></canvas>
							</div>
						</div>
						`;
		
					document.getElementById('app').innerHTML = html;
		
					let ctx = document.getElementById("totalPoint-canvas").getContext("2d");

					let chart = new Chart(ctx, {
					type: "line",
					data: {
						labels: [1,2,3,4,5,6,7,8,9],
						datasets: [
							{
							label: "Total Points",
							backgroundColor: "#79AEC8",
							borderColor: "#417690",
							data: totalPoints,
							}
						]
					},
					options: {
						title: {
							text: "Total Points",
							display: true
						}
					}
					});

					ctx = document.getElementById("soloPoint-canvas").getContext("2d");

					chart = new Chart(ctx, {
					type: "line",
					data: {
						labels: [1,2,3,4,5,6,7,8,9],
						datasets: [
							{
							label: "1v1 Points",
							backgroundColor: "#79AEC8",
							borderColor: "#417690",
							data: soloPoints,
							}
						]
					},
					options: {
						title: {
							text: "1v1 Points",
							display: true
						}
					}
					});

					ctx = document.getElementById("deathPoint-canvas").getContext("2d");

					chart = new Chart(ctx, {
					type: "line",
					data: {
						labels: [1,2,3,4,5,6,7,8,9],
						datasets: [
							{
							label: "1v1 Points",
							backgroundColor: "#79AEC8",
							borderColor: "#417690",
							data: deathPoints,
							}
						]
					},
					options: {
						title: {
							text: "1v1 Points",
							display: true
						}
					}
					});

					ctx = document.getElementById("tournamentPoint-canvas").getContext("2d");

					chart = new Chart(ctx, {
					type: "line",
					data: {
						labels: [1,2,3,4,5,6,7,8,9],
						datasets: [
							{
							label: "1v1 Points",
							backgroundColor: "#79AEC8",
							borderColor: "#417690",
							data: tournamentPoints,
							}
						]
					},
					options: {
						title: {
							text: "1v1 Points",
							display: true
						}
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