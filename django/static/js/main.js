function navigateTo(event, route) {
	console.log('navigateTo', route);
	event.preventDefault();

	fetch(route)
		.then(response => response.text())
		.then(html => {
		document.getElementById('app').innerHTML = html;
	});

	history.pushState(null, null, route);
}

window.addEventListener('popstate', function(event) {
	const currentUrl = window.location.pathname;
	fetch(currentUrl)
		.then(response => response.text())
		.then(html => {
		document.getElementById('app').innerHTML = html;
	});
});