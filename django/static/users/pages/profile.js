function renderProfile(user) {
	return `
		<div class="profile">
			<img class="profile-img" src="${user.photo_url}" alt="profile picture">
			<div class="profile-infos">
				<p class="profile-username">${user.username}</p>
				<p class="profile-email">${user.email}</p>
			</div>
		</div>
	`;
}


function renderForm(fieldsHtml) {
	return `
		<div class="form-div">
			<form class="sign-form" method="POST" enctype="multipart/form-data" novalidate>
				<h3 class="sign-title">Edit informations</h3>
				${fieldsHtml}
				<p class="error-message" id="error-message"></p>
				<input type="submit" value="Accept modifications"/>
			</form>
		</div>
	`;
}


function renderSignOutButton() {
	return `<button class="profile-button" id="sign-out">Sign out</button>`;
}


function renderProfilePage(username) {

	fetchAPI('/api/isAuthenticated').then(data => {
		// If the user is already connected
		if (data.isAuthenticated) {

			// Get the user
			fetchAPI('/api/get_user/' + username).then(data => {
				if (data.user) {
					const user = data.user;

					const fields = [
						{ name: 'input-username', label: 'Username', type: 'text', value: user.username },
						{ name: 'input-photo', label: 'Profile picture', type: 'file', accept: 'image/*' },
					];

					const fieldsHtml = fields.map(renderField).join('');
							
					// Display the current user's informations
					if (data.isCurrentUser) {
						const fieldsHtml = fields.map(renderField).join('');
						const profileHtml = renderProfile(user);
						const formHtml = renderForm(fieldsHtml);
						const signOutButtonHtml = renderSignOutButton();

						document.getElementById('app').innerHTML = `
							${profileHtml}
							${formHtml}
							${signOutButtonHtml}
						`;

						// Add an event listener on the sign-in form
						document.querySelector('.sign-form').addEventListener('submit', async function(event) {
							event.preventDefault();

							// Clear errors messages
							document.getElementById('error-input-username').textContent = '';
							document.getElementById('error-input-photo').textContent = '';

							// Get data from the form
							const new_username = document.getElementById('input-username').value;
							const photo = document.getElementById('input-photo').files[0];

							// Validate the data
							if (!new_username) {
								document.getElementById('error-input-username').textContent = 'This field is required.';
								return;
							}

							// Convert the photo to a Base64 string
							let photoBase64 = null;
							if (photo) {
								const reader = new FileReader();
								reader.readAsDataURL(photo);

								// Wait for the photo to be converted to Base64
								await new Promise(resolve => {
									reader.onloadend = function() {
										photoBase64 = reader.result.replace('data:', '').replace(/^.+,/, '');
										resolve();
									}
								});
							}

							// Send data to the server
							const response = await fetch('/profile/' + user.username, {
								method: 'POST',
								headers: {
									'X-Requested-With': 'XMLHttpRequest',
									'X-CSRFToken': getCookie('csrftoken'),
								},
								body: JSON.stringify({ new_username, photo: photoBase64 })
							});

							if (response.headers.get('content-type').includes('application/json')) {
								const responseData = await response.json();

								if (responseData.success) {
									renderHeader();
									router.navigate('/profile/' + new_username);
	
								} else {
									// If the connection failed, display the error message
									document.getElementById('error-input-username').textContent = responseData.username;
									document.getElementById('error-input-photo').textContent = responseData.photo;
									document.getElementById('error-message').textContent = responseData.message;
								}
							
							} else {
								document.getElementById('error-message').textContent = "The server did not return a JSON response.";
							}
						});

						// Add an event listener on the sign-out button
						document.getElementById('sign-out').addEventListener('click', async function(event) {

							// Logout the user
							fetchAPI('/api/sign_out').then(data => {
								renderHeader();
								SignOutProcess(user.id);

								router.navigate('/sign_in/');
								return ;
							});
						});
					
					// Display the user's informations
					} else {
						fetchAPI('/api/get_user').then(data => {
							// If the user is not connected
							if (!data.user) {
								router.navigate('/sign_in/');
								return;
							}

							const currentUser = data.user;

							// Get the room
							let room = null;
							if (currentUser.channels) {
								for (channel of Object.values(currentUser.channels)) {
									if (channel.private && user.id in channel.users && currentUser.id in channel.users) {
										room = channel.room_id;
										break;
									}
								}
							}


							// Generate the profile page HTML
							let html = `
								<div class="profile">
									<img class="profile-img" src="${user.photo_url}" alt="profile picture">
									<div class="profile-infos">
										<p class="profile-username">${user.username}</p>
									</div>
								</div>
							`;

							if (currentUser.blockedUsers.includes(user.id)) {
								html += `
									<button class="profile-button unblock" data-user-id="${user.id}">
										Unblock
									</button>
									<p class="profile-blocked">You can't send a chat or follow this user</p>
								`;
							} else {
								html += '<div class="profile-actions">';
								if (currentUser.follows.includes(user.id)) {
									html += `
										<button class="profile-button unfollow" data-user-id="${user.id}">
											Unfollow
										</button>
									`;
								} else {
									html += `
										<button class="profile-button follow" data-user-id="${user.id}">
											Follow
										</button>
									`;
								}
								if (room) {
									html += `
										<button class="profile-button" data-route="/chat/${room}">
											Send a chat
										</button>
									`;
								} else {
									html += `
										<button class="profile-button">
											Send a chat
										</button>
									`;
								}
								html += `
										<button class="profile-button block" data-user-id="${user.id}">
											Block
										</button>
									</div>`;
							}

							// Display the profile page
							document.getElementById('app').innerHTML = html;

							// Add an event listener on the send a chat button
							const sendChatButton = document.querySelector('.profile-button.chat');
							if (sendChatButton) {
								sendChatButton.addEventListener('click', async function(event) {
									// Create the chat
									fetchAPI('/api/create_channel?user_ids=' + user.id + '&user_ids=' + currentUser.id + '&private=True').then(data => {
										router.navigate('/chat/' + data.room_id);
										return ;
									});
								});
							}
							
							// Add an event listener on the follow button
							const followButton = document.querySelector('.profile-button.follow');
							if (followButton) {
								followButton.addEventListener('click', async function(event) {
									// Follow the user
									fetchAPI('/api/follow/' + event.target.dataset.userId).then(data => {
										router.navigate('/profile/' + user.username);
										return ;
									});
								});
							}

							// Add an event listener on the unfollow button
							const unfollowButton = document.querySelector('.profile-button.unfollow');
							if (unfollowButton) {
								unfollowButton.addEventListener('click', async function(event) {
									// Unfollow the user
									fetchAPI('/api/unfollow/' + event.target.dataset.userId).then(data => {
										router.navigate('/profile/' + user.username);
										return ;
									});
								});
							}

							// Add an event listener on the block button
							const blockButton = document.querySelector('.profile-button.block');
							if (blockButton) {
								blockButton.addEventListener('click', async function(event) {
									// Block the user
									fetchAPI('/api/block/' + event.target.dataset.userId).then(data => {
										router.navigate('/profile/' + user.username);
										return ;
									});
								});
							}

							// Add an event listener on the unblock button
							const unblockButton = document.querySelector('.profile-button.unblock');
							if (unblockButton) {
								unblockButton.addEventListener('click', async function(event) {
									// Unblock the user
									fetchAPI('/api/unblock/' + event.target.dataset.userId).then(data => {
										router.navigate('/profile/' + user.username);
										return ;
									});
								});
							}
						})
					}

				// If the user does not exist
				} else {
					router.navigate('/users/');
				}
			})
		
		// If the user is not connected
		} else {
			router.navigate('/sign_in/');
		}
	})
}