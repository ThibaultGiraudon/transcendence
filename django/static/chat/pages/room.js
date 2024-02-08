function renderRoomPage(room_id) {

	// If the user is not connected
	fetchAPI('/api/get_user').then(dataUser => {
		if (!dataUser.isAuthenticated) {
			router.navigate('/sign_in/');
			return;
		}
		
		const user = dataUser.user;
		if (user === null) {
			router.navigate('/sign_in/');
			return;
		}

		// Get the room
		let room = null;
		for (let channel of Object.values(user.channels)) {
			if (channel.room_id == room_id) {
				room = channel;
			}
		}

		// If the user is not in the room
		if (room === null) {
			router.navigate('/chat/');
			return;
		}

		// Check if the channel is private and the other user is blocked
		if (room.private && Object.keys(room.users).length == 2) {
			const userIds = Object.keys(room.users);
			if (userIds[0] == user.id) {
				if (userIds[1] in user.blockedUsers) {
					router.navigate('/chat/');
					return;
				}
			} else {
				if (userIds[0] in user.blockedUsers) {
					router.navigate('/chat/');
					return;
				}
			}
		}

		// Get the messages
		fetchAPI(`/api/get_messages/${room_id}`).then(dataMessages => {

			const messages = dataMessages.messages;
			if (!messages) {
				router.navigate('/chat/');
				return;
			}

			// Get the name and the photo of the channel
			let name_channel = null;
			let photo_channel = null;

			if (room.private && Object.keys(room.users).length == 2) {
				const users = Object.values(room.users);
				if (users[0].id == user.id) {
					name_channel = users[1].username;
					photo_channel = users[1].photo_url;
				} else {
					name_channel = users[0].username;
					photo_channel = users[0].photo_url;
				}
			} else {
				name_channel = room.name;
			}

			// Display the room page
			let html = `<div class="chat-window">`;

			// Display the participants
			if (!room.private) {
				html += `
					<div class="participants">
						<h2 class="chat-category">Participants</h2>
						
						<div class="list-participants">
							${Object.values(room.users).map(some_user => `
								<a data-route="/profile/${some_user.username}">
									<div class="participants-container">
										<img class="participants-img" src="${some_user.photo_url}" alt="profile picture">
										<h3 class="participants-username">
											${some_user.username}
											${some_user.id == user.id ? '<span class="you-text">(You)</span>' : ''}
										</h3>
									</div>
								</a>
							`).join('')}
						</div>
					</div>
				`;
			}

			// Open HTML
			html += `<div class="chat">`;

			// Display informations about the chat
			if (room.private && Object.keys(room.users).length == 2) {
				html += `
					<a class="chat-private-user" data-route="/profile/${name_channel}">
						<img class="chat-private-img" src="${photo_channel}" alt="profile picture">
						<h2 class="chat-category-pp">${name_channel}</h2>
					</a>
					<p class="chat-info-private">Private channel</p>
				`;
			} else {
				html += `
					<h2 class="chat-category">${name_channel}</h2>
					<p class="chat-info-private">Group channel</p>
				`;
			}

			// Display the messages
			let previousMessageSender = null;

			html += ` <div id="chat-log" class="chat-log">`;
			for (let message of Object.values(messages)) {
				let messageHTML = '';
				if (user.blockedUsers.includes(message.sender)) {
					messageHTML += `
						<p class="blocked-message">This user is blocked</p>
					`;
				} else {
					if (!room.private && message.sender != user.id) {
						if (previousMessageSender != message.sender) {
							messageHTML += `
								<p class="other-username">${message.username}</p>
							`;
						}
					}
					messageHTML += `
						${message.sender == user.id ? `
							<p class="my-message" data-sender="${message.sender}">
						` : `
							<p class="other-message" data-sender="${message.sender}">
						`}
						${message.message}
						</p>
					`;
				}
				previousMessageSender = message.sender;
				html += messageHTML;
			}
			html += `</div>`;
			
			// Display the chat buttons and close HTML
			html += `
				<br>
				<div class="chat-buttons">
					<input class="chat-message-input" id="chat-message-input" type="text" autocomplete="off">
					<input class="chat-message-submit" id="chat-message-submit" type="button" value="Send">
				</div>
			</div>
			`;

			// Display the page
			document.getElementById('app').innerHTML = html;

			// Call the websocket
			chatProcess(room_id, user.blockedUsers, room.private, user.id, user.username);
		});
	});
}