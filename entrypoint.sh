#!/bin/bash

# Set Django settings module based on environment
if [ "$ENVIRONMENT" = "development" ]; then
    export DJANGO_SETTINGS_MODULE=core.settings.local
    echo "Running in DEVELOPMENT mode"

    # Run migrations
    echo "Running Django migrations..."
    python manage.py migrate --noinput 2>&1 || { echo "Migration failed!"; exit 1; }

    # Start development server with hot reload
    echo "Starting Django development server on port ${PORT:-8000}"
    exec python manage.py runserver 0.0.0.0:${PORT:-8000}
elif [ "$ENVIRONMENT" = "production" ]; then
    export DJANGO_SETTINGS_MODULE=core.settings.production
    echo "Running in PRODUCTION mode"

    # Run migrations
    echo "Running Django migrations..."
    python manage.py migrate --noinput 2>&1 || { echo "Migration failed!"; exit 1; }

    # Collect static files
    echo "📁 Collecting static files..."
    python manage.py collectstatic --noinput 2>&1 || { echo "Static file collection failed!"; exit 1; }


    export PORT=${PORT:-8000}
    echo "Using PORT: $PORT"

    # Wait for server to be ready
    echo "Waiting 5 seconds for server startup..."
    sleep 5

    # Start production server with gunicorn
    echo "Starting Gunicorn server on 0.0.0.0:$PORT"
    exec gunicorn core.wsgi:application \
        --bind 0.0.0.0:$PORT \
        --workers 2 \
        --threads 2 \
        --log-level info \
else
    echo "Unknown ENVIRONMENT: $ENVIRONMENT"
    echo "Expected: development, production, or unset (defaults to production)"
    exit 1
fi

