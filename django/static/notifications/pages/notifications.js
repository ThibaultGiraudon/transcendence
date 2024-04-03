// Variables
let totalMessages = {};


function renderNotification(notification, index) {
	let image;
	if (notification.imageType === 'message') {
		if (notification.interacted) {
			image = '/static/notifications/img/message_open.png';
		} else {
			image = '/static/notifications/img/message_close.png';
		}

	} else if (notification.imageType === 'user') {
		image = notification.imageUser;

	} else {
		image = '/static/notifications/img/empty.png';
	}

	return `
		<div data-ignore-click data-route="${notification.redirect}" data-notification-id=${notification.id} class="notification" data-index="${index}">
			<div class="notification-containers">
				
				<div class="notification-theme">
					<img class="notification-theme-img" src="${image}">
				</div>

				<div class="notification-content">

					<span class="notification-title" data-index="${index}">${safeText(notification.title)}</span>
					<span class="notification-message" data-index="${index}">${safeText(notification.message)}</span>
					<span class="notification-date" data-index="${index}">${safeText(notification.date)}</span>

					<div class="notification-buttons">

						${notification.type === 'request-friend' ? `
						<a data-ignore-click data-notification-id=${notification.id} data-user-id=${notification.userID}>
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

	// Get the notifications
	fetchAPI('/api/get_notifications').then(data => {

		// Update the header to clear notifs count
		renderHeader();

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
			totalMessages = {};

			for (notification of reversedNotifications) {

				// If the notification is a message, count the total number from the same channel
				if (notification.type === 'message') {
					const channel = notification.message;

					if (totalMessages[channel] === undefined) {
						totalMessages[channel] = [notification];

						for (notification of reversedNotifications) {
							if (notification === totalMessages[channel][0])
								continue;
							else if (notification.type === 'message' && notification.message === channel) {
								totalMessages[channel].push(notification);
							}
						}

						if (totalMessages[channel].length === 1) {
							totalMessages[channel][0].message = "You have a new message from " + totalMessages[channel][0].message;
						} else {
							totalMessages[channel][0].message = "You have " + totalMessages[channel].length + " new messages from " + totalMessages[channel][0].message;
						}

						document.getElementById('app').innerHTML += renderNotification(totalMessages[channel][0], index);
					
						// Change the background color of the notification if it's not read
						if (!totalMessages[channel][0].read) {
							document.querySelector(`.notification[data-index="${index}"]`).style.backgroundColor = '#F3F2ED';
				
							document.querySelector(`.notification-title[data-index="${index}"]`).style.color = 'black';
				
							document.querySelector(`.notification-message[data-index="${index}"]`).style.fontWeight = 'bold';
							document.querySelector(`.notification-message[data-index="${index}"]`).style.color = 'black';
				
							document.querySelector(`.notification-date[data-index="${index}"]`).style.fontWeight = 'bold';
							document.querySelector(`.notification-date[data-index="${index}"]`).style.color = 'black';
						}
						index++;
					}
				} else {
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
			
				// Select filter "all" by default
				document.querySelector('.notification-filter[data-filter="all"]').style.border = '1px solid #474747';
			}
		};

		// Add event listeners on the delete buttons
		document.querySelectorAll('.notification-delete').forEach(button => {
			button.addEventListener('click', async function(event) {
				event.preventDefault();

				const notificationId = button.getAttribute('data-notification-id');
				if (notificationId === null) {
					return ;
				}

				for (notificationList in totalMessages) {
					if (totalMessages[notificationList][0].id === parseInt(notificationId)) {
						let promises = totalMessages[notificationList].map(notification => 
							fetchAPI(`/api/delete_notification/${notification.id}`)
						);
						
						Promise.all(promises).then(() => {
							router.navigate('/notifications/');
							return ;
						});
					}
				}

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

				// If the user clicked on a notification's button
				if (event.target.classList.contains('notification-delete')) {
					return ;
				} else if (event.target.classList.contains('notification-button-text')) {
					return ;
				}

				const notificationId = notification.getAttribute('data-notification-id');
				fetchAPI(`/api/interacted_notification/${notificationId}`).then(data => {
					const url = notification.getAttribute('data-route');
					router.navigate(url);
					return ;
				});
			});
		});

		// Add a listener to the accept friend button
		document.querySelectorAll('.notification-buttons a').forEach(button => {
			button.addEventListener('click', function(event) {
				event.preventDefault();

				const notificationId = button.getAttribute('data-notification-id');
				if (notificationId === null) {
					return ;
				}

				const userID = button.getAttribute('data-user-id');
				if (userID === null) {
					return ;
				}

				fetchAPI(`/api/follow/${userID}`).then(data => {
					fetchAPI(`/api/delete_notification/${notificationId}`).then(data => {
						router.navigate('/notifications/');
						return ;
					});
				});
			});
		});

		// Add event listeners on the filters
		document.querySelectorAll('.notification-filter').forEach(filter => {
			filter.addEventListener('click', function(event) {
				event.preventDefault();

				const filterName = filter.getAttribute('data-filter');
				if (filterName === null) {
					return ;
				}

				// Reset all filter bold style
				document.querySelectorAll('.notification-filter').forEach(filter => {
					filter.style.border = '0px solid #474747';
				});

				// Display all the notifications
				if (filterName === 'all') {
					document.querySelectorAll('.notification').forEach(notification => {
						notification.style.display = 'flex';

						filter.style.border = '1px solid #474747';
					});

				// Display only the messages
				} else if (filterName === 'messages') {
					document.querySelectorAll('.notification').forEach(notification => {
						if (notification.querySelector('.notification-title').textContent.includes('New message')) {
							notification.style.display = 'flex';
						} else {
							notification.style.display = 'none';
						}
						filter.style.border = '1px solid #474747';
					});

				// Display only the friend requests
				} else if (filterName === 'requests') {
					document.querySelectorAll('.notification').forEach(notification => {
						if (notification.querySelector('.notification-title').textContent.includes('New friend request')) {
							notification.style.display = 'flex';
						} else {
							notification.style.display = 'none';
						}
						filter.style.border = '1px solid #474747';
					});
				}
			});
		});
	});
};