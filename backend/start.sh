#!/bin/sh
set -eu

echo "Applying database migrations..."
alembic upgrade head
python -m scripts.verify_migration_head
echo "Synchronizing validated curriculum..."
python seed_30_day_plan.py
echo "Checking persisted curriculum answer quality..."
python -m scripts.audit_curriculum_answers --json || echo "Curriculum audit could not complete; API startup will continue."
echo "Starting DeutschIQ API..."
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8080}"
