#!/bin/bash

# Multi-Source Travel Planner API Startup Script

echo "🚀 Starting Multi-Source Travel Planner API"
echo "=========================================="

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "   Creating from .env.example..."
    cp .env.example .env
    echo "   ⚠️  Please edit .env and add your API keys before running again."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Check if Redis is running
echo "🔍 Checking Redis connection..."
if redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis is running"
else
    echo "⚠️  Redis is not running!"
    echo "   Start Redis with: brew services start redis"
    echo "   Or use Docker: docker-compose up -d"
    echo ""
    echo "   The API will work without Redis, but caching will be disabled."
    echo ""
fi

# Start the API
echo "🌐 Starting API server..."
echo "   API will be available at: http://localhost:8000"
echo "   Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python main.py

