#!/bin/bash

echo "💰 Starting Automated Revenue System..."
echo "🚀 This system will make money 24/7 without your input!"
echo ""

# Check if virtual environment exists, create if not
if [ ! -d "revenue_env" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv revenue_env
fi

# Activate virtual environment
source revenue_env/bin/activate

# Install dependencies if needed
echo "🔧 Installing dependencies..."
pip install -q fastapi uvicorn requests beautifulsoup4 python-dotenv

# Start the system
echo ""
echo "🎯 Starting Revenue Generation System..."
echo "🌐 Dashboard: http://localhost:8000"
echo "📊 API Docs: http://localhost:8000/docs"
echo ""
echo "💰 MAKING MONEY NOW! Press Ctrl+C to stop."
echo ""

python simple_main.py