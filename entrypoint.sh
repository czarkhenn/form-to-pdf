#!/bin/bash

# Set Django settings module based on environment
if [ "$ENVIRONMENT" = "development" ] || [ -z "$ENVIRONMENT" ]; then
    export DJANGO_SETTINGS_MODULE=core.settings.local
    echo "Running in development mode"

    # Run migrations
    echo "Running Django migrations..."
    python manage.py migrate --noinput || echo "Migration failed!"

    # Start development server with hot reload
    echo "Starting Django development server on port ${PORT:-8000}"
    exec python manage.py runserver 0.0.0.0:${PORT:-8000}
else
    export DJANGO_SETTINGS_MODULE=core.settings.production
    echo "Running in production mode"

    # Run migrations
    echo "Running Django migrations..."
    python manage.py migrate --noinput || echo "Migration failed!"

    # Collect static files
    echo "Collecting static files..."
    python manage.py collectstatic --noinput || echo "Static file collection failed!"

    export PORT=${PORT:-8000}
    echo "Using PORT: $PORT"

    echo "Waiting 3 seconds for server startup..."
    sleep 3

    # Start production server with gunicorn
    echo "Starting Gunicorn server..."
    exec gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --threads 2
fi

