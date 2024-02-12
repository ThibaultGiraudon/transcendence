function renderUser(user) {
	return `
		<button class="menu-link" data-route="/profile/${user.username}">
			<div class="container" data-user-id="${user.id}">
				<img src="${user.photo_url}" alt="profile picture">
				<h3>${user.username}</h3>
				<p class="status">${user.status.includes("chat") ? "online" : user.status}</p>
			</div>
		</button>
	`;
}


function renderUsersSection(title, users) {
	if (Object.keys(users).length === 0) {
		return `
			<div class="${title.toLowerCase()}">
				<h1>${title}</h1>
				<div class="list">
					<h4 class="no-${title.toLowerCase()}">No ${title.toLowerCase()}</h4>
				</div>
			</div>
		`;
	} else {
		return `
			<div class="${title.toLowerCase()}">
				<h1>${title}</h1>
				<div class="list">
					${Object.values(users).map(renderUser).join('')}
				</div>
			</div>
		`;
	}
}


function renderUsersPage() {
	// Check if the user is authenticated
	fetchAPI('/api/isAuthenticated').then(data => {
		if (!data.isAuthenticated) {
			router.navigate('/sign_in/');
			return;
		}

		// Get the users
		fetchAPI('/api/users').then(dataUsers => {
			// Define categories
			let users = {};
			let followed = {};

			for (const user of Object.values(dataUsers.users)) {
				if (user.followed) {
					followed[user.id] = user;
				} else {
					users[user.id] = user;
				}
			}

			// Build the HTML
			let html = '<div id="status-log" class="status-log">';
			html += renderUsersSection('All users', users);
			html += renderUsersSection('Friends', followed);
			html += '</div>';

			// Display the users page
			document.getElementById('app').innerHTML = html;
		});
	});
}