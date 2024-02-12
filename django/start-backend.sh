#!/bin/bash

if [ "$DATABASE_HOST" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py makemigrations mainApp
python manage.py migrate

if [ "$DEBUG" = "False" ]
then
    python manage.py collectstatic --noinput
    echo -e "\033[1;32m[SERVER] Production server is ready to accept connections...\033[0m"
    exec uvicorn mainProject.asgi:application --host 0.0.0.0 --port 8000 --log-level warning
else
    echo -e "\033[1;32m[SERVER] Development server is ready to accept connections...\033[0m"
    exec uvicorn mainProject.asgi:application --host 0.0.0.0 --port 8000 --reload
fi