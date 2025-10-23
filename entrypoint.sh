#!/usr/bin/env bash
set -euo pipefail

# Default to production if ENVIRONMENT is not set
ENVIRONMENT="${ENVIRONMENT:-production}"
export PORT="${PORT:-8000}"

if [ "$ENVIRONMENT" = "development" ]; then
  export DJANGO_SETTINGS_MODULE=core.settings.local
  echo "Running in DEVELOPMENT mode"

  echo "Running migrations..."
  python manage.py migrate --noinput

  echo "Starting Django dev server on 0.0.0.0:${PORT}"
  exec python manage.py runserver 0.0.0.0:${PORT}

elif [ "$ENVIRONMENT" = "production" ]; then
  export DJANGO_SETTINGS_MODULE=core.settings.production
  echo "Running in PRODUCTION mode (PORT=$PORT)"

  echo "Running migrations..."
  python manage.py migrate --noinput

  echo "Collecting static..."
  python manage.py collectstatic --noinput


  WORKERS="${WEB_CONCURRENCY:-2}"
  THREADS="${GUNICORN_THREADS:-2}"
  TIMEOUT="${GUNICORN_TIMEOUT:-60}"
  KEEPALIVE="${GUNICORN_KEEPALIVE:-5}"
  GRACEFUL="${GUNICORN_GRACEFUL_TIMEOUT:-30}"

  echo "Starting Gunicorn on 0.0.0.0:${PORT} (workers=$WORKERS threads=$THREADS)"
  exec gunicorn core.wsgi:application \
    --bind 0.0.0.0:${PORT} \
    --workers "$WORKERS" \
    --threads "$THREADS" \
    --timeout "$TIMEOUT" \
    --graceful-timeout "$GRACEFUL" \
    --keep-alive "$KEEPALIVE" \
    --log-level info
else
  echo "Unknown ENVIRONMENT: $ENVIRONMENT"
  exit 1
fi
