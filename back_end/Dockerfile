# Use the official Python image as a base image
FROM python:3.8

# Set the working directory
WORKDIR /usr/src/app/

# Copy the requirements file into the container
COPY ./requirements.txt ./

# Install dependencies
RUN pip install --no-cache -r requirements.txt

# Copy the project files into the container
COPY ./pong_game/ ./

# Apply Django migrations
RUN python manage.py makemigrations --noinput
# RUN python pong_game/manage.py migrate --noinput

# Expose the port on which the application will run
EXPOSE 8000

# Command to run the application using Daphne
CMD ["daphne", "-u", "/tmp/daphne.sock", "pong_game.asgi:application"]