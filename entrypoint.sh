#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py migrate

echo

if [ "$#" -eq 0 ]; then
  gunicorn proj.wsgi:application --bind 0.0.0.0:$PORT
else
  exec "$@"
fi