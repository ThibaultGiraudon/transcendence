function navigateTo(event, route) {
  // Empêche le comportement par défaut du lien
  console.log('navigateTo', route);
  event.preventDefault();

  // Utilisez fetch() ou toute autre méthode pour récupérer le contenu de la route
  // et mettez à jour le contenu du conteneur principal
//   fetch(route)
//     .then(response => response.text())
//     .then(html => {
//       document.getElementById('app').innerHTML = html;
//     });

//   // Facultatif : Mettez à jour l'URL du navigateur
//   history.pushState(null, null, route);
}
