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
			title = "Deathmatch Points";
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

	//Fill lables with the number of games played
	let labels = [];
	for (let i = 0; i < data.length + 9; i++) {
		labels.push(i);
	}

	// Create chart
	chart = new Chart(ctx, {
	type: "line",
	data: {
		labels: labels,
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

function renderPieGraph(id, player) {
	let ctx = null;
	let title = '';
	let data = {};
	if (id === "pie-chart-games") {
		ctx = document.getElementById("pie-chart-games").getContext("2d");
		title = "Games Played";
		data = [
			player.soloPoints.length - 1,
			player.deathPoints.length - 1,
			player.tournamentPoints.length - 1,
		];
	}
	else if (id === "pie-chart-points") {
		ctx = document.getElementById("pie-chart-points").getContext("2d");
		title = "Points Distribution";
		data = [
			player.soloPoints[player.soloPoints.length - 1], 
			player.deathPoints[player.deathPoints.length - 1], 
			player.tournamentPoints[player.tournamentPoints.length - 1],
		];
	}
	return (new Chart(ctx, {
		type: "pie",
		data: {
			labels: [
				"1v1 Games",
				"Deathmatch Games",
				"Tournament Games"
			],
			datasets: [{
				label: title,
				backgroundColor: ["#1598E9", "#2FD661", "#F19705", ],
				data: data,
			}],
		},
		options: {
			plugins: {
				title: {
					display: true,
					text: title,
					font: {
						size: 25
					}
				}
			}
		}}));
}


function renderOurProfile(user) {
	const officialImageHTML = user.isOfficial
		? `
			<img class="profile-official" src="/static/users/img/official.png">
			<span class="profile-official-text">Developper</span>
		`
		: '';

	return `
		<div class="profile">
			<img class="profile-img" src="${user.photo_url}" alt="profile picture">
			<div class="profile-infos">
				<div class="profile-official-container">
					<p class="profile-username">
						${user.username}
					</p>
					${officialImageHTML}
				</div>
				<p class="profile-email">${user.email}</p>
			</div>
		</div>
	`;
}

function renderOtherProfile(user) {
	const officialImageHTML = user.isOfficial
		? `
			<img class="profile-official" src="/static/users/img/official.png">
			<span class="profile-official-text">Developper</span>
		`
		: '';

	return `
		<div class="profile">
			<img class="profile-img" src="${user.photo_url}" alt="profile picture">
			<div class="profile-infos">
				<div class="profile-official-container">
					<p class="profile-username">
						${user.username}
					</p>
					${officialImageHTML}
				</div>
			</div>
		</div>
	`;
}


function checkboxEmail(user) {
	const checkedAttribute = user.emailAlerts ? ' checked' : '';
	return `
		<div class="checkbox-wrapper">
			<label class="control control--checkbox">
				Receive alerts by email about your activity
				<input type="checkbox" ${checkedAttribute} />
				<div class="control__indicator"></div>
			</label>
		</div>
	`;
}


function renderForm(fieldsHtml, user) {
	return `
		<div class="form-div">
			<form class="sign-form" method="POST" enctype="multipart/form-data" novalidate>
				<h3 class="sign-title">Edit informations</h3>
				${fieldsHtml}

				${checkboxEmail(user)}

				<p class="error-message" id="error-message"></p>
				<input type="submit" value="Accept modifications"/>
				<button class="profile-sign-out-button" id="sign-out">Sign out</button>
				</form>
		</div>
	`;
}


function renderFollowButton(currentUser, user) {
	if (currentUser.follows.includes(user.id)) {
		return `
			<button class="profile-button unfollow" data-user-id="${user.id}">
				Unfollow
			</button>
		`;
	} else {
		if (user.friendRequests.includes(currentUser.id))
			return `
				<button class="profile-button follow" data-user-id="${user.id}">
					Accept friend request
				</button>
			`;
		else if (currentUser.friendRequests.includes(user.id))
			return `
				<p class="profile-button-pending">
					Pending...
				</p>
			`;
		else
		return `
			<button class="profile-button follow" data-user-id="${user.id}">
				Send a friend request
			</button>
		`;
	}
}


function renderChatButton(room) {
	if (room) {
		return `
			<button class="profile-button" data-route="/chat/${room}">
				Send a chat
			</button>
		`;
	} else {
		return `
			<button class="profile-button chat">
				Send a chat
			</button>
		`;
	}
}


function renderBlockedButton(user) {
	return `
		<button class="profile-button block" data-user-id="${user.id}">
			Block
		</button>
	`;
}

function renderPongStats(user) {
	const player = user.player;

	document.getElementById('app').innerHTML += `
		<h2>Statistics</h2>
		<div class="stats-container">
			<div class="carousel-container">
				<button data-ignore-click class="carousel-button" id="carousel-left-btn">
					<img class="carousel-img" src="/static/users/img/left.png" alt="left">
				</button>
				<canvas class="carousel-content" id=""></canvas>
				<button data-ignore-click class="carousel-button" id="carousel-right-btn">
					<img class="carousel-img" src="/static/users/img/right.png" alt="right">
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

	let pieChartGames = renderPieGraph("pie-chart-games", player);
	let pieChartPoints = renderPieGraph("pie-chart-points", player);
}


function renderProfilePage(username) {

	fetchAPI('/api/isAuthenticated').then(data => {
		// If the user is already connected
		if (data.isAuthenticated) {

			// Get the user
			fetchAPI('/api/get_user/' + username).then(data => {
				if (data.user) {
					const user = data.user;
					let fields = [];

					if (user.is42) {
						fields = [
							{ name: 'input-username', label: 'Username', type: 'text', value: user.username },
							{ name: 'input-photo', label: 'Profile picture', type: 'file', accept: 'image/*' },
						];
					} else {
						fields = [
							{ name: 'input-username', label: 'Username', type: 'text', value: user.username },
							{ name: 'input-photo', label: 'Profile picture', type: 'file', accept: 'image/*' },
							{ name: 'input-email', label: 'Email', type: 'email', value: user.email },
							{ name: 'input-password', label: 'Password', type: 'password' }
						];
					}

					// Display the current user's informations
					if (data.isCurrentUser) {
						const fieldsHtml = fields.map(renderField).join('');
						const profileHtml = renderOurProfile(user);
						const formHtml = renderForm(fieldsHtml, user);

						document.getElementById('app').innerHTML = `
							${profileHtml}
							${formHtml}
						`;

						renderPongStats(user);

						// Add an event listener on the sign-in form
						document.querySelector('.sign-form').addEventListener('submit', async function(event) {
							event.preventDefault();

							// Clear errors messages
							document.getElementById('error-input-username').textContent = '';
							document.getElementById('error-input-photo').textContent = '';
							if (!user.is42) {
								document.getElementById('error-input-email').textContent = '';
								document.getElementById('error-input-password').textContent = '';
							}

							// Get data from the form
							const new_username = document.getElementById('input-username').value;
							const photo = document.getElementById('input-photo').files[0];
							let new_email, new_password;
							if (!user.is42) {
								new_email = document.getElementById('input-email').value;
								new_password = document.getElementById('input-password').value;
							}

							// Validate the data
							if (!new_username) {
								document.getElementById('error-input-username').textContent = 'This field is required.';
								return;
							}

							// Convert the photo to a Base64 string
							let photoBase64 = null;
							if (photo) {
								// Wait for the photo to be converted to Base64
								const reader = new FileReader();
								reader.readAsDataURL(photo);

								await new Promise(resolve => {
									reader.onloadend = function() {
										photoBase64 = reader.result.replace('data:', '').replace(/^.+,/, '');
										resolve();
									}
								});
							}

							// Get the checkbox value
							const emailAlerts = document.querySelector('.control--checkbox input').checked;

							// Send data to the server
							if (user.is42) {
								new_email = user.email;
								new_password = '';
							}

							const response = await fetch('/profile/' + user.username, {
								method: 'POST',
								headers: {
									'X-Requested-With': 'XMLHttpRequest',
									'X-CSRFToken': getCookie('csrftoken'),
								},
								body: JSON.stringify({ new_username, photo: photoBase64, new_email, new_password, emailAlerts })
							});

							if (response.headers.get('content-type').includes('application/json')) {
								const responseData = await response.json();

								if (responseData.success) {
									renderHeader();
									router.navigate('/profile/' + new_username);
									return ;
	
								} else {
									// If the connection failed, display the error message
									document.getElementById('error-input-username').textContent = responseData.username;
									document.getElementById('error-input-photo').textContent = responseData.photo;
									if (!user.is42) {
										document.getElementById('error-input-email').textContent = responseData.email;
										document.getElementById('error-input-password').textContent = responseData.password;
									}
									document.getElementById('error-message').textContent = responseData.message;
								}
							
							} else {
								if (response.status == 413) {
									document.getElementById('error-message').textContent = "The photo size is too large.";
								} else {
									document.getElementById('error-message').textContent = "The server encountered an unexpected error.";
								}
							}
						});


						// Add an event listener on the sign-out button
						document.getElementById('sign-out').addEventListener('click', async function(event) {

							// Logout the user
							fetchAPI('/api/sign_out').then(data => {
								renderHeader();
								SignOutProcess(user.id);

								router.navigate('/sign_in/');
								return ;
							});
						});
					
					// Display the user's informations
					} else {
						fetchAPI('/api/get_user').then(data => {
							// If the user is not connected
							if (!data.user) {
								router.navigate('/sign_in/');
								return;
							}

							const currentUser = data.user;

							// Get the room
							let room = null;
							if (currentUser.channels) {
								for (channel of Object.values(currentUser.channels)) {
									if (channel.private && user.id in channel.users && currentUser.id in channel.users) {
										room = channel.room_id;
										break;
									}
								}
							}


							// Generate the profile page HTML
							const profileHtml = renderOtherProfile(user);
							document.getElementById('app').innerHTML = `
								${profileHtml}
							`;

							if (currentUser.blockedUsers.includes(user.id)) {
								document.getElementById('app').innerHTML += `
									<button class="profile-button unblock" data-user-id="${user.id}">
										Unblock
									</button>
									<p class="profile-blocked">You can't send a chat or follow this user</p>
								`;

							} else {
								
								const followButtonHtml = renderFollowButton(currentUser, user);
								const blockedButtonHtml = renderBlockedButton(user);
								const chatButtonHtml = renderChatButton(room);

								document.getElementById('app').innerHTML += `
									<div class="profile-actions">
										${followButtonHtml}
										${blockedButtonHtml}
										${chatButtonHtml}
									</div>
								`;
							}
							renderPongStats(user);

							
							// Add an event listener on the send a chat button (for new chat only)
							const sendChatButton = document.querySelector('.profile-button.chat');
							if (sendChatButton) {
								sendChatButton.addEventListener('click', async function(event) {
									// Create the chat
									fetchAPI('/api/create_channel?user_ids=' + user.id + '&user_ids=' + currentUser.id + '&private=True').then(data => {
										router.navigate('/chat/' + data.room_id);
										return ;
									});
								});
							}
							
							// Add an event listener on the follow button
							const followButton = document.querySelector('.profile-button.follow');
							if (followButton) {
								followButton.addEventListener('click', async function(event) {
									// Follow the user
									fetchAPI('/api/follow/' + event.target.dataset.userId).then(data => {
										router.navigate('/profile/' + user.username);
										return ;
									});
								});
							}

							// Add an event listener on the unfollow button
							const unfollowButton = document.querySelector('.profile-button.unfollow');
							if (unfollowButton) {
								unfollowButton.addEventListener('click', async function(event) {
									// Unfollow the user
									fetchAPI('/api/unfollow/' + event.target.dataset.userId).then(data => {
										router.navigate('/profile/' + user.username);
										return ;
									});
								});
							}

							// Add an event listener on the block button
							const blockButton = document.querySelector('.profile-button.block');
							if (blockButton) {
								blockButton.addEventListener('click', async function(event) {
									// Block the user
									fetchAPI('/api/block/' + event.target.dataset.userId).then(data => {
										router.navigate('/profile/' + user.username);
										return ;
									});
								});
							}

							// Add an event listener on the unblock button
							const unblockButton = document.querySelector('.profile-button.unblock');
							if (unblockButton) {
								unblockButton.addEventListener('click', async function(event) {
									// Unblock the user
									fetchAPI('/api/unblock/' + event.target.dataset.userId).then(data => {
										router.navigate('/profile/' + user.username);
										return ;
									});
								});
							}
						})
					}

				// If the user does not exist
				} else {
					router.navigate('/users/');
					return ;
				}
			})
		
		// If the user is not connected
		} else {
			router.navigate('/sign_in/');
			return ;
		}
	})
}