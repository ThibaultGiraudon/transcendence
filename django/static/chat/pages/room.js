function renderRoomPage(room_id) {

	fetchAPI('/api/get_user').then(dataUser => {

		// If the user is not connected
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
			const users = Object.values(room.users);
			if (users[0].id == user.id) {
				if (users[1].blocked) {
					router.navigate('/chat/');
					return;
				}
			} else {
				if (users[0].blocked) {
					router.navigate('/chat/');
					return;
				}
			}
		}

		// Get the messages
		fetchAPI(`/api/get_messages/${room_id}`).then(dataMessages => {
			fetchAPI('/api/change_status/chat:' + room_id).then(data => {});

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
						<h2 class="chat-category">Users</h2>
						
						<div class="list-participants">
							${Object.values(room.users).map(some_user => `
								<a data-route="/profile/${some_user.username}">
									<div class="participants-container">
										<img class="participants-img" src="${some_user.photo_url}" alt="profile picture">
										<h3 class="participants-username">
											${some_user.username}
											${some_user.id == room.creator ? '<span class="admin-text">👑</span>' : ''}
											${some_user.id == user.id ? '<span class="you-text">(You)</span>' : ''}
										</h3>
									</div>
								</a>
							`).join('')}
						</div>

						<input class="chat-add-user" id="chat-add-user" type="button" value="Add a user">
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
					<button class="invite-game-button">Play a game</button>
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
							if (message.sender == 0) {
								messageHTML += `
								<p class="system-username">${message.username}</p>`;
							}
							else {
								messageHTML += `
									<p class="other-username">${message.username}</p>
								`;
							}
						}
					}
					if (message.sender == user.id) {
						messageHTML += `
							<p class="my-message" data-sender="${message.sender}">`;
					}
					else if (message.sender == 0) {
						messageHTML += `
							<p class="system-message" data-sender="${message.sender}">`;
					}
					else {
						messageHTML += `
							<p class="other-message" data-sender="${message.sender}">`;
					}
					messageHTML += `
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
			document.getElementById('app').innerHTML = `
				<div class="all-screen">
					${html}
				</div>
			`;

			// Hide the button if the user is not the creator of the room
			const addUserButton = document.getElementById('chat-add-user');
			if (addUserButton) {
				if (room.creator != user.id) {
					addUserButton.style.display = 'none';
				}

				// Handle the click on the add user button
				addUserButton.addEventListener('click', async function(event) {

					// Get the list of users
					fetchAPI('/api/users').then(dataUsers => {
						if (!dataUsers.users) {
							return;
						}

						// Create the popup background
						let popupBackgroundHTML = '<div class="popup-background" id="popup-background"></div>';

						// Create the popup
						let popupHTML = `
							<div class="popup">
								<h3 class="title-popup">Select a user</h3>
						`;

						// Add each user to the popup
						let count_users = 0;
						for (const user of Object.values(dataUsers.users)) {
							if (!(user.id in room.users))
							{
								popupHTML += `
								<button class="add-user" data-user-id="${user.id}">
									<div class="container" data-user-id="${user.id}">
										<img class="users-img" src="${user.photo_url}" alt="profile picture">
										<p class="users-user">${user.username}</p>
									</div>
								</button>
								`;
								count_users++;
							}
						}

						// If there is no user to add
						if (count_users == 0) {
							popupHTML += `
								<p class="no-user-to-add">❌ No user to add</p>
							`;
						}

						popupHTML += `
								<button class="close-popup" id="close-popup">Close</button>
							</div>
						`;

						// Create the popup background and the popup
						let popupBackground = document.createElement('div');
						popupBackground.innerHTML = popupBackgroundHTML;
						document.body.appendChild(popupBackground);

						let popup = document.createElement('div');
						popup.innerHTML = popupHTML;
						document.body.appendChild(popup);

						// Add a click event listener to each user
						document.querySelectorAll('.add-user').forEach(user => {
							user.addEventListener('click', () => {
								const userId = user.getAttribute('data-user-id');

								// Add the user to the room
								fetchAPI(`/api/add_user_to_room/${room_id}/${userId}`, 'POST').then(data => {
									if (data.success) {
										send_message(room_id, 0, `${dataUser.user.username} added ${data.username} to the channel`);
										popup.remove();
										popupBackground.remove();
										renderRoomPage(room_id);
									}
								});
							});
						});

						// Handle the click on the close button
						document.getElementById('close-popup').addEventListener('click', () => {
							popup.remove();
							popupBackground.remove();
						});

						document.getElementById('popup-background').addEventListener('click', () => {
							popup.remove();
							popupBackground.remove();
						});
					});
				});
			}

			const inviteGameButton = document.querySelector('.invite-game-button');

			if (inviteGameButton) {
				inviteGameButton.addEventListener('click', () => {
					send_message(room_id, 0, `${dataUser.user.username} invited you to play a game`);
				});
			}

			// Call the websocket
			chatProcess(room_id, user.blockedUsers, room.private, user.id, user.username);
		});
	});
}

function send_message(room_id, sender, message) {
	let websocketProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
	let websocketPort = window.location.protocol === 'https:' ? ':8443' : ':8000';
	const socketUrl = websocketProtocol + '//' + window.location.hostname + websocketPort + '/ws/chat/' + room_id + "/";

	let tmpSocket

	tmpSocket = {
		socket: new WebSocket(socketUrl),
		url: socketUrl,
		shouldClose: false
	};

	tmpSocket.socket.onopen = function(event) {
		tmpSocket.socket.send(JSON.stringify({
			'message': message,
			'sender': sender,
			'username': 'System Info',
		}));
	};

	fetchAPI(`/api/create_invite_game/${room_id}`).then(data => {
		if (data.success) {
			console.log("dans fetch API create_invite_game");
			console.log(data);
			router.navigate('/pong/wait_players/init_ranked_solo_game');
		} else {
			
		}
	})
}