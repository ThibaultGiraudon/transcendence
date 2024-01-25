// --------------------------------------------------------------------------------
// ---------------------------------- Router --------------------------------------
// --------------------------------------------------------------------------------


// Create a new router
const router = {

	routes: {
		// Main
		'/': renderChooseModePage,
		'/ken/': renderKenPage,

		// User
		'/sign_in/': renderSignInPage,
		'/sign_up/': renderSignUpPage,
		'/profile/:username': renderProfilePage,
		'/users/': renderUsersPage,

		// Pong
		'/pong/': renderChooseModePage,

		// Chat

		// Notifications

		// Errors
	},

	navigate: function(route) {
		// Find the matching route
		const matchingRoute = Object.keys(this.routes).find(r => {
			const regex = new RegExp(`^${r.replace(/:[^\s/]+/g, '([\\w-]+)')}$`);
			return regex.test(route);
		});
	
		if (matchingRoute) {
			// Extract the parameters
			const params = route.match(new RegExp(matchingRoute.replace(/:[^\s/]+/g, '([\\w-]+)'))).slice(1);
	
			// Call the corresponding function with the parameters
			this.routes[matchingRoute](...params);
			history.pushState({}, '', route);
		}
	}
};


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
	router.navigate(route);
}


// Handle the navigation when the user clicks on a link
document.addEventListener('click', function(event) {
	let target = event.target;
	while (target !== document) {
		if ((target.tagName === 'BUTTON' || target.tagName === 'A') && !target.hasAttribute('data-ignore-click')) {
			event.preventDefault();
			navigateTo(event, target.getAttribute('data-route'));
			return;
		}
		target = target.parentNode;
	}
});


// --------------------------------------------------------------------------------
// ---------------------------------- Event listeners -----------------------------
// --------------------------------------------------------------------------------


// When the user navigates back or forward in the browser history
// window.addEventListener('popstate', async function(event) {
// 	const currentUrl = window.location.pathname;
	
// 	try {
// 		const response = await fetch(currentUrl, {
// 			method: 'GET',
// 			headers: {
// 				'X-Requested-With': 'XMLHttpRequest'
// 			},
// 			credentials: 'same-origin'
// 		});
	
// 		const data = await response.json();
// 		document.querySelector('#page-content').innerHTML = data.html;
// 		if (data.header) {
// 			document.querySelector('#header').innerHTML = data.header;
// 		}
// 	} catch (error) {}
// });


// --------------------------------------------------------------------------------
// ------------------------------------ Utils -------------------------------------
// --------------------------------------------------------------------------------


function renderField(field) {
	return `
		<label for="${field.name}">${field.label}</label>
		<input type="${field.type}" id="${field.name}" name="${field.name}" autocomplete="on" value="${field.value || ''}" accept="${field.accept || ''}"/>
		<div class="error-alert" id="error-${field.name}"></div>
	`;
}


function fetchAPI(url) {
	return fetch(url, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
		},
	})
	.then(response => response.json());
}


// --------------------------------------------------------------------------------
// ---------------------------------- Observer ------------------------------------
// --------------------------------------------------------------------------------


const elementsToProcess = {
	'chat-log': chatProcess,
	'pong_game': gameProcess,
	'sign-out': SignOutProcess,
	'set-status-online': SignInProcess
};


function handleMutation() {
	for (let id in elementsToProcess) {
		const element = document.getElementById(id);
		if (element) {
			elementsToProcess[id]();
			delete elementsToProcess[id];
		}
	}
}


const observer = new MutationObserver(handleMutation);
observer.observe(document, { childList: true, subtree: true });


window.addEventListener('DOMContentLoaded', (event) => {
	router.navigate(window.location.pathname);
	renderHeader();
});