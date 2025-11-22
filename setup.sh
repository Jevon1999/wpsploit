#!/bin/bash
# Quick Start Script untuk WP AutoExploit Tool

echo "=================================================="
echo "WP AutoExploit Tool - Quick Start"
echo "=================================================="

# Check Python
echo -e "\n[1] Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ $PYTHON_VERSION found"
else
    echo "✗ Python3 not found. Please install Python 3.7+"
    exit 1
fi

# Check Git
echo -e "\n[2] Checking Git..."
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version)
    echo "✓ $GIT_VERSION found"
else
    echo "✗ Git not found. Installing..."
    sudo apt-get update && sudo apt-get install -y git
fi

# Install Python dependencies
echo -e "\n[3] Installing Python dependencies..."
pip3 install -r requirements.txt

# Check Nuclei
echo -e "\n[4] Checking Nuclei..."
if command -v nuclei &> /dev/null; then
    NUCLEI_VERSION=$(nuclei -version 2>&1 | head -n1)
    echo "✓ $NUCLEI_VERSION found"
else
    echo "✗ Nuclei not found. Installing..."
    wget -q https://github.com/projectdiscovery/nuclei/releases/latest/download/nuclei_linux_amd64.zip
    unzip -q nuclei_linux_amd64.zip
    chmod +x nuclei
    sudo mv nuclei /usr/local/bin/
    rm nuclei_linux_amd64.zip
    echo "✓ Nuclei installed"
fi

# Create necessary directories
echo -e "\n[5] Creating directories..."
mkdir -p cache/exploitdb
mkdir -p logs
mkdir -p results
echo "✓ Directories created"

# Test installation
echo -e "\n[6] Running integration tests..."
python3 test_integration.py

echo -e "\n=================================================="
echo "Setup Complete!"
echo "=================================================="
echo ""
echo "🚀 Usage - DEFAULT INTERACTIVE MODE:"
echo ""
echo "   python3 main.py"
echo ""
echo "   Menu interaktif dengan ASCII banner akan muncul! ✨"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📚 Other Usage Examples:"
echo ""
echo "   1. Interactive dengan target:"
echo "      python3 main.py https://target.com"
echo ""
echo "   2. Command-line mode (advanced):"
echo "      python3 main.py https://target.com --no-interactive --exploit"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "⚠️  REMEMBER: Only use on authorized targets!"
echo "=================================================="
