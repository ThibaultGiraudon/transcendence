function renderSignUpPage() {

	fetchAPI('/api/is_authenticated').then(data => {
		// If the user is already connected
		if (data.isAuthenticated) {
			document.getElementById('app').innerHTML = `
				<div class="already-log-in">
					<p class="log-in-message">You are already connected, please log out before creating a new user.</p>
					<a class="log-in-button" href="#" onclick="navigateTo(event, '/sign_out')">Sign out</a>
				</div>
			`;
		
		// If the user is not connected
		} else {

			// Generate the fields of the sign up form
			const fields = [
				{ name: 'username', label: 'Username', type: 'text' },
				{ name: 'email', label: 'Email', type: 'email' },
				{ name: 'password', label: 'Password', type: 'password' }
			];

			const fieldsHtml = fields.map(renderField).join('');

			// Display the sign up form
			document.getElementById('app').innerHTML = `
				<div class="form-div">
					<form method="POST" class="sign-form">
						<h3 class="sign-title">Sign up</h3>
						${fieldsHtml}
						<p class="error-message" id="error-message"></p>
						<input type="submit" value="Sign up"/>
					</form>
				</div>
			`;

			// Add an event listener on the sign-up form
			document.querySelector('.sign-form').addEventListener('submit', async function(event) {
				event.preventDefault();

				// Clear errors messages
				document.getElementById('error-username').textContent = '';
				document.getElementById('error-email').textContent = '';
				document.getElementById('error-password').textContent = '';
				document.getElementById('error-message').textContent = '';

				// Get data from the form
				const username = document.getElementById('username').value;
				const email = document.getElementById('email').value;
				const password = document.getElementById('password').value;

				// Validate the data
				if (!username) {
					document.getElementById('error-username').textContent = 'This field is required.';
					return;
				}
				if (!email) {
					document.getElementById('error-email').textContent = 'This field is required.';
					return;
				}
				if (!password) {
					document.getElementById('error-password').textContent = 'This field is required.';
					return;
				}

				// Send data to the server
				const response = await fetch('/sign_in/', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'X-CSRFToken': csrfToken
					},
					body: JSON.stringify({ username, email, password })
				});

				if (response.headers.get('content-type').includes('application/json')) {
					const responseData = await response.json();

					if (responseData.success) {
						// Update the header
						renderHeader();

						// Redirect the user
						router.navigate('/users/');
					
					} else {
						// If the connection failed, display the error message
						document.getElementById('error-username').textContent = responseData.username;
						document.getElementById('error-email').textContent = responseData.email;
						document.getElementById('error-password').textContent = responseData.password;
						document.getElementById('error-message').textContent = responseData.message;
					}

				} else {
					document.getElementById('error-message').textContent = "The server did not return a JSON response.";
				}
			});
		}
	})
}
