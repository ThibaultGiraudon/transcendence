FROM	nginx:latest
EXPOSE	80
EXPOSE	443

# SSL certificate
RUN		openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
		-keyout etc/ssl/private/server.key -out etc/ssl/certs/server.crt \
		-subj "/C=FR/L=Lyon/O=42/OU=ezanotti/CN=ezanotti.42.fr"

# Copy nginx.conf file
COPY	./conf/nginx.conf /etc/nginx/conf.d/default.conf