function renderHeader() {

	// Get the header
	fetchAPI('/api/header').then(data => {
		const header = document.querySelector('.header-menu');

		// If the user is authenticated
		if (data.isAuthenticated) {

			// Display the user's informations
			header.classList.add('user-authenticated');
			header.classList.remove('user-guest');

			document.getElementById('header-username').textContent = data.username;
			document.getElementById('header-user-photo').src = data.photo_url;
			document.getElementById('header-notification-count').textContent = data.nbNewNotifications;

		// If the user is not authenticated
		} else {
			header.classList.add('user-guest');
			header.classList.remove('user-authenticated');
		}
	})
	.catch((error) => {});
}