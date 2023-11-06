# Utilisez l'image Nginx officielle en tant qu'image de base
FROM nginx:latest

# Copiez le contenu du site web local dans le conteneur
COPY ./html/ /usr/share/nginx/html

# Exposez le port 80 pour le trafic HTTP
EXPOSE 80

# Commande par défaut pour exécuter Nginx en arrière-plan
CMD ["nginx", "-g", "daemon off;"]
