#!/bin/bash
echo "Initializing database..."
if ! python -m app.initial_data; then
    echo "Failed to initialize database. Exiting."
    exit 1
fi
echo "Database initialized successfully. Starting server..."
python -m uvicorn app.main:app --reload --host $HOST --port $PORT --log-level debug