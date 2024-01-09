/*
	I swear that I almost died trying to make this work.
	For the love of god, don't touch it,
											 Leon Pupier
*/


// --------------------------------------------------------------------------------
// ---------------------------------- Cookies -------------------------------------
// --------------------------------------------------------------------------------


// Return the value of the given cookie name (from the offical Django documentation)
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


// Get the CSRF token from the cookie
let csrfToken = getCookie('csrftoken');


// --------------------------------------------------------------------------------
// ----------------------------- Navigation & Routing -----------------------------
// --------------------------------------------------------------------------------


// When the user clicks on a link, navigate to the given route
async function navigateTo(event, route) {
	event.preventDefault();

	try {
		const response = await fetch(route, {
			method: 'GET',
			headers: {
				'X-Requested-With': 'XMLHttpRequest',
				'X-CSRFToken': csrfToken
			},
			credentials: 'same-origin'
		});
	
		const data = await response.json();

		if (data.redirect) {
			navigateTo(event, data.redirect);
		} else if (data.html) {
			document.querySelector('#page-content').innerHTML = data.html;
			if (data.header) {
				document.querySelector('#header').innerHTML = data.header;
			}
			csrfToken = getCookie('csrftoken');
		} else {
			if (data.header) {
				document.querySelector('#header').innerHTML = data.header;
			}
		}
	} catch (error) {}

	history.pushState(null, null, route);
}


// --------------------------------------------------------------------------------
// -------------------------------- Form listeners --------------------------------
// --------------------------------------------------------------------------------


// Handle form submission
async function handleFormSubmit(event) {
	event.preventDefault();

	let formData = new FormData(event.target);

	let fetchOptions = {
		method: 'POST',
		body: formData,
		headers: {
			'X-Requested-With': 'XMLHttpRequest',
			'X-CSRFToken': csrfToken
		},
		credentials: 'same-origin'
	};

	try {
		const data = await fetch(event.target.action, fetchOptions);
		const jsonData = await data.json();

		if (jsonData.success) {
			if (jsonData.redirect) {
				navigateTo(event, jsonData.redirect);
			} else if (jsonData.html) {
				document.querySelector('#page-content').innerHTML = jsonData.html;
				if (jsonData.header) {
					document.querySelector('#header').innerHTML = jsonData.header;
				}
				csrfToken = getCookie('csrftoken');
			}
		} else {
			for (const field in jsonData.errors) {
				const errorElement = document.querySelector(`#error-${field}`);
				if (errorElement) {
					errorElement.textContent = jsonData.errors[field][0].message;
				}
			}
		}

	} catch (error) {}
}


// --------------------------------------------------------------------------------
// ---------------------------------- Event listeners -----------------------------
// --------------------------------------------------------------------------------


// When the user navigates back or forward in the browser history
window.addEventListener('popstate', async function(event) {
	const currentUrl = window.location.pathname;
	
	try {
		const response = await fetch(currentUrl, {
			method: 'GET',
			headers: {
				'X-Requested-With': 'XMLHttpRequest'
			},
			credentials: 'same-origin'
		});
	
		const data = await response.json();
		document.querySelector('#page-content').innerHTML = data.html;
		if (data.header) {
			document.querySelector('#header').innerHTML = data.header;
		}
	} catch (error) {}
});


// When the user submits a form
document.addEventListener('submit', function(event) {
	const target = event.target;
	if (target && target.matches('form')) {
		handleFormSubmit(event);
	}
}, true);