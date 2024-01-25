function renderUsersPage() {
	
	// Check if the user is authenticated
	fetchAPI('/api/is_authenticated').then(data => {
		if (!data.isAuthenticated) {
			router.navigate('/sign_in/');
			return;
		}

		let html = '<div id="status-log" class="status-log">';

		// Get the users
		fetchAPI('/api/users').then(dataUsers => {

			if (Object.keys(dataUsers.users).length === 0) {
				html += `
					<div class="all-users">
						<h1>All users</h1>
						<div class="list">
							<h4 class="no-users">No users</h4>
						</div>
					</div>
				`;

			// Display the users
			} else {
				html += `
					<div class="all-users">
						<h1>All users</h1>
						<div class="list">
				`;

				for (const user of Object.values(dataUsers.users)) {
					html += `
							<button class="menu-link" data-route="/profile/${user.username}">
								<div class="container" data-user-id="${user.id}">
									<img src="${user.photo_url}" alt="profile picture">
									<h3>${user.username}</h3>
					`;
					if (!user.status.includes("chat")) {
						html += `
									<p class="status">${user.status}</p>
						`;
					} else {
						html += `
									<p class="status">online</p>
						`;
					}
					html += `
								</div>
							</button>
					`;
				}

				html += `
						</div>
					</div>
				`;
			}

			// Get the follows
			fetchAPI('/api/follows').then(dataFollows => {

				// check if the dict dataFollows.follows is empty
				if (Object.keys(dataFollows.follows).length === 0) {
					html += `
						<div class="friend">
							<h1>Friends</h1>
							<div class="list">
								<h4 class="no-friends">No friends</h4>
							</div>
						</div>
					`;
	
				// Display the friends
				} else {
					html += `
						<div class="friend">
							<h1>Friends</h1>
							<div class="list">
					`;

					for (const user of Object.values(dataFollows.follows)) {
						html += `
								<button class="menu-link" data-route="/profile/${user.username}">
									<div class="container" data-user-id="${user.id}">
										<img src="${user.photo_url}" alt="profile picture">
										<h3>${user.username}</h3>
						`;
						if (!user.status.includes("chat")) {
							html += `
										<p class="status">${user.status}</p>
							`;
						} else {
							html += `
										<p class="status">online</p>
							`;
						}
						html += `
									</div>
								</button>
						`;
					}
				}

				html += `
							</div>
						</div>
				`;

				// Display the users page
				document.getElementById('app').innerHTML = html;
			});
		});
	});
}