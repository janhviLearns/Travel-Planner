#!/bin/bash

# Travel Planner Setup Script
# This script sets up both the backend and frontend

set -e  # Exit on error

echo "🌍 AI Travel Planner Setup"
echo "=========================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18 or higher."
    exit 1
fi

echo "✅ Node.js found: $(node --version)"

# Backend setup
echo ""
echo "📦 Setting up backend..."
echo "------------------------"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install backend dependencies
echo "Installing backend dependencies..."
pip install -r requirements.txt

# Frontend setup
echo ""
echo "📦 Setting up frontend..."
echo "------------------------"

cd frontend

# Install frontend dependencies
echo "Installing frontend dependencies..."
npm install

# Build frontend
echo "Building frontend for production..."
npm run build

cd ..

# Check for .env file
echo ""
echo "🔑 Checking environment configuration..."
echo "----------------------------------------"

if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from example..."
    cp example.env .env
    echo "📝 Please edit .env and add your API keys:"
    echo "   - OPENAI_API_KEY"
    echo "   - OPENWEATHER_API_KEY"
    echo "   - FOURSQUARE_API_KEY"
else
    echo "✅ .env file found"
fi

# Check Redis
echo ""
echo "🔍 Checking Redis..."
echo "-------------------"

if command -v redis-cli &> /dev/null; then
    if redis-cli ping &> /dev/null; then
        echo "✅ Redis is running"
    else
        echo "⚠️  Redis is installed but not running. Start it with:"
        echo "   brew services start redis  # macOS"
        echo "   sudo systemctl start redis  # Linux"
    fi
else
    echo "⚠️  Redis is not installed. Install it with:"
    echo "   brew install redis  # macOS"
    echo "   sudo apt install redis-server  # Linux"
fi

echo ""
echo "✅ Setup complete!"
echo "=================="
echo ""
echo "🚀 To start the application:"
echo ""
echo "1. Make sure Redis is running"
echo "2. Ensure .env has your API keys"
echo "3. Run: python main.py"
echo "4. Open: http://localhost:8000/ui"
echo ""
echo "📚 For development mode (with hot reload):"
echo ""
echo "Terminal 1: python main.py"
echo "Terminal 2: cd frontend && npm run dev"
echo "Then open: http://localhost:5173"
echo ""
echo "📖 Read REACT_UI_SETUP.md for more details"
echo ""

