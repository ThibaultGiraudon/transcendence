function renderChatPage() {

	// If the user is not connected
	fetchAPI('/api/isAuthenticated').then(data => {
		if (!data.isAuthenticated) {
			router.navigate('/sign_in/');
			return;
		}
	});

	// Get the current user
	fetchAPI('/api/get_user').then(dataUser => {
		document.getElementById('app').innerHTML = `<h1>Chats</h1>`;

		// Check if the user has chats
		if (Object.keys(dataUser.user.channels).length > 0) {

			// Display the chats
			document.getElementById('app').innerHTML += `
				<div class="chat-scrollable">
					${Object.values(dataUser.user.channels).map(channel => {
						return `
							<a class="chat-container" data-route="/chat/${channel.room_id}">
								<h3 class="chat-name">${channel.name}</h3>
								${channel.last_message ? `
									<p class="chat-last-message-timestamp">${channel.last_message.timestamp}</p>
									<div class="chat-last-message-container">
										<p class="chat-last-message-sender">${channel.last_message.sender}: </p>
										<p class="chat-last-message">${channel.last_message.message.substring(0, 50)}${channel.last_message.message.length > 50 ? '...' : ''}</p>
									</div>
								`
								:
								`
									<p class="chat-last-message-timestamp">No message yet, be the first!</p>
								`
								}
							</a>
						`;
					}).join('')}
				</div>
			`;
		// If the user has no chats
		} else {
			document.getElementById('app').innerHTML += '<p>No channels available.</p>';
		}
	});
}