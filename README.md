# Transcendence

> [!NOTE]  
> This project is still under development.
## Modules (A modifier)

-	**Major module**: Use a Framework as backend. (Django instead of Ruby)
-	**Major module**: Implementing a remote authentication.
-	**Major module**: Standard user management, authentication, users across
tournaments.
-	**Major module**: Multiplayers (more than 2 in the same game).
<!-- -	**Major module**: Add Another Game with User History and Matchmaking. -->
-	**Major module**: Live chat.
-	**Major module**: Introduce an AI Opponent.
-	**Major module**: Remote players.
-	(server side game)
-	minor (database with PostgreSQL)

## Technos Utilisées

-	**Front End**: 
	-	Html
	-	Css
	-	JavaScript
-	**Back End**:
	-	Django
-	**Database**:
	-	PostgreSQL

## Features (to do list)

-	Premier jeu fonctionnel (creer la base du jeu fonctionnel dabord sans DB avec JS)

## sh'est les modules ishi

Module majeur : Clavardage en direct
Vous devez créer un système de clavardage (chat) pour vos utilisateurs dans ce
module :
◦ L’utilisateur doit pouvoir envoyer des messages directs à d’autres utilisateurs.✅
◦ L’utilisateur doit pouvoir en bloquer d’autres. Ainsi, l’utilisateur ne verra plus
les messages provenant du compte qu’il a bloqué.✅
◦ L’utilisateur doit pouvoir inviter d’autres utilisateurs à jouer une partie de
Pong à partir de l’interface de Chat.
◦ Le système de tournoi doit pouvoir avertir les utilisateurs qui sont attendus
pour la prochaine partie.
◦ L’utilisateur doit pouvoir accéder aux profiles d’autres joueurs à partir de l’interface de Chat.✅


Module majeur : Joueurs multiples
Il est possible d’avoir plus de deux joueurs. Chaque joueur doit avoir ses propres
contrôles (donc, le module précédent "Joueurs à distance" est hautement recommandé). Il vous appartient de définir comment on peut jouer à 3, 4, 5, 6 ... joueurs.
En plus du jeu classique à 2 joueurs, vous pouvez choisir un nombre de joueurs
unique, supérieur à 2, pour ce module multijoueur. Par exemple, 4 joueurs peuvent
jouer sur un plateau carré, chaque joueur possédant un côté unique du carré.


Module majeur : Implémenter une authentification à distance.
Dans ce module majeur, le but est d’implémenter le système d’authentification
suivant : OAuth 2.0 authentication with 42 . Les fonctionnalités à inclure sont :
◦ Intégrer un système d’authentification permettant aux utilisateurs d’accéder
au site en toute sécurité.✅
◦ Obtenir les informations et permissions nécessaires de l’autorité afin d’activer
une authentification sécuritaire.✅
◦ Mettez en place des flux de connexion et d’autorisation conviviaux pour les
utilisateurs, conformes aux meilleures pratiques et normes de sécurité.✅
◦ Assurez-vous de l’échange sécurisé des jetons (tokens) d’authentification et des
informations de l’utilisateur entre l’application web et le fournisseur d’authentification.✅
Ce module majeur vise à obtenir une authentification distante de l’utilisateur,
procurant à celui-ci une façon simple et sécuritaire d’accéder à l’application web.


Module majeur : Gestion d’utilisateurs standard, authentification et utilisateurs
en tournois.
◦ Les utilisateurs peuvent s’inscrire au site web de manière sécuritaire.✅
◦ Les utilisateurs enregistrés peuvent s’authentifier de manière sécuritaire.✅
◦ Les utilisateurs peuvent choisir un nom d’affichage unique pour jouer en tournoi.✅
◦ Les utilisateurs peuvent mettre à jour leurs informations.✅
◦ Les utilisateurs peuvent téléverser un avatar, mais un avatar par défaut existe
si aucun n’est fourni.✅
◦ Les utilisateurs peuvent ajouter d’autres utilisateurs comme amis et voir leur
statut (en ligne / hors-ligne / en partie).✅
◦ Les profils d’utilisateurs affichent des statistiques, comme les victoires et défaites.
◦ Chaque utilisateur a un Historique des parties incluant les parties 1v1, les
dates et autres détails pertinents, accessibles aux utilisateurs authentifiés.


Module mineur : Utiliser une base de données pour le backend -et plus.✅
La base de données désignée pour toutes les instances de base de données
dans votre projet est PostgreSQL . Ce choix garantit la cohérence des données et
la compatibilité entre tous les composants du projet et peut être une condition
préalable pour d’autres modules, tels que le Module Framework backend.


Module majeur : Utiliser un Framework en backend.✅
Dans ce module majeur, vous devez utiliser un framework web spécifique pour
le développement de votre backend, et ce framework est Django .


• Module majeur : Adversaire contrôlé par IA.
Dans ce module majeur, l’objectif est d’incorporer un joueur contrôlé par Intelligence Artificielle (IA) dans le jeu. Notamment, l’utilisation d’un A* algorithm
n’est pas permise pour réaliser cette tâche. Les buts et fonctionnalités clés incluent :
◦ Développez un adversaire IA qui fournissent un défi et une expérience engageante aux utilisateurs.
◦ L’IA doit reproduire un comportement humain, signifiant que dans l’implémentation de votre IA, vous devez simuler les entrées au clavier. La contrainte
ici est que l’IA peut seulement rafraîchir sa vue du jeu une fois par seconde,
lui demandant donc d’anticiper les rebonds et autres actions.
L’IA doit pouvoir utiliser des bonus (power-ups) si vous avez choisi
d’implémenter le Module Option de personnalisation de jeu.
◦ Implémentez la logique de l’IA et le processus de décision qui permettent à
votre IA de faire des mouvements et décisions intelligentes et stratégiques.
◦ Explorer des algorithmes alternatifs et techniques afin de créer une IA efficace
sans utiliser A*.
◦ Assurer vous que l’IA s’adapte aux différents scénarios de gameplay et interactions utilisateurs.
Attention: Vous allez devoir expliquer en détails comment votre IA
fonctionne durant l’évaluation. Créer une IA qui ne fait rien est
strictement défendu. Elle doit pouvoir gagner des parties.
Ce module majeur vise à améliorer le jeu en introduisant un adversaire contrôlé
par Intelligence Artificielle qui ajoute des aspects excitants et compétitifs, tout en
n’utilisant pas l’Algorithme A*.


Module majeur : Joueurs à distance
Il est possible d’avoir 2 joueurs distants. Chaque joueur est sur un ordinateurs
différent, accédant au même site web et jouant la même partie de Pong.


• Module mineur : Étendre la compatibilité des navigateurs web.
Dans ce module mineur, l’objectif est d’améliorer la compatibilité de l’application web en ajoutant la compatibilité pour un navigateur web supplémentaire.
Cela inclue :
◦ Étendre le support navigateur afin d’inclure un navigateur supplémentaire,
s’assurant ainsi que les utilisateurs peuvent accéder l’application web sans problèmes.
◦ Effectuer des tests approfondis et des optimisations pour s’assurer que l’application web fonctionne correctement et s’affiche correctement dans le nouveau
navigateur pris en charge.
◦ Gérer et régler tout problème de compatibilité ou de rendu qui pourrait survenir
dans le nouveau navigateur.
◦ S’assurer d’une expérience utilisateur constante sur tous les navigateurs supportés, conservant l’usage et les fonctionnalités.//
Ce module mineur vise à élargir l’accessibilité de l’application web en supportant un navigateur additionnel, offrant ainsi plus de choix d’usage de l’application
par l’utilisateur.