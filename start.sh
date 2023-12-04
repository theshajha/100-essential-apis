#!/bin/bash

# Run database migrations
python manage.py migrate

# Start Uvicorn with specified workers and uvloop
uvicorn odyssey.asgi:application --host 0.0.0.0 --port 8000 --workers 4 --loop uvloop --http h11
