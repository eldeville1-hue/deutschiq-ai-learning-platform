#!/bin/sh
set -eu

echo "Applying database migrations..."
alembic upgrade head
echo "Synchronizing validated curriculum..."
python seed_30_day_plan.py
echo "Starting DeutschIQ API..."
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8080}"
