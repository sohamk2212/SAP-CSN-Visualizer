#!/bin/bash
# Setup script for CSN Object Visualizer

echo \"🧩 CSN Object Visualizer - Setup Script\"
echo \"========================================\"
echo \"\"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo \"❌ Python 3 is not installed. Please install Python 3.8 or higher.\"
    exit 1
fi

echo \"✓ Python detected: $(python3 --version)\"
echo \"\"

# Create virtual environment
echo \"📦 Creating virtual environment...\"
if [ -d \".venv\" ]; then
    echo \"⚠️  Virtual environment already exists. Using existing environment.\"
else
    python3 -m venv .venv
    echo \"✓ Virtual environment created\"
fi

echo \"\"

# Activate virtual environment
echo \"⚡ Activating virtual environment...\"
source .venv/bin/activate
echo \"✓ Virtual environment activated\"

echo \"\"

# Upgrade pip
echo \"🔄 Upgrading pip...\"
pip install --upgrade pip > /dev/null 2>&1
echo \"✓ Pip upgraded\"

echo \"\"

# Install requirements
echo \"📚 Installing dependencies...\"
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo \"✓ Dependencies installed successfully\"
else
    echo \"❌ Failed to install dependencies\"
    exit 1
fi

echo \"\"

# Verify installation
echo \"🔍 Verifying installation...\"
python3 -c \"import streamlit; import pandas; import openpyxl\" 2>/dev/null
if [ $? -eq 0 ]; then
    echo \"✓ All dependencies verified\"
else
    echo \"⚠️  Some dependencies may not be properly installed\"
fi

echo \"\"
echo \"========================================\"
echo \"✅ Setup Complete!\"
echo \"========================================\"
echo \"\"
echo \"📝 Next Steps:\"
echo \"\"
echo \"1. Activate the virtual environment (if not already active):\"
echo \"   source .venv/bin/activate\"
echo \"\"
echo \"2. Run the application:\"
echo \"   streamlit run app.py\"
echo \"\"
echo \"3. Open your browser to: http://localhost:8501\"
echo \"\"
echo \"📖 For more information, see README.md\"
echo \"\"
