#!/bin/bash
# 🌌 Solar System 3D - Quick Start (macOS/Linux)
# This script automatically sets up and runs the solar system simulation

echo ""
echo "🌌 Solar System 3D - Quick Start"
echo "================================"
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found! Please install Python 3.8+"
    echo "   https://www.python.org/downloads/"
    exit 1
fi

python3 --version
echo ""

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

echo ""
echo "📥 Installing dependencies..."
source venv/bin/activate
pip install -q -r requirements.txt
echo "✅ Dependencies installed"

echo ""
echo "🚀 Starting Solar System Physics Engine..."
echo ""
echo "================================================================"
echo "  🌌 Server running at: http://localhost:8000"
echo "  📚 API Documentation: http://localhost:8000/docs"
echo "  🌐 Frontend will open automatically..."
echo "================================================================"
echo ""

# Open browser (works on macOS and some Linux systems)
if command -v open &> /dev/null; then
    open "file://$(pwd)/templates/index.html"
elif command -v xdg-open &> /dev/null; then
    xdg-open "file://$(pwd)/templates/index.html"
fi

# Run server
python app.py
