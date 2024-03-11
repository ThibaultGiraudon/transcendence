function renderResetPasswordIDPage() {
	fetchAPI('/api/isAuthenticated').then(data => {
		// If the user is already connected
		if (data.isAuthenticated) {
			document.getElementById('app').innerHTML = `
				<div class="already-log-in">
					<p class="log-in-message">You are already connected, please logout before reset a password.</p>
					<button class="log-in-button" id="sign-out">Sign out</button>
				</div>
			`;

			// Add an event listener on the sign-out button
			document.getElementById('sign-out').addEventListener('click', async function(event) {

				// Logout the user
				fetchAPI('/api/sign_out').then(data => {
					renderHeader();
					
					router.navigate('/sign_in/');
					return ;
				});
			});
		
		// If the user is not connected
		} else {

			// Generate the fields of the sign in form
			const fields = [
				{ name: 'password', label: 'New password', type: 'password' },
				{ name: 'password-confirmation', label: 'Password confirmation', type: 'password' },
			];

			const fieldsHtml = fields.map(renderField).join('');

			// Display the sign in form
			document.getElementById('app').innerHTML = `
				<div class="all-screen">
					<div class="form-div">
						<form method="POST" class="sign-form">
							<h3 class="sign-title">New password</h3>
							${fieldsHtml}
							<p class="error-message" id="error-message"></p>
							<input type="submit" value="Change your password"/>
						</form>
					</div>
				</div>
			`;

			// Add an event listener on the sign-in form
			document.querySelector('.sign-form').addEventListener('submit', async function(event) {
				event.preventDefault();

				// Clear errors messages
				document.getElementById('error-password').textContent = '';
				document.getElementById('error-password-confirmation').textContent = '';

				// Get data from the form
				const password = document.getElementById('password').value;
				const passwordConfirmation = document.getElementById('password-confirmation').value;

				// Validate the data
				if (!password) {
					document.getElementById('error-password').textContent = 'This field is required.';
					return;
				}
				if (!passwordConfirmation) {
					document.getElementById('error-password-confirmation').textContent = 'This field is required.';
					return;
				}
				if (password !== passwordConfirmation) {
					document.getElementById('error-password-confirmation').textContent = 'The password confirmation does not match the password.';
					return;
				}

				// Send data to the server
				const response = await fetch('/reset_password_id/' + window.location.pathname.split('/')[2], {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'X-CSRFToken': getCookie('csrftoken'),
					},
					body: JSON.stringify({ password })
				});

				if (response.headers.get('content-type').includes('application/json')) {
					const responseData = await response.json();

					if (responseData.success) {
						// Update the header
						renderHeader();

						// Redirect the user
						router.navigate('/sign_in/');
						return ;
					
					} else {
						document.getElementById('error-password').textContent = responseData.password;
						document.getElementById('error-password-confirmation').textContent = responseData.passwordConfirmation;
						document.getElementById('error-message').textContent = responseData.message;
					}

				} else {
					document.getElementById('error-message').textContent = "The server encountered an unexpected error.";
				}
			});
		}
	})
}