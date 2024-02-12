FROM	python:3.11.4-slim-buster

# Set work directory
WORKDIR	/usr/src/app

ENV		PYTHONDONTWRITEBYTECODE 1
ENV		PYTHONUNBUFFERED 1

# Install system dependencies
RUN		apt-get update && \
		apt-get install -y --no-install-recommends gcc netcat && \
		apt-get clean && \
		rm -rf /var/lib/apt/lists/*

# Install python dependencies
RUN		pip install --upgrade pip
COPY	./requirements.txt .
RUN		pip install --no-cache-dir -r requirements.txt

# Create working directories
RUN		mkdir -p /home/app
ENV		APP_HOME=/home/app/web
RUN		mkdir $APP_HOME
WORKDIR	$APP_HOME

# Copy the script
COPY	./start-backend.sh .
RUN		chmod +x $APP_HOME/start-backend.sh

# Copy project
COPY	. $APP_HOME

# Run the start script
ENTRYPOINT ["/home/app/web/start-backend.sh"]