#!/bin/bash
# Probash Mart Backend - Server Startup Script
# Runs migrations, seeds data, and collects static files

set -e

echo "🔄 Running database migrations..."
python manage.py migrate --noinput

echo "🌱 Seeding initial data..."
python manage.py seed_data || echo "Seed data already exists, skipping..."

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Setup complete! Starting server..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --worker-class gthread \
    --threads 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
