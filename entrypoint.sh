#!/bin/sh
set -e

# Run database migrations
/app/.venv/bin/alembic upgrade head

# Start the application
exec uv run fastapi dev app.py --host 0.0.0.0 --port 8000
