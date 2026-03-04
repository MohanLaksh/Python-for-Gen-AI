#!/bin/bash
# Setup script for ChromaDB environment with Python 3.11/3.12/3.13

echo "Setting up ChromaDB environment..."

# Check for compatible Python versions (3.11, 3.12, or 3.13)
if command -v python3.12 &> /dev/null; then
    echo "✓ Python 3.12 found"
    PYTHON_CMD="python3.12"
elif command -v python3.13 &> /dev/null; then
    echo "✓ Python 3.13 found (should work with ChromaDB)"
    PYTHON_CMD="python3.13"
elif command -v python3.11 &> /dev/null; then
    echo "✓ Python 3.11 found (will also work)"
    PYTHON_CMD="python3.11"
else
    echo "✗ Python 3.11, 3.12, or 3.13 not found."
    echo ""
    echo "Install Python 3.12 using one of these methods:"
    echo "  Homebrew: brew install python@3.12"
    echo "  pyenv:    pyenv install 3.12"
    echo ""
    exit 1
fi

# Create virtual environment
VENV_NAME=".venv_chroma"
echo "Creating virtual environment: $VENV_NAME"
$PYTHON_CMD -m venv $VENV_NAME

# Activate and install dependencies
echo "Installing dependencies..."
source $VENV_NAME/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install langchain-community chromadb

echo ""
echo "✓ Setup complete!"
echo ""
echo "To activate this environment, run:"
echo "  source $VENV_NAME/bin/activate"
echo ""
echo "Then run your scripts:"
echo "  python workpad.py"
