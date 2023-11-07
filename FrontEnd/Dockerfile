# Utilisez l'image Nginx officielle en tant qu'image de base
FROM nginx:latest

# Copiez votre fichier de certificat SSL et votre clé privée (remplacez ces fichiers par les vôtres)
COPY ssl/server.crt /etc/ssl/certs/
COPY ssl/server.key /etc/ssl/private/

# Copiez votre fichier de configuration Nginx (remplacez-le par le vôtre)
COPY ./conf/nginx.conf /etc/nginx/conf.d/default.conf

# openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ssl/server.key -out ssl/server.crt -subj "/C=FR/L=Lyon/O=42/OU=ezanotti/CN=ezanotti.42.fr"
# Exposez les ports HTTP (80) et HTTPS (443)
EXPOSE 80
EXPOSE 443
