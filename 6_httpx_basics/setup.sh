#!/bin/bash

# HTTPX Tutorial Setup Script
# This script sets up the virtual environment and installs dependencies

echo "=========================================="
echo "HTTPX Tutorial Setup"
echo "=========================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

if [ $? -eq 0 ]; then
    echo "✓ Virtual environment created"
else
    echo "❌ Failed to create virtual environment"
    exit 1
fi

echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

if [ $? -eq 0 ]; then
    echo "✓ Virtual environment activated"
else
    echo "❌ Failed to activate virtual environment"
    exit 1
fi

echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet

echo "✓ pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "=========================================="
echo "Setup Complete! 🎉"
echo "=========================================="
echo ""
echo "To get started:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run the examples:"
echo "     python 01_httpx-basics.py"
echo "     python 04_httpx-async.py"
echo "     python 05_httpx-streaming.py"
echo ""
echo "  3. For OpenAI examples, set your API key:"
echo "     export OPENAI_API_KEY='your-api-key-here'"
echo "     python 06_httpx-openai.py"
echo ""
echo "  4. Read the documentation:"
echo "     cat README.md"
echo "     cat CHEATSHEET.md"
echo ""
echo "Happy coding! 🚀"
