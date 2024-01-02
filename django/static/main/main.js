// --------------------------------------------------------------------------------
// ----------------------------- Navigation & Routing -----------------------------
// --------------------------------------------------------------------------------

// Return the value of the given cookie name
function getCookie(name) {
	
	let cookieValue = null;

	if (document.cookie && document.cookie !== '') {
		const cookies = document.cookie.split(';');
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}

	return cookieValue;
}


// When the user clicks on a link, navigate to the given route
function navigateTo(event, route) {
	event.preventDefault();

	fetch(route, {
		headers: {
			'X-Requested-With': 'XMLHttpRequest'
		}
	})
	.then(response => {
		if (!response.ok) {
			throw new Error('Network response was not ok');
		}
		return response.json();
	})
	.then(data => {
		if (data.redirect) {
			window.location.href = data.redirect;
		} else if (data.html) {
			document.querySelector('#page-content').innerHTML = data.html;
		} else {
			console.error('Unexpected response:', data);
		}
	})
	.catch(error => {
		console.error('Error:', error);
	});

	history.pushState(null, null, route);
}


// Update the header menu of the website
function updateHeader() {
	fetch('/header_view/', {
		method: 'GET',
		headers: {
			'X-Requested-With': 'XMLHttpRequest',
			'Accept': 'application/json'
		}
	})
	.then(response => response.text())
	.then(data => {
		const header = document.querySelector('header');
		header.innerHTML = data;
	});
}


// --------------------------------------------------------------------------------
// -------------------------------- Form listeners --------------------------------
// --------------------------------------------------------------------------------


// Form submit handler
function handleFormSubmit(event) {
	event.preventDefault();

	const form = event.target;
	const formData = new FormData(form);

	sendRequest(form.action, form.method, formData)
		.then(handleResponse)
		.catch(handleError);
}


function sendRequest(url, method, formData) {
	return fetch(url, {
		method: method,
		body: new URLSearchParams(formData),
		headers: {
			'X-Requested-With': 'XMLHttpRequest',
			'X-CSRFToken': getCookie('csrftoken')
		},
		credentials: 'same-origin'
	}).then(response => response.json());
}


function handleResponse(data) {
	if (data.success) {
		if (data.redirect) {
			window.location.href = data.redirect;
		} else if (data.html) {
			document.querySelector('#page-content').innerHTML = data.html;
		}
	} else if (data.errors) {
		Object.keys(data.errors).forEach(field => {
			const errorDiv = document.querySelector(`#error-${field}`);
			if (errorDiv) {
				const errorMessages = data.errors[field].map(error => error.message);
				errorDiv.innerHTML = errorMessages.join(', ');
			} else {
				console.warn(`No error div found for field ${field}`);
			}
		});
	} else {
		console.error('Unexpected response:', data);
	}
}


function handleError(error) {
	console.error("Error:", error);
}


// --------------------------------------------------------------------------------
// ---------------------------------- Event listeners -----------------------------
// --------------------------------------------------------------------------------


// When the user navigates back or forward in the browser history
window.addEventListener('popstate', function(event) {
	const currentUrl = window.location.pathname;
	
	fetch(currentUrl, {
		headers: {
			'X-Requested-With': 'XMLHttpRequest'
		}
	})
	.then(response => response.json())
	.then(data => {
		document.querySelector('#page-content').innerHTML = data.html;
	});
});


// Add event listener to all forms
const forms = document.querySelectorAll('form');
forms.forEach(form => {
	form.addEventListener('submit', handleFormSubmit);
});