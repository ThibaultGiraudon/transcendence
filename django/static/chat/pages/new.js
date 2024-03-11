function renderNewRoomPage() {

	// If the user is not connected
	fetchAPI('/api/isAuthenticated').then(data => {
		if (!data.isAuthenticated) {
			router.navigate('/sign_in/');
			return;
		}
	});
		
	// Generate the fields for the channel creation form
	const fields = [
		{ name: 'input-group-name', label: 'Name (required)', type: 'text' },
		{ name: 'input-group-description', label: 'Description', type: 'text' },
	];

	const fieldsHtml = fields.map(renderField).join('');

	// Display the form
	document.getElementById('app').innerHTML = `
		<div class="all-screen">
			<div class="form-div">
				<form method="POST" class="sign-form">
					<h3 class="sign-title">New chat group</h3>
					${fieldsHtml}
					<p class="error-message" id="error-message"></p>
					<input type="submit" value="Create"/>
				</form>
			</div>
		</div>
	`;

	// Add the event listener to the form
	document.querySelector('.sign-form').addEventListener('submit', async function(event) {
		event.preventDefault();

		// Clear errors messages
		document.getElementById('error-input-group-name').textContent = '';
		document.getElementById('error-input-group-description').textContent = '';
		document.getElementById('error-message').textContent = '';

		// Get data
		const name = document.getElementById('input-group-name').value;
		const description = document.getElementById('input-group-description').value;

		// Send data to the server
		const response = await fetch('/chat/new/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': getCookie('csrftoken'),
			},
			body: JSON.stringify({ name, description })
		});

		if (response.headers.get('content-type').includes('application/json')) {
			const responseData = await response.json();

			if (responseData.success) {
				// Redirect the user
				router.navigate('/chat/' + responseData.room_id);
				return ;
			
			} else {
				document.getElementById('error-input-group-name').textContent = responseData.name;
				document.getElementById('error-input-group-description').textContent = responseData.description;
				document.getElementById('error-message').textContent = responseData.message;
			}

		} else {
			document.getElementById('error-message').textContent = "The server encountered an unexpected error.";
		}
	});
}