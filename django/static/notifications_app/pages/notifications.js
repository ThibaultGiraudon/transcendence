function renderNotificationsPage() {

	// If the user is not connected
	fetchAPI('/api/isAuthenticated').then(data => {
		if (!data.isAuthenticated) {
			router.navigate('/sign_in/');
			return ;
		}
	});

	// Update the header
	renderHeader();

	// Get the notifications
	fetchAPI('/api/get_notifications').then(data => {

		// Display the notifications page
		document.getElementById('app').innerHTML = `
			<h1>Notifications</h1>

			<a class="notification-delete-all" data-route="delete_all_notifications">
				Delete All
			</a>
		`;

		if (Object.keys(data.notifications).length === 0) {
			document.getElementById('app').innerHTML += `
				<p class="no-notification">No notifications.</p>
			`;

		} else {
			
			for (notification in data.notifications) {
				document.getElementById('app').innerHTML += `
					<div class="notification">
				`;

				if (!notification.read) {
					document.getElementById('app').innerHTML += `
						<span class="notification-new">New</span>
					`;
				}

				document.getElementById('app').innerHTML += `
					<span class="notification-date">${notification.date}:</span>
					<span class="notification-message">${notification.message}</span>

					<a class="notification-delete" data-notification-id=${notification.id}>
						Delete
					</a>
				`;
			}
		};

		// Add event listeners on the delete buttons
		document.querySelectorAll('.notification-delete').forEach(button => {
			button.addEventListener('click', async function(event) {
				event.preventDefault();

				const notificationId = button.getAttribute('data-notification-id');
				fetchAPI(`/api/delete_notification/${notificationId}`).then(data => {
					router.navigate('/notifications/');
					return ;
				});
			});
		});

		// Add an event listener on the delete all button
		document.querySelector('.notification-delete-all').addEventListener('click', async function(event) {
			event.preventDefault();

			fetchAPI('/api/delete_all_notifications').then(data => {
				router.navigate('/notifications/');
				return ;
			});
		});
	});
};