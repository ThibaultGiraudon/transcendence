FROM	python:3.8
EXPOSE	8000

# Set the working directory
WORKDIR	/usr/src/app/

# Install dependencies
COPY	./requirements.txt ./
RUN		pip install --no-cache -r requirements.txt

# Copy the project
COPY	./ ./

# Apply Django migrations
# TODO 
RUN		python pong_game/manage.py makemigrations --noinput
# RUN		python pong_game/manage.py migrate --noinput

# Run the project
CMD		["python", "pong_game/manage.py", "runserver", "0.0.0.0:8000"]