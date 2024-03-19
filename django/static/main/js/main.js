// --------------------------------------------------------------------------------
// ------------------------------------- API --------------------------------------
// --------------------------------------------------------------------------------


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
// ----------------------------------- Status -------------------------------------
// --------------------------------------------------------------------------------


fetchAPI('/api/change_status/online').then(data => {});


function sendDisconnectSignal() {
	fetchAPI('/api/change_status/offline').then(data => {
		if (data.user_id) {
			changeStatus(data.user_id, 'offline');
		}
	});
}

function handleVisibilityChange() {
	if (document.hidden) {
		sendDisconnectSignal();
	} else {
		fetchAPI('/api/change_status/online').then(data => {
			if (data.user_id) {
				changeStatus(data.user_id, 'online');
			}
		});
	}
}

document.addEventListener("visibilitychange", handleVisibilityChange, false);


// --------------------------------------------------------------------------------
// ----------------------------------- Router -------------------------------------
// --------------------------------------------------------------------------------

let isPopStateEvent = false;

// Create a new router
const router = {

	routes: {
		// Main
		'/': renderChooseModePage,
		'/ken/': renderKenPage,

		// User
		'/sign_in/': renderSignInPage,
		'/sign_up/': renderSignUpPage,
		'/reset_password/': renderResetPasswordPage,
		'/reset_password_id/:resetPasswordID': renderResetPasswordIDPage,
		'/profile/:username': renderProfilePage,
		'/friends/': renderFriendsPage,

		// Pong
		'/pong/': renderChooseModePage,
		'/pong/ranked/': renderRankedPage,
		'/pong/practice/': renderPracticePage,
		'/pong/wait_players/:gameMode': renderWaitPlayers,
		'/pong/game/:gameMode': renderGamePage,
		'/pong/game_over/:gameID': renderGameOverPage,

		// Chat
		'/chat/': renderChatPage,
		'/chat/new/': renderNewRoomPage,
		'/chat/:id': renderRoomPage,

		// Notifications
		'/notifications/': renderNotificationsPage,

		// Stats
		'/ranking/:sortedBy': renderRankingPage,

		// Errors handling
		'/token42/': renderToken42Page,
		'/down42/': renderDown42Page,
		'/used42/': renderUsed42Page,
		'/auth42/': renderAuth42Page,
	},

	navigate: function(route) {
		// Check if the route is a string
		if (typeof route !== 'string') {
			return;
		}

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
			
			// Add the new route to the history
			if (!isPopStateEvent) {
				history.pushState({ route: route }, '', route);
			}
			isPopStateEvent = false;
		
		} else {
			// If no route is found, render the 404 page
			render404Page();
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


// --------------------------------------------------------------------------------
// ----------------------------- Navigation & Routing -----------------------------
// --------------------------------------------------------------------------------


// When the user clicks on a link, navigate to the given route
async function navigateTo(event, route) {
	event.preventDefault();
	router.navigate(route);
	renderHeader();
}


// Handle the navigation when the user clicks on a link
document.addEventListener('click', function(event) {
	let target = event.target;
	while (target !== document) {
		if (!target) return;
		if ((target.tagName === 'BUTTON' || target.tagName === 'A') && !target.hasAttribute('data-ignore-click')) {
			event.preventDefault();
			navigateTo(event, target.getAttribute('data-route'));
			return;
		}
		target = target.parentNode;
	}
});


// Handle the navigation when the user clicks on the back or forward button
window.addEventListener('popstate', function(event) {
	if (event.state && event.state.route) {
		isPopStateEvent = true;
		router.navigate(event.state.route);
	}
});


// --------------------------------------------------------------------------------
// ------------------------------------ Utils -------------------------------------
// --------------------------------------------------------------------------------


function renderField(field) {
	return `
		<label for="${field.name}">${field.label}</label>
		<div class="input-container">
			<input type="${field.type}" id="${field.name}" name="${field.name}" autocomplete="on" value="${field.value || ''}" accept="${field.accept || ''}" ${field.disabled ? 'disabled' : ''}/>
			${field.type === 'password' ?
				`<button data-ignore-click type="button" class="show-password" id="show-${field.name}">
					<img class="img-password" src="/static/users/img/eye_close.png" alt="Show/Hide"/>
				</button>`
			: ''}
		</div>
		<p class="error-alert" id="error-${field.name}"></p>
	`;
}


/* change the visibility of a password field */
document.addEventListener('click', function(event) {
	if (event.target.classList.contains('show-password')) {
		const input = event.target.previousElementSibling;
		if (input.type === 'password') {
			input.type = 'text';
			event.target.firstElementChild.src = '/static/users/img/eye_open.png';
		} else {
			input.type = 'password';
			event.target.firstElementChild.src = '/static/users/img/eye_close.png';
		}
	}
});


// --------------------------------------------------------------------------------
// ---------------------------------- Observer ------------------------------------
// --------------------------------------------------------------------------------

window.addEventListener('DOMContentLoaded', (event) => {
	router.navigate(window.location.pathname);
	renderHeader();

	// Generate a new CSRF token if it doesn't exist
	if (!getCookie('csrftoken')) {
		fetch('/api/generate_csrf_token/', {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
			},
		})
		.then(response => response.json())
		.then(data => {
			document.cookie = `csrftoken=${data.token};path=/`;
		});
	} 
});