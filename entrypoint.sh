#!/bin/sh

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Start the Django development server
exec "$@"
