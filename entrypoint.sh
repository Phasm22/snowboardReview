#!/bin/sh
# entrypoint.sh

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Start the server
echo "Starting server..."
exec "$@"
