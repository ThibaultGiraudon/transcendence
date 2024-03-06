// Initialize the chart to display the player's statistics
let chart;


function renderLineGraph(id, player) {
	let ctx = null;
	let title = '';
	let color = '';
	let data = {};

	// Assign new chart
	switch (id) {
		case "totalPoint-canvas":
			ctx = document.getElementById("totalPoint-canvas").getContext("2d");
			title = "Total Points";
			color = "#E21E59";
			data = player.totalPoints;
			break;

		case "soloPoint-canvas":
			ctx = document.getElementById("soloPoint-canvas").getContext("2d");
			title = "1v1 Points";
			color = "#1598E9";
			data = player.soloPoints;
			break;

		case "deathPoint-canvas":
			ctx = document.getElementById("deathPoint-canvas").getContext("2d");
			title = "Death Points";
			color = "#2FD661";
			data = player.deathPoints;
			break;

		case "tournamentPoint-canvas":
			ctx = document.getElementById("tournamentPoint-canvas").getContext("2d");
			title = "Tournament Points";
			color = "#F19705";
			data = player.tournamentPoints;
			break;
	}

	// Destroy the previous chart
	if (chart) {
		chart.destroy();
	}

	// Create chart
	chart = new Chart(ctx, {
	type: "line",
	data: {
		labels: [1,2,3,4,5,6,7,8,9],
		datasets: [
			{
			label: title,
			backgroundColor: color,
			borderColor: color,
			data: data,
			}
		]
	},
	options: {
		scales: {
			y: {
			title: {
				display: true,
				text: 'Points'
			}
			},
			x: {
			title: {
				display: true,
				text: 'Games Played'
			}
			}
		},
		plugins: {
			legend: {
			display: true,
			},
		}
		}
	});
}


function renderStatsPage() {
	
	fetchAPI('/api/isAuthenticated').then(data => {
		if (data.isAuthenticated) {
			
			fetchAPI('/api/get_user').then(data => {
				if (data.user) {
					const user = data.user;
					const player = user.player;

					document.getElementById('app').innerHTML = `
						<h1>Statistics</h1>
						<div class="stats-container">
							<div class="carousel-container">
								<button data-ignore-click class="carousel-button" id="carousel-left-btn">
									<img class="carousel-img" src="/static/stats/img/left.png" alt="left">
								</button>
								<canvas class="carousel-content" id=""></canvas>
								<button data-ignore-click class="carousel-button" id="carousel-right-btn">
									<img class="carousel-img" src="/static/stats/img/right.png" alt="right">
								</button>
							</div>
							<div class="pie-stats-container">
								<div class="pie-stats-games">
									<canvas class="pie-chart-games" id="pie-chart-games"></canvas>
								</div>
								<div class="pie-stats-points">
									<canvas class="pie-chart-points" id="pie-chart-points"></canvas>
								</div>
							</div>
						</div>
						`;

					const graph = document.querySelector('.carousel-content');
					const rightBtn = document.getElementById('carousel-right-btn');
					const leftBtn = document.getElementById('carousel-left-btn');

					const graphs = [
						"totalPoint-canvas",
						"soloPoint-canvas",
						"deathPoint-canvas",
						"tournamentPoint-canvas"
					];

					graph.id = graphs[0];
					renderLineGraph(graph.id, player);
					let position = 0;

					const moveRight = () => {
						if (position >= graphs.length - 1) {
							position = 0
							graph.id = graphs[position];
							renderLineGraph(graph.id, player);
							return;
						}
						graph.id = graphs[position + 1];
						renderLineGraph(graph.id, player);
						position++;
					}

					const moveLeft = () => {
						if (position < 1) {
							position = graphs.length - 1;
							graph.id = graphs[position];
							renderLineGraph(graph.id, player);
							return;
						}
						graph.id = graphs[position - 1];
						renderLineGraph(graph.id, player);
						position--;
					}

					rightBtn.addEventListener("click", moveRight);
					leftBtn.addEventListener("click", moveLeft);

					let ctx = document.getElementById("pie-chart-games").getContext("2d");

					let mychart = new Chart(ctx, {
						type: "pie",
						data: {
							labels: [
								"1v1 Games",
								"Death Games",
								"Tournament Games"
							],
							datasets: [{
								label: 'Games Played',
								backgroundColor: ["#1598E9", "#2FD661", "#F19705", ],
								data: [player.soloPoints.length, player.deathPoints.length, player.tournamentPoints.length,],
							}],
						},
						options: {
							plugins: {
								title: {
									display: true,
									text: 'Games Played',
									font: {
										size: 25
									}
								}
							}
						}
					});

					ctx = document.getElementById("pie-chart-points").getContext("2d");

					mychartgames = new Chart(ctx, {
						type: "pie",
						data: {
							labels: [
								"1v1 Points",
								"Death Points",
								"Tournament Points"
							],
							datasets: [{
								label: 'Points',
								backgroundColor: ["#1598E9", "#2FD661", "#F19705", ],
								data: [
									player.soloPoints[player.soloPoints.length - 1], 
									player.deathPoints[player.deathPoints.length - 1], 
									player.tournamentPoints[player.tournamentPoints.length - 1],
								],
							}],
						},
						options: {
							plugins: {
								title: {
									display: true,
									text: 'Points Distribution',
									font: {
										size: 25
									}
								}
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