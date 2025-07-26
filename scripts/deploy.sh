#!/bin/bash

# PaiNaiDee Database Deployment Script
# This script handles database migrations and application deployment

set -e

echo "🚀 Starting PaiNaiDee Database deployment..."

# Load environment variables if .env file exists
if [ -f .env ]; then
    echo "📋 Loading environment variables from .env file..."
    source .env
fi

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo "❌ ERROR: DATABASE_URL environment variable is not set"
    echo "Please set DATABASE_URL or create a .env file"
    exit 1
fi

echo "🗄️  Database URL: ${DATABASE_URL%:*}:****"

# Function to wait for database to be ready
wait_for_db() {
    echo "⏳ Waiting for database to be ready..."
    timeout=30
    while ! pg_isready -d "$DATABASE_URL" > /dev/null 2>&1; do
        timeout=$((timeout - 1))
        if [ $timeout -eq 0 ]; then
            echo "❌ ERROR: Database is not ready after 30 seconds"
            exit 1
        fi
        echo "  Waiting for database... ($timeout seconds remaining)"
        sleep 1
    done
    echo "✅ Database is ready!"
}

# Function to run database migrations
run_migrations() {
    echo "🔄 Running database migrations..."
    
    if [ -d "migrations" ]; then
        echo "  Found migrations directory, running Alembic migrations..."
        alembic upgrade head
        echo "✅ Migrations completed successfully!"
    else
        echo "  No migrations directory found, creating tables directly..."
        python -c "
import os
from api.models import Base
from api.config import db_config
engine = db_config.get_engine()
Base.metadata.create_all(bind=engine)
print('✅ Database tables created successfully!')
"
    fi
}

# Function to populate test data (optional)
populate_test_data() {
    if [ "$POPULATE_TEST_DATA" = "true" ]; then
        echo "🌱 Populating test data..."
        python db_script.py
        echo "✅ Test data populated successfully!"
    else
        echo "ℹ️  Skipping test data population (set POPULATE_TEST_DATA=true to enable)"
    fi
}

# Function to start the application
start_application() {
    echo "🎯 Starting PaiNaiDee API application..."
    
    if [ "$ENVIRONMENT" = "development" ]; then
        echo "  Starting in development mode with auto-reload..."
        uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000} --reload
    else
        echo "  Starting in production mode..."
        uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers ${WORKERS:-4}
    fi
}

# Main deployment process
main() {
    case "${1:-deploy}" in
        "migrate")
            wait_for_db
            run_migrations
            ;;
        "populate")
            wait_for_db
            populate_test_data
            ;;
        "start")
            start_application
            ;;
        "deploy")
            wait_for_db
            run_migrations
            populate_test_data
            start_application
            ;;
        "test")
            echo "🧪 Running tests..."
            wait_for_db
            run_migrations
            pytest tests/ -v
            ;;
        "help")
            echo "Usage: $0 [command]"
            echo "Commands:"
            echo "  deploy    - Full deployment (migrate, populate, start) [default]"
            echo "  migrate   - Run database migrations only"
            echo "  populate  - Populate test data only"
            echo "  start     - Start application only"
            echo "  test      - Run tests"
            echo "  help      - Show this help message"
            ;;
        *)
            echo "❌ Unknown command: $1"
            echo "Run '$0 help' for usage information"
            exit 1
            ;;
    esac
}

# Trap to handle interrupts gracefully
trap 'echo "⚠️  Deployment interrupted"; exit 1' INT

# Run main function with all arguments
main "$@"