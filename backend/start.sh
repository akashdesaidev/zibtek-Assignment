#!/bin/bash

echo "Starting Zibtek AI Chatbot Backend..."

# Wait for Qdrant to be ready
echo "Waiting for Qdrant to be ready..."
sleep 5

# Check if data needs to be ingested
echo "Checking if data ingestion is needed..."
python -m app.ingest_data

# Start the FastAPI application
echo "Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000


