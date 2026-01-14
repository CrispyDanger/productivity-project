#!/bin/sh

set -e

python manage.py migrate --noinput

python manage.py collectstatic --noinput

hypercorn -b 0.0.0.0:8000 -w 2 productivity-app.asgi:application
