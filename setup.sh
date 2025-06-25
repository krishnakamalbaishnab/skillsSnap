#!/bin/bash

# SkillSnap Backend Setup Script
echo "🚀 Setting up SkillSnap Backend..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $required_version or higher is required. Found: $python_version"
    exit 1
fi

echo "✓ Python $python_version detected"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv skillsnap_env

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source skillsnap_env/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📋 Installing dependencies..."
pip install -r requirements.txt

# Download spaCy model
echo "🤖 Downloading spaCy model..."
python -m spacy download en_core_web_sm

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the server:"
echo "  1. Activate the virtual environment: source skillsnap_env/bin/activate"
echo "  2. Run the application: python app.py"
echo ""
echo "To deactivate the virtual environment when done: deactivate" 