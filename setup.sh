#!/bin/bash

# Rembg MCP Server Setup Script
# This script sets up the complete environment for the Rembg MCP server

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

print_status "Starting Rembg MCP Server setup..."
print_status "Working directory: $SCRIPT_DIR"

# Check uv installation
print_status "Checking uv installation..."
if ! command_exists uv; then
    print_error "uv is not installed. See https://docs.astral.sh/uv/ for installation instructions."
    exit 1
fi

print_success "uv $(uv --version | cut -d' ' -f2) found"

# Create the virtual environment and install all dependencies from pyproject.toml / uv.lock
print_status "Syncing environment with uv..."
uv sync

PYTHON_VERSION=$(uv run python --version 2>&1 | cut -d' ' -f2)
print_success "Python $PYTHON_VERSION ready"

# Test the installation
print_status "Testing installation..."
if uv run python test_server.py; then
    print_success "Installation test passed!"
else
    print_error "Installation test failed!"
    exit 1
fi

# Run comprehensive validation
print_status "Running comprehensive validation..."
if uv run python validate_setup.py; then
    print_success "All validation checks passed!"
else
    print_warning "Some validation checks failed, but basic installation completed"
fi

# Make scripts executable
print_status "Making scripts executable..."
chmod +x start_server.sh

# Create model cache directory
print_status "Creating model cache directory..."
mkdir -p "$HOME/.u2net"

# Check if user wants GPU support
echo
read -p "Do you want to install GPU support? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Installing GPU support..."
    uv sync --extra gpu
    print_success "GPU support installed!"
    print_warning "Note: GPU support requires CUDA or ROCm to be properly configured"
fi

# Generate configuration files
print_status "Generating configuration files..."

# Update claude_desktop_config.json with current path
cat > claude_desktop_config.json << EOF
{
  "mcpServers": {
    "rembg": {
      "command": "$SCRIPT_DIR/start_server.sh",
      "cwd": "$SCRIPT_DIR",
      "env": {
        "REMBG_HOME": "~/.u2net",
        "OMP_NUM_THREADS": "4"
      }
    }
  }
}
EOF

print_success "Updated claude_desktop_config.json with current path"

# Test server startup (quick test)
print_status "Testing server startup..."
timeout 5s ./start_server.sh 2>/dev/null || true
print_success "Server startup test completed"

# Model download section
echo
print_status "🤖 AI Model Setup"
echo "Rembg requires AI models to remove backgrounds. Models are cached locally (~/.u2net)"
echo "and only need to be downloaded once."
echo

# Check if any models already exist
MODEL_CACHE="$HOME/.u2net"
if [ -d "$MODEL_CACHE" ] && [ "$(ls -A $MODEL_CACHE 2>/dev/null)" ]; then
    print_success "Found existing models in cache"
    ls -la "$MODEL_CACHE"/*.onnx 2>/dev/null | awk '{print "  • " $9}' || true
    echo
fi

read -p "Would you like to download AI models now? (Y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
    print_status "Starting model download..."
    ./download_models.sh
    echo
else
    print_warning "Skipping model download."
    print_warning "Models will be downloaded automatically when first used, but this may cause delays."
    echo "You can download models later by running: ./download_models.sh"
fi

# Print setup summary
echo
print_success "🎉 Rembg MCP Server setup completed successfully!"
echo
echo "📋 Setup Summary:"
echo "  ✓ uv environment synced: $SCRIPT_DIR/.venv"
echo "  ✓ Dependencies installed from uv.lock"
echo "  ✓ MCP server installed in development mode"
echo "  ✓ Scripts made executable"
echo "  ✓ Configuration files updated"
echo
echo "🚀 Next Steps:"
echo
echo "1. Start the server:"
echo "   ./start_server.sh"
echo
echo "2. For Claude Desktop, copy this configuration to your settings:"
echo "   macOS: ~/Library/Application Support/Claude/claude_desktop_config.json"
echo "   Windows: %APPDATA%\\Claude\\claude_desktop_config.json"
echo
echo "3. For Claude Code CLI, add the MCP server configuration"
echo
echo "4. For Cursor IDE, add to .cursor/settings.json"
echo
echo "📖 Documentation:"
echo "   - README.md: Complete usage guide"
echo "   - USAGE_CN.md: Chinese documentation"
echo "   - example_usage.py: Code examples"
echo
echo "🔧 Configuration:"
echo "   - Server script: $SCRIPT_DIR/start_server.sh"
echo "   - Model cache: ~/.u2net"
echo "   - Config file: $SCRIPT_DIR/claude_desktop_config.json"
echo
print_success "Setup complete! The Rembg MCP server is ready to use."