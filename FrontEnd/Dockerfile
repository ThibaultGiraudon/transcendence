FROM	nginx:latest

EXPOSE	80
EXPOSE	443

COPY	./html /usr/share/nginx/html

RUN		mkdir -p /etc/nginx/ssl
RUN		openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
		-keyout /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt \
		-subj "/C=FR/L=Lyon/O=42/OU=ezanotti/CN=ezanotti.42.fr"

CMD		["nginx", "-g", "daemon off;"]