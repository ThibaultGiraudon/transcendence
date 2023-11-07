FROM	nginx:latest

# SSL certificate
RUN		openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
		-keyout etc/ssl/private/server.key -out etc/ssl/certs/server.crt \
		-subj "/C=FR/L=Lyon/O=42/OU=ezanotti/CN=ezanotti.42.fr"

# Copy index.html file
RUN		rm -rf /var/www/html
RUN		mkdir -p /var/www/html
RUN		chown -R 755 /var/www/html
# COPY	./html/* /var/www/html/

# Copy nginx.conf file
COPY	./conf/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE	80
EXPOSE	443