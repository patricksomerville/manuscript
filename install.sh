#!/bin/bash
#
# Manuscript Workflow Installation Script
# Installs the manuscript CLI tool and dependencies
#

set -e

echo "📚 Installing Manuscript Workflow System"
echo "========================================"
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Found Python $PYTHON_VERSION"

# Install Python dependencies
if [ -f "requirements.txt" ]; then
    echo ""
    echo "📦 Installing Python dependencies..."
    pip3 install --user -r requirements.txt
    echo "✓ Dependencies installed"
fi

# Create symlink for CLI
INSTALL_DIR="$HOME/.local/bin"
mkdir -p "$INSTALL_DIR"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CLI_SOURCE="$SCRIPT_DIR/manuscript_cli.py"
CLI_TARGET="$INSTALL_DIR/manuscript"

if [ -L "$CLI_TARGET" ]; then
    rm "$CLI_TARGET"
fi

ln -s "$CLI_SOURCE" "$CLI_TARGET"
chmod +x "$CLI_SOURCE"

echo ""
echo "✓ CLI installed to $CLI_TARGET"

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo ""
    echo "⚠️  Warning: $INSTALL_DIR is not in your PATH"
    echo "   Add this line to your ~/.bashrc or ~/.zshrc:"
    echo ""
    echo "   export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "Next steps:"
echo "  1. Initialize your project:"
echo "     manuscript init --airtable-key YOUR_KEY --airtable-base YOUR_BASE"
echo ""
echo "  2. Check status:"
echo "     manuscript status"
echo ""
echo "  3. Segment a chapter:"
echo "     manuscript segment your_chapter.txt CH001"
echo ""

