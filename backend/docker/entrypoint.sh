#!/usr/bin/env sh

set -e  # Exit on any error

echo "=== Surveys Service Application Startup ==="

# Function to wait for database
wait_for_db() {
    echo "Waiting for database connection..."
    poetry run python -c "
import sys
import time
import os
from sqlalchemy import create_engine
from backend.core.config import settings

def test_connection():
    engine = create_engine(settings.DATABASE_URL)
    connection = engine.connect()
    connection.close()
    engine.dispose()

max_retries = 30
retry_count = 0

while retry_count < max_retries:
    try:
        test_connection()
        print('Database is available!')
        sys.exit(0)
    except Exception as e:
        retry_count += 1
        print(f'Database unavailable, attempt {retry_count}/{max_retries}. Error: {e}')
        print('Waiting 2 seconds...')
        time.sleep(2)

print('Database connection failed after maximum retries')
sys.exit(1)
"
}

# Function to run database migrations
run_migrations() {
    echo "Running database migrations..."
    if poetry run alembic upgrade head; then
        echo "Migrations completed successfully"
    else
        echo "Migration failed"
        exit 1
    fi
}

# Main execution flow
main() {
    echo "Starting initialization sequence..."

    # Always wait for database
    wait_for_db

    # Run migrations
    run_migrations

    echo "Initialization completed successfully!"

    # Handle different modes based on environment or command
    MODE=${1:-${APP_MODE:-development}}

    case "$MODE" in
        "development"|"dev")
            echo "=== Starting FastAPI server in development mode ==="
            exec poetry run uvicorn backend.main:app \
                --host 0.0.0.0 \
                --port 8000 \
                --reload
            ;;
        "production"|"prod")
            echo "=== Starting FastAPI server in production mode ==="
            exec poetry run gunicorn backend.main:app \
                -w ${WORKERS:-4} \
                -k uvicorn.workers.UvicornWorker \
                --bind 0.0.0.0:${PORT:-8000} \
                --access-logfile - \
                --error-logfile - \
                --timeout ${TIMEOUT:-120} \
                --preload
            ;;
        "migrate")
            echo "=== Running migrations only ==="
            run_migrations
            echo "Migrations completed, exiting."
            exit 0
            ;;
        *)
            echo "Unknown mode: $MODE"
            echo "Available modes: development, production, migrate"
            exit 1
            ;;
    esac
}

# Handle signals gracefully
trap 'echo "Received termination signal, shutting down..."; exit 0' TERM INT

# Run main function
main "$@"