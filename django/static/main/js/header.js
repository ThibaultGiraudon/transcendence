function renderHeader() {
	// Get the authentication status
	fetchAPI('/api/is_authenticated').then(data => {
		// Get the header
		const header = document.querySelector('.header-menu');

		if (data.isAuthenticated) {
			// If the user is authenticated
			header.classList.add('user-authenticated');
			header.classList.remove('user-guest');

			// Display the user's informations
			fetchAPI('/api/get_user').then(data => {
				if (data.user) {
					document.getElementById('username').textContent = data.user.username;
					document.getElementById('user-photo').src = data.user.photo_url;
					document.getElementById('notification-count').textContent = data.user.nbNewNotifications;
				} else {
					document.getElementById('username').textContent = "UserNotFound";
					document.getElementById('user-photo').src = "/static/users_app/img/default.jpg";
					document.getElementById('notification-count').textContent = "0";
				}
			})

		} else {
			// If the user is not authenticated
			header.classList.add('user-guest');
			header.classList.remove('user-authenticated');
		}
	})
	.catch((error) => {});
}
