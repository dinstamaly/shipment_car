#!/bin/sh
until cd /app/backend
do
    echo "Waiting for server volume..."
done
python manage.py migrate
python load_data.py

python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000

