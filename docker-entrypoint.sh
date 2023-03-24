#!/bin/sh
python manage.py migrate
gunicorn jappl_staffclocker_backend.wsgi:application --bind 0.0.0.0:8000 --timeout 600 --preload
