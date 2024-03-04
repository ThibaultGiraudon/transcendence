function renderResetPasswordPage() {
	fetchAPI('/api/isAuthenticated').then(data => {
		// If the user is already connected
		if (data.isAuthenticated) {
			document.getElementById('app').innerHTML = `
				<div class="already-log-in">
					<p class="log-in-message">You are already connected, you can change your password in your profile.</p>
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
				{ name: 'email', label: 'Email', type: 'email' },
			];

			const fieldsHtml = fields.map(renderField).join('');

			// Display the sign in form
			document.getElementById('app').innerHTML = `
				<div class="all-screen">
					<div class="form-div">
						<form method="POST" class="sign-form">
							<h3 class="sign-title">Reset password</h3>
							${fieldsHtml}
							<p class="error-message" id="error-message"></p>
							<input type="submit" value="Send the email"/>
						</form>
					</div>
				</div>
			`;

			// Add an event listener on the sign-in form
			document.querySelector('.sign-form').addEventListener('submit', async function(event) {
				event.preventDefault();

				// Clear errors messages
				document.getElementById('error-email').textContent = '';

				// Get data from the form
				const email = document.getElementById('email').value;

				// Validate the data
				if (!email) {
					document.getElementById('error-email').textContent = 'This field is required.';
					return;
				}

				// Send data to the server
				const response = await fetch('/reset_password/', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'X-CSRFToken': getCookie('csrftoken'),
					},
					body: JSON.stringify({ email })
				});

				if (response.headers.get('content-type').includes('application/json')) {
					const responseData = await response.json();

					if (responseData.success) {
						// Update the header
						renderHeader();

						// Display a message
						document.getElementById('error-message').textContent = "If the email provided is correct, you will receive a link to reset your password.";
						return ;
					
					} else {
						document.getElementById('error-email').textContent = responseData.email;
						document.getElementById('error-message').textContent = responseData.message;
					}

				} else {
					document.getElementById('error-message').textContent = "The server did not return a JSON response.";
				}
			});
		}
	})
}