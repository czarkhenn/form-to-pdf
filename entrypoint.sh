#!/bin/bash

# Set Django settings module based on environment
if [ "$ENVIRONMENT" = "development" ] || [ -z "$ENVIRONMENT" ]; then
    export DJANGO_SETTINGS_MODULE=core.settings.local
    echo "Running in development mode"

    # Run migrations
    python manage.py migrate --noinput

    # Start development server with hot reload
    exec python manage.py runserver 0.0.0.0:${PORT:-8000}
else
    export DJANGO_SETTINGS_MODULE=core.settings.production
    echo "Running in production mode"

    # Run migrations
    python manage.py migrate --noinput

    # Collect static files
    python manage.py collectstatic --noinput

    # Start production server with gunicorn
    exec gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3 --threads 2
fi

