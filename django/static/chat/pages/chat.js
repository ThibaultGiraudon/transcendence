function renderChannel(channel) {
	let badge = "";
	if (channel.room_id == "general") {
		badge = "🌍 Global";
	} else if (channel.private) {
		badge = "👥 Private discution";
	} else if (channel.tournament) {
		badge = "🎯 Tournament";
	} else if (!channel.creator) {
		badge = "⭐ Official";
	}

	let sender = '';
	if (channel.last_message) {
		sender = channel.last_message.sender;
		if (sender == 0) {
			sender = "System";
		}
	}

	return `
		<div class="a-chat">
			<a class="chat-container" data-route="/chat/${channel.room_id}">
				<h4 class="chat-badge">${badge}</h4>
				<h3 class="chat-name">${channel.name}</h3>
				${channel.last_message ? `
					<p class="chat-last-message-timestamp">${channel.last_message.timestamp}</p>
					<div class="chat-last-message-container">
						<p class="chat-last-message-sender">${sender}: </p>
						<p class="chat-last-message">${channel.last_message.message.substring(0, 50)}${channel.last_message.message.length > 50 ? '...' : ''}</p>
					</div>
				`
				:
				`
					<p class="chat-last-message-timestamp">No message yet, be the first!</p>
				`
				}
			</a>
			<button class="chat-info-button" id="${channel.room_id}">
				<img class="chat-info-button-img" src="/static/chat/img/info.png" alt="Info">
			</button>
		</div>
	`;
}


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

			// Display the favorites chats
			if (dataUser.user.favoritesChannels.length > 0) {
				document.getElementById('app').innerHTML += `
					${dataUser.user.favoritesChannels.length == 1 ? '<h3 class="chat-section">• Favorite</h3>' : '<h3 class="chat-section">• Favorites</h3>'}
					<div class="chat-scrollable">
						${Object.values(dataUser.user.channels).map(channel => {
							// Check if the channel is a DM with a blocked user
							if (channel.private) {
								for (let user of Object.values(channel.users)) {
									if (user.blocked) { return ; }
								}
							}

							if (dataUser.user.favoritesChannels.includes(channel.room_id)) {
								return renderChannel(channel);
							}
						}).join('')}
					</div>
				`;
			}

			// Display the other chats
			if (Object.keys(dataUser.user.channels).length != dataUser.user.favoritesChannels.length) {	
				document.getElementById('app').innerHTML += `
					${Object.keys(dataUser.user.channels).length - Object.keys(dataUser.user.favoritesChannels).length == 1 ? '<h3 class="chat-section">• Channel</h3>' : '<h3 class="chat-section">• Channels</h3>'}
					<div class="chat-scrollable">
						${Object.values(dataUser.user.channels).map(channel => {
							// Check if the channel is a DM with a blocked user
							if (channel.private) {
								for (let user of Object.values(channel.users)) {
									if (user.blocked) { return ; }
								}
							}
							
							if (!dataUser.user.favoritesChannels.includes(channel.room_id)) {
								return renderChannel(channel);
							}
						}).join('')}
					</div>
				`;
			}


		// If the user has no chats
		} else {
			document.getElementById('app').innerHTML += '<p>No channels available.</p>';
		}

		// Add the button to start a new chat
		document.getElementById('app').innerHTML += `
			<button class="profile-button" data-route="/chat/new/">Start a new chat group ➜</button>
		`;

		// Handle the informations of a chat
		document.querySelectorAll('.chat-info-button').forEach(button => {
			button.addEventListener('click', () => {

				// Get the channel
				let channel = dataUser.user.channels[button.id];

				// Create the popup background
				let popupBackgroundHTML = '<div class="popup-background" id="popup-background"></div>';

				// Create the popup
				let popupHTML = `
					<div class="popup">
						<h3 class="title-popup">Informations</h3>
				`;

				// Add informations
				popupHTML += `
					<p class="popup-info-title">Name:</p>
					<p class="popup-info">${channel.name}</p>

					<p class="popup-info-title">Description:</p>
					<p class="popup-info">${channel.description}</p>

					<p class="popup-info-title">Creator:</p>
					<p class="popup-info">${channel.creator_username}</p>

					<p class="popup-info-title">Private:</p>
					<p class="popup-info">${channel.private ? 'Yes' : 'No'}</p>

					<p class="popup-info-title">Members:</p>
					<p class="popup-info">${Object.values(dataUser.user.channels[button.id].users).map(user => user.username).join(', ')}</p>
				`;


				popupHTML += `
						${ dataUser.user.favoritesChannels.includes(channel.room_id) ? `
							<button class="button-popup" id="global-chat">Remove from favorite</button>`
						: `
							<button class="button-popup" id="favorite-chat">Add to favorite</button>`
						}
				`;

				if (channel.room_id != "general") {
					popupHTML += `
						<button class="button-leave-popup" id="leave-chat">Leave</button>
					`;
				}

				popupHTML += `
						<button class="close-popup" id="close-popup">Close</button>
					</div>
				`;
				

				// Add informations
				popupHTML += `
					<p class="popup-info">Name: ${channel.name}</p>
				`;

				// Create the popup background and the popup
				let popupBackground = document.createElement('div');
				popupBackground.innerHTML = popupBackgroundHTML;
				document.body.appendChild(popupBackground);

				let popup = document.createElement('div');
				popup.innerHTML = popupHTML;
				document.body.appendChild(popup);

				// Handle the click on the close button
				document.getElementById('close-popup').addEventListener('click', () => {
					popup.remove();
					popupBackground.remove();
				});

				document.getElementById('popup-background').addEventListener('click', () => {
					popup.remove();
					popupBackground.remove();
				});

				// Add to favorite
				if (document.getElementById('favorite-chat')) {
					document.getElementById('favorite-chat').addEventListener('click', () => {
						popup.remove();
						popupBackground.remove();
						fetchAPI(`/api/add_to_favorite/${channel.room_id}`).then(data => {
							if (data.success) {
								router.navigate('/chat/');
								return ;
							}
						});
					});
				}

				// Remove from favorite
				if (document.getElementById('global-chat')) {
					document.getElementById('global-chat').addEventListener('click', () => {
						popup.remove();
						popupBackground.remove();
						fetchAPI(`/api/remove_from_favorite/${channel.room_id}`).then(data => {
							if (data.success) {
								router.navigate('/chat/');
								return ;
							}
						});
					});
				}

				// Remove from favorite
				if (document.getElementById('leave-chat')) {
					document.getElementById('leave-chat').addEventListener('click', () => {
						fetchAPI(`/api/leave_channel/${channel.room_id}`).then(data => {
							if (data.success) {
								popup.remove();
								popupBackground.remove();
								router.navigate('/chat/');
								return ;
							}
						});
					});
				}
			});
		});
	});
}