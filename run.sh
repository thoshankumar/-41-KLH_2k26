#!/bin/bash

# AI Behavioral Finance Coach - Run Script
# Makes it easy to start the application

echo "🏦 AI Behavioral Finance Coach"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

echo "✓ pip found"
echo ""

# Check if requirements are installed
echo "📦 Checking dependencies..."
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "⚠️  Dependencies not installed. Installing now..."
    pip3 install -r requirements.txt
    echo ""
fi

echo "✓ All dependencies installed"
echo ""

# Start the application
echo "🚀 Starting AI Behavioral Finance Coach..."
echo ""
echo "The application will open in your browser at:"
echo "http://localhost:8501"
echo ""
echo "Demo Account:"
echo "  Email: demo@financecoach.ai"
echo "  Password: demo123"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""
echo "================================"
echo ""

streamlit run app.py
