#!/bin/bash
set -e

function postgres_ready(){
python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(dbname="$POSTGRES_DB", user="$POSTGRES_USER", password="$POSTGRES_PASSWORD", host="postgres")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - continuing..."

export DATABASE_URL=postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@postgres:5432/$POSTGRES_DB

export DJANGO_SETTINGS_MODULE=flight.settings.$ENV
cd /app
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn flight.wsgi:application \
    --name flights_django \
    --bind 0.0.0.0:8080 \
    --workers 5
