#!/bin/sh

#python manage.py migrate --no-input
#python manage.py collectstatic --no-input

gunicorn settings.wsgi:application --bind 0.0.0.0:8000 &

wait-for-it.sh -t 60 djangogunicorn:8000
wait-for-it.sh -t 60 rabbitmq:5672 -- celery -A settings worker -B -c 1 -l info