function renderNotification(notification, index) {
	let image;
	if (notification.imageType === 'message') {
		image = '/static/notifications/img/message.png';

	} else if (notification.imageType === 'user') {
		image = notification.imageUser;

	} else {
		image = '/static/notifications/img/empty.png';
	}

	return `
		<div data-ignore-click data-route="${notification.redirect}" class="notification" data-index="${index}">
			<div class="notification-containers">
				
				<div class="notification-theme">
					<img class="notification-theme-img" src="${image}">
				</div>

				<div class="notification-content">

					<span class="notification-title" data-index="${index}">${notification.title}</span>
					<span class="notification-message" data-index="${index}">${notification.message}</span>
					<span class="notification-date" data-index="${index}">${notification.date}</span>

					<div class="notification-buttons">

						${notification.type === 'request-friend' ? `
						<a data-ignore-click data-notification-id=${notification.id}>
							<p class="notification-button-text">Accept</p>
						</a>
						` : ''}	
					
						<a data-ignore-click class="notification-delete" data-notification-id=${notification.id}>
							<img class="notification-delete-img" src="/static/notifications/img/delete.png" alt="Delete">
						</a>
					</div>
				</div>
			</div>
		</div>
	`;
}


function renderNotificationsPage() {

	// If the user is not connected
	fetchAPI('/api/isAuthenticated').then(data => {
		if (!data.isAuthenticated) {
			router.navigate('/sign_in/');
			return ;
		}
	});

	// Update the header to clear notifs count
	renderHeader();

	// Get the notifications
	fetchAPI('/api/get_notifications').then(data => {

		// Reverse the notifications
		let reversedNotifications = Object.values(data.notifications).reverse();

		// Display the notifications page
		document.getElementById('app').innerHTML = `
			<h1>Notifications</h1>

			<div class="notifications-actions">
				
				<div class="notifications-filters">

					<p class="notification-filter-title">Filters:</p>
					<a data-ignore-click class="notification-filter" data-filter="all">
						All
					</a>
					<p class="notification-filter-divider">|</p>
					<a data-ignore-click class="notification-filter" data-filter="messages">
						Messages
					</a>
					<p class="notification-filter-divider">|</p>
					<a data-ignore-click class="notification-filter" data-filter="requests">
						Friends requests
					</a>
				</div>

				<a class="notification-delete-all">Delete All</a>
			</div>
		`;

		if (reversedNotifications.length === 0) {
			document.getElementById('app').innerHTML += `
				<p class="no-notification">No notifications.</p>
			`;

		} else {
			let index = 0;
			for (notification of reversedNotifications) {
				document.getElementById('app').innerHTML += renderNotification(notification, index);
			
				// Change the background color of the notification if it's not read
				if (!notification.read) {
					document.querySelector(`.notification[data-index="${index}"]`).style.backgroundColor = '#F3F2ED';
		
					document.querySelector(`.notification-title[data-index="${index}"]`).style.color = 'black';
		
					document.querySelector(`.notification-message[data-index="${index}"]`).style.fontWeight = 'bold';
					document.querySelector(`.notification-message[data-index="${index}"]`).style.color = 'black';
		
					document.querySelector(`.notification-date[data-index="${index}"]`).style.fontWeight = 'bold';
					document.querySelector(`.notification-date[data-index="${index}"]`).style.color = 'black';
				}
				index++;
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

		// Add a listener to redirect when clicking on a notification
		document.querySelectorAll('.notification').forEach(notification => {
			notification.addEventListener('click', function(event) {
				event.preventDefault();

				// If the user clicked on the delete button, don't redirect
				if (event.target.classList.contains('notification-delete')) {
					return ;
				}

				const url = notification.getAttribute('data-route');
				router.navigate(url);
			});
		});
	});
};